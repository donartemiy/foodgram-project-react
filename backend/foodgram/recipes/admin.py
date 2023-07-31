from django.contrib import admin

from recipes.models import (Favorite, Ingredient, Recipe,
                            RecipeIngredient,
                            ShoppingCart, Subscription, Tag)
from users.models import User


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    # extra = 1


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )
    list_display = ('name', 'author', 'favorites_amount')
    list_filter = ('author', 'name', 'tags')

    def favorites_amount(self, obj):
        return obj.is_favorited.count()


admin.site.register(ShoppingCart)
admin.site.register(Favorite)
admin.site.register(Tag)
admin.site.register(Subscription)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name', )
