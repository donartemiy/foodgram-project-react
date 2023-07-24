from api.serializers import (FollowSerializer, GrossaryListSerializer,
                             IngredientSerializer, RecipeSerializer,
                             TagSerializer, Follow)
from recipes.models import Favorite, GrossaryList, Ingredient, Recipe, Tag
from rest_framework import viewsets


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class GrossaryListViewSet(viewsets.ModelViewSet):
    queryset = GrossaryList.objects.all()
    serializer_class = GrossaryListSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FollowSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
