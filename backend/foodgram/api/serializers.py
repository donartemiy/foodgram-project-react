from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Subscription, Tag)
from rest_framework import serializers
from users.models import User
# from djoser.serializers import UserSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


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


class RecipeForFavoriteSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения добавления/удаления favorite. """
    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'


class RecipeSerializer(serializers.ModelSerializer):
    """Для просмотра рецепта"""
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True,
                                             # Использовать связную модель
                                             source='rname_recipe_ingredients')
    is_favorited = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients', 'name', 'image',
                  'text', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')

    def to_representation(self, instance):
        """Преобразуем данные перед выводом."""
        representation = super().to_representation(instance)
        # Преобразуем is_favorited в True, если есть связанные записи
        if instance.is_favorited.exists():
            representation['is_favorited'] = True
        else:
            representation['is_favorited'] = False
        return representation


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Прокидываем id ингредиента в рецепт, при создании рецепта. """
    id = serializers.PrimaryKeyRelatedField(source='ingredient',
                                            queryset=Ingredient.objects.all())
    # amount = serializers.IntegerField(source='profile.street')

    class Meta:
        model = RecipeIngredient
        fields = 'id', 'amount'


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Для создания рецепта. """
    ingredients = RecipeIngredientCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time', 'text', 'tags', 'ingredients')
        # fields = ('name', 'cooking_time', 'text', 'tags')

    def create(self, validated_data):
        """ Станадртный create не может сам создать объекты записываемые
        вложенные поля. Поле ingredients. """
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)

        # Обновление данных ингредиентов
        for ingredient_data in ingredients:
            RecipeIngredient(recipe=instance,
                             ingredient=ingredient_data['ingredient'],
                             amount=ingredient_data['amount']).save()
        return instance

    def update(self, instance, validated_data):
        # Обновление данных основного объекта Recipe
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.save()

        # Обновление данных тегов
        tags_data = validated_data.pop('tags', [])
        instance.tags.set(tags_data)

        # Обновление данных ингредиентов
        ingredients = validated_data.pop('ingredients', [])
        instance.ingredients.clear()
        for ingredient_data in ingredients:
            RecipeIngredient.objects.create(recipe=instance, **ingredient_data)
        return instance

    def to_representation(self, instance):
        """ Для отображения данных после создания рецепта. """
        return RecipeSerializer(instance).data


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class SubscriptionListSerializer(serializers.ModelSerializer):
    """Мои подписки.
    http://localhost/api/users/subscriptions/"""
    # recipes = serializers.SerializerMethodField() TODO

    class Meta:
        model = Subscription
        fields = ('id', 'follower', 'following', )

    def get_recipes(self, instance):
        print(instance)
        print(instance.rname_recipe_author.all())
        return instance


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с информацией о пользователях.
    http://127.0.0.1:8000/api/users/"""
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name')
