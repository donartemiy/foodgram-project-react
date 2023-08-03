from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from recipes.models import (Favorite, Ingredient, Recipe,
                            RecipeIngredient,
                            ShoppingCart, Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    # Данный параметр указывает на количество строк в админке
    # при создании рецепта, в которые можно добавить ингредиенты.
    # То есть при значении 0, в админке еще нужно нажать на кнопку:
    # "+Добавить еще один Ингредиент в рецепте", но это не ограничивает
    # возможность админа создать рецепт без ингредиентов.
    # В модель добавил blank=False тоже не помогло.
    # Решение проблемы не нашел. Прошу подсказать.


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )
    list_display = ('name', 'author', 'favorites_amount',)
    list_filter = ('author', 'name', 'tags',)

    def favorites_amount(self, obj):
        return obj.is_favorited.count()


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)


class IngredientResource(resources.ModelResource):
    """ Необходим для импорта ингредиентов. """
    class Meta:
        model = Ingredient


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name', )
    resource_class = [IngredientResource]
