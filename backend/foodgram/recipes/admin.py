from django.contrib import admin

# Register your models here.

from foodgram.models import Recipe

admin.site.register(Recipe)
