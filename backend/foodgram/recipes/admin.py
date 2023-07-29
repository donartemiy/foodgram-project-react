from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from recipes.models import Favorite, ShoppingCart, Ingredient, Recipe, Tag, RecipeIngredient, Subscription
from users.models import User


class IngredientAdmin(ImportExportModelAdmin):
    pass


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )


# admin.site.register(Recipe)
# admin.site.register(Ingredient)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Subscription)
admin.site.register(User)
