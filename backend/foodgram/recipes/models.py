from colorfield.fields import ColorField
from django.db import models
from django.core.validators import (MinValueValidator, MaxValueValidator,
                                    RegexValidator)

from foodgram.settings import MAX_LENGTH
from users.models import User


class Recipe(models.Model):
    tags = models.ManyToManyField(
        'Tag',
        blank=False,
        verbose_name='Список id тегов')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='rname_recipe_author')
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        blank=False,
        related_name='rname_recipes',
        verbose_name='Список ингредиентов')
    is_favorited = models.ManyToManyField(
        User,
        through='Favorite',
        through_fields=('recipe', 'user'),
        blank=True,
        verbose_name='В списке избранного',
        related_name='rname_recipes_is_favorited')
    is_in_shopping_cart = models.ManyToManyField(
        User,
        through='ShoppingCart',
        through_fields=('recipe', 'user'),
        verbose_name='В списке покупок',
        related_name='rname_recipes_is_in_shopping_cart')
    image = models.ImageField(
        # upload_to='images/',
        blank=True,
        null=True,
        verbose_name='Картинка, закодированная в Base64')
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название',
        validators=[
            RegexValidator(
                regex='^[а-яА-ЯёЁa-zA-Z]+$',
                message='Название рецепта должно быть в текстовом виде'
            )
        ])
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                1, 'Время приготовления не должно быть меньше 1 минуты'),
            MaxValueValidator(
                1440, 'Время приготовления не должно быть больше суток')])
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=MAX_LENGTH,
                            verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=MAX_LENGTH,
                                        verbose_name='Единицы измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit_ingredient'
            )
        ]
        default_related_name = 'ingredient'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Название рецепта',)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Название ингредиента',)
    amount = models.PositiveIntegerField(verbose_name='Количество ингредиента',
                                         validators=[
                                             MaxValueValidator(
                                                 1000, 'Количество < 1000'),
                                             MinValueValidator(
                                                 1, 'Количество > 0')])

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        default_related_name = 'rname_recipe_ingredients'

    def __str__(self):
        return f'{self.recipe}, {self.ingredient}'


class Tag(models.Model):
    name = models.CharField(max_length=MAX_LENGTH,
                            verbose_name='Название')
    color = ColorField(default='#FF0000',
                       verbose_name='Цвет в HEX')
    slug = models.SlugField(max_length=MAX_LENGTH,
                            verbose_name='Уникальный слаг',
                            unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'color', 'slug'],
                name='unique_tag_name_color_slug'
            )
        ]

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Название рецепта')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ('recipe',)
        default_related_name = 'shopping_cart'

    def __str__(self):
        return (f'{self.user.username} добавил '
                f'{self.recipe.name} в список покупок')


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Название рецепта')

    class Meta:
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списки избранного'
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'user'],
                                    name='unique_like')]

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в избраннное'
