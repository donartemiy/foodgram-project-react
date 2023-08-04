from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import User, Subscription


class MyCustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с избранными рецептами."""
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в избранное')]

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': request}).data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id', 'name', 'color', 'slug'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Промежуточный сериалайзер для корректного
    отображаения ingredients в RecipeSerializer."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = 'id', 'name', 'amount', 'measurement_unit'

    def validate_amount(self, instance):
        """Количество ингредиента больше 0."""
        if instance <= 0:
            raise serializers.ValidationError("Введите число больше 0")
        return instance


class RecipeForFavoriteSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения добавления/удаления favorite. """
    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'


class RecipeSerializer(serializers.ModelSerializer):
    """Для просмотра рецепта. Через source='rname_recipe_ingredients'
    используем связную модель. """
    tags = TagSerializer(many=True)
    image = Base64ImageField()
    author = MyCustomUserCreateSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True,
                                             source='rname_recipe_ingredients')
    is_favorited = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time',)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and Favorite.objects.filter(author=request.user,
                                            recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and ShoppingCart.objects.filter(user=request.user,
                                                recipe=obj).exists())

    def to_representation(self, instance):
        """Преобразуем данные перед выводом. Определяем is_favorited,
        в зависимости от наличия связных списков. """
        representation = super().to_representation(instance)
        if instance.is_favorited.exists():
            representation['is_favorited'] = True
        else:
            representation['is_favorited'] = False
        return representation


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Прокидываем id ингредиента в рецепт, при создании рецепта. """
    id = serializers.PrimaryKeyRelatedField(source='ingredient',
                                            queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = 'id', 'amount'


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Для создания рецепта. """
    ingredients = RecipeIngredientCreateSerializer(many=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientCreateSerializer(many=True)
    cooking_time = serializers.IntegerField()
    tags = serializers.SlugRelatedField(
        many=True, queryset=Tag.objects.all(), slug_field="id"
    )

    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time', 'text', 'tags',
                  'ingredients', 'image')

    def create(self, validated_data):
        """ Станадртный create не может сам создать объекты
        записываемые вложенные поля. Поле ingredients. """
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)
        # Обновление данных ингредиентов
        for ingredient_data in ingredients:
            RecipeIngredient(recipe=instance,
                             ingredient=ingredient_data['ingredient'],
                             amount=ingredient_data['amount']).save()
        return instance

    def update(self, instance, validated_data):
        """ Обновление рецепта. Получаем значения
        вложенных полей тэгов и ингредиентов. """
        tags_data = validated_data.pop('tags', [])
        instance.tags.set(tags_data)
        ingredients = validated_data.pop('ingredients', [])
        instance.ingredients.clear()
        for ingredient_data in ingredients:
            RecipeIngredient.objects.create(recipe=instance, **ingredient_data)
        instance = super().update(instance, validated_data)
        return instance

    def validate_cooking_time(self, instance):
        """Время приготовления больше 0."""
        if instance <= 0:
            raise serializers.ValidationError("Введите число больше 0")
        return instance

    def to_representation(self, instance):
        """ Отображение данных после создания рецепта. """
        return RecipeSerializer(instance).data


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('following', 'follower')


class SubscriptionListSerializer(serializers.ModelSerializer):
    """ Мои подписки users/subscriptions. """
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField("get_recipes_count")

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes',
                  'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return Subscription.objects.filter(follower=request.user,
                                           following=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.rname_recipe_author.all()
        return RecipeShortSerializer(recipes, many=True,
                                     context={'request': request}).data

    def get_recipes_count(self, obj):
        return obj.rname_recipe_author.count()


class MyCustomUserSerializer(UserSerializer):
    """ Кастомное отображения полей при просмотре инфо о пользователях. """
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name')


class UserSubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки/отписки от пользователей."""
    class Meta:
        model = Subscription
        fields = ('following', 'follower')

    def validate(self, data):
        """Пользователь не может подписаться на самого себя."""
        request = self.context.get('request')
        check_uniq = Subscription.objects.filter(follower=request.user.id,
                                                 following=data['following'].id
                                                 ).exists()
        if request.user == data['following'] or check_uniq:
            raise serializers.ValidationError(
                'Такая подписка невозможна'
            )
        return data

    def to_representation(self, instance):
        """После POST возвращаем """
        request = self.context.get('request')
        return SubscriptionListSerializer(
            instance.following, context={'request': request}
        ).data


class RecipeShortSerializer(MyCustomUserCreateSerializer):
    """ Предоставление данных о рецептах в Подписки
     и Списке покупок. """
    class Meta:
        model = Recipe
        fields = ['id',
                  'name',
                  'image',
                  'cooking_time'
                  ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для работы со списком покупок."""
    class Meta:
        model = ShoppingCart
        fields = ['recipe', 'user']

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': request}).data
