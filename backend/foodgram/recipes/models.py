from django.db import models

from foodgram.settings import MAX_LENGTH, MAX_LENGTH_HEX
from users.models import User


class Recipe(models.Model):
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Список id тегов')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rname_recipe_author')
    ingredients = models.ManyToManyField(
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
        max_length=MAX_LENGTH,
        verbose_name='Название')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    measurement_unit = models.CharField(max_length=MAX_LENGTH)

    class Meta:
        default_related_name = 'ingredient'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='rname_recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return self.recipe


class Tag(models.Model):
    name = models.CharField(max_length=MAX_LENGTH,
                            verbose_name='Название')
    color = models.CharField(max_length=MAX_LENGTH_HEX,
                             verbose_name='Цвет в HEX')
    slug = models.SlugField(max_length=MAX_LENGTH,
                            verbose_name='Уникальный слаг',
                            unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shopping_cart'

    def __str__(self):
        return (f'{self.user.username} добавил '
                f'{self.recipe.name} в список покупок')


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'user'],
                                    name='unique_like')]

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в избраннное'


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
        return f'{self.follower.username} подписан на {self.following.username}'
