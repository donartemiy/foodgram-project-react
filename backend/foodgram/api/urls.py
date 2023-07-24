from api.views import (FavoriteViewSet, FollowViewSet, GrossaryListViewSet,
                       IngredientViewSet, RecipeViewSet, TagViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('shoppong_cart', GrossaryListViewSet, basename='shoppong_cart')
router.register('users/favorite', FavoriteViewSet, basename='favorite')
router.register('users/subscriptions', FollowViewSet, basename='subscriptions')

urlpatterns = [
    path('', include(router.urls)),
]
