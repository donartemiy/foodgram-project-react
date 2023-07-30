from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from recipes.models import Favorite, ShoppingCart, Ingredient, Recipe, Tag, RecipeIngredient, Subscription
from users.models import User


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )
    list_display = ('name', 'author', 'favorites_amount')
    list_filter = ('author', 'name', 'tags')

    def favorites_amount(self, obj):
        return obj.is_favorited.count()


admin.site.register(ShoppingCart)
admin.site.register(Favorite)
# admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Subscription)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    # empty_value_display = settings.EMPTY_VALUE


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name', )
