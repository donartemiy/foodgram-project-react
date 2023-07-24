from django.db import models

from users.models import User


TAG = [
    ('Завтрак', ('#E26C2D', 'breakfast')),
    ('Обед', ('#49B64E', 'breakfast')),
    ('Ужин', ('#3d66bf', 'dinner'))
]


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Называние рецепта')
    text = models.TextField(verbose_name='Рецепт')
    user_id = models.ForeignKey(  # У разных постов один автор
        User,
        on_delete=models.CASCADE)
    # Один юзер может лайнкуть много рецептов
    # Один пост может иметь много лайков
    like_id = models.ManyToManyField(
        User,
        through='Favorite',
        through_fields=('recipe_id', 'user_id'),
        blank=True,
        related_name='rname_recipes')
    image = models.ImageField(
        blank=True,
        null=True)
    ingredient_id = models.ManyToManyField(  # У разных рецпетов неск. ингр-ов
        'Ingredient',
        related_name='rname_recipes')
    quantity = models.PositiveIntegerField()
    tag_id = models.ManyToManyField('Tag')
    duration = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)  # primary_key=True
    measurement_unit = models.CharField(max_length=15)

    class Meta:
        default_related_name = 'ingredient'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=15, verbose_name='тэг')
    color = models.CharField(max_length=16)
    slug = models.SlugField(unique=True, verbose_name='Ссылка')


class GrossaryList(models.Model):
    user_id = models.ForeignKey(  # У разных листов один автор
        User,
        on_delete=models.CASCADE)
    # В одном списке покупок может быть несколько рецептов
    # Один рецепт пожет быть в нескольких листах
    recipe_id = models.ManyToManyField(Recipe)

    class Meta:
        default_related_name = 'rname_grossarylist'


class Favorite(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe_id', 'user_id'],
                                    name='unique_like')
        ]


class Follow(models.Model):
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following')
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['following', 'follower'],
            name='unique subs')
        ]
