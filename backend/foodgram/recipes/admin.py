from django.contrib import admin
from recipes.models import Recipe, Ingredient, Tag, GrossaryList, Favorite

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(GrossaryList)
admin.site.register(Favorite)
