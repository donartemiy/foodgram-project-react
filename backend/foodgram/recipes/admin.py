from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from recipes.models import Favorite, GrossaryList, Ingredient, Recipe


class IngredientAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Recipe)
# admin.site.register(Ingredient)
admin.site.register(GrossaryList)
admin.site.register(Favorite)
admin.site.register(Ingredient, IngredientAdmin)
