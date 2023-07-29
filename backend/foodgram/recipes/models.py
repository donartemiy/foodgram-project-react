from django.db import models

from users.models import User


class Recipe(models.Model):
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Список id тегов')
    author = models.ForeignKey(  # У разных постов один автор
        User,
        on_delete=models.CASCADE,
        related_name='rname_recipe_author')
    ingredients = models.ManyToManyField(  # У разных рецпетов неск. ингр-ов
        'Ingredient',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        related_name='rname_recipes',
        verbose_name='Список ингредиентов')
    is_favorited = models.ManyToManyField(
        User,
        through='Favorite',
        through_fields=('recipe', 'user'),
        blank=True,
        related_name='rname_recipes_is_favorited')
    is_in_shopping_cart = models.ManyToManyField(
        User,
        through='ShoppingCart',
        through_fields=('recipe', 'user'),
        related_name='rname_recipes_is_in_shopping_cart')
    image = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Картинка, закодированная в Base64')
    name = models.CharField(
        max_length=200,
        verbose_name='Название')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveIntegerField(     # >= 1
        verbose_name='Время приготовления в минутах')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return f'РЕЦЕПТ {self.name}'


class Ingredient(models.Model):
    name = models.CharField(max_length=200)  # primary_key=True
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        default_related_name = 'ingredient'

    def __str__(self):
        return f'ИНГРЕДИЕНТ {self.name}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='rname_recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f'РЕЦЕПТИНГРЕДИЕНТ {self.recipe}'


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    color = models.CharField(max_length=7, verbose_name='Цвет в HEX')
    slug = models.SlugField(max_length=200, verbose_name='Уникальный слаг',
                            unique=True)

    def __str__(self):
        return f'ТЭГ {self.name}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'user'],
                                    name='unique_like')
        ]

    def __str__(self):
        return f'ИЗБРАННОЕ{self.user}, id рецепта: {self.recipe.id}, {self.recipe}'


class Subscription(models.Model):
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор(на когоподписаны)',
        related_name='following')
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик/Юзер(кто подписан)',
        related_name='follower')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['following', 'follower'],
            name='unique subs')
        ]

    def __str__(self):
        return f'ПОДПИСКИ {self.follower} подписан на {self.following}'
