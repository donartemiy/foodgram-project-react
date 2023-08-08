# import django_filters as filters
from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),)
#     is_favorited = filters.CharFilter(method="get_is_favorited")
#     is_in_shopping_cart = filters.CharFilter(
#         method='get_is_in_shopping_cart')

#     class Meta:
#         model = Recipe
#         fields = ["author", "tags", "is_favorited", "is_in_shopping_cart"]

#     def get_is_favorited(self, queryset, name, value):
#         user = self.request.user
#         if value:
#             return Recipe.objects.filter(favorite__user=user)
#         return Recipe.objects.all()

#     def get_is_in_shopping_cart(self, queryset, name, value):
#         user = self.request.user
#         if value:
#             return Recipe.objects.filter(shopping_cart__user=user)
#         return Recipe.objects.all()


# class IngredientFilter(FilterSet):
#     name = filters.CharFilter(field_name="name", lookup_expr="startswith")

    is_favorited = filters.BooleanFilter(
        method='is_favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filter')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def is_favorited_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorite_recipe__user=user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_recipe__user=user)
        return queryset

    class Meta:
        model = Ingredient
        fields = ("name",)
