from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()     # TODO new app


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Называние рецепта')
    text = models.TextField(verbose_name='Рецепт')
    user_id = models.ForeignKey(  # У разных постов один автор
        'User',
        on_delete=models.CASCADE)     
    like_id = models.ManyToManyField(
        'User',
        through='Favarite',
        through_fields=('recipe_id', 'user_id'),
        blank=True,
        related_name='rname_liked_recipes')
    image = models.ImageField(
        blank=True,
        null=True)
    ingredient_id = models.ManyToManyField(  # У разных рецпетов неск. ингр-ов
        'Inredient',
        related_name='rname_recipes')
    quantity = models.IntegerField()
    tag_id = models.ManyToManyField('Tag')  # У разных рецептов несколько тегов
    duration = models.IntegerField(
        verbose_name='Время приготовления в минутах')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Inredient(models.Model):
    name = models.CharField(max_length=200)
    measure = models.CharField(max_length=15)   # TODO choices

    def __str__(self):
        return f'{self.name}, {self.measure}'


class Tag(models.Model):
    name = models.CharField(max_length=15, verbose_name='тэг')
    color = models.CharField(max_length=16)
    slug = models.SlugField(unique=True, verbose_name='Ссылка')


class GrossaryList(models.Model):
    user_id = models.ForeignKey(   # У разных листов один автор
        'User',
        on_delete=models.CASCADE,
        related_name='rname_grossarylist_user')
    ingridient_id = models.ManyToManyField(  # У разных листов несколько ингр-ов
        'Recipe',
        related_name='rname_grossarylist_inredient')


class Favarite(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    recipe_id = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe_id', 'user_id'],
                                    name='unique_like')
        ]