from api.views import (FavoriteViewSet, ShoppingCartViewSet, IngredientViewSet,
                       RecipeViewSet, SubscriptionViewSet, TagViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('shopping_cart', ShoppingCartViewSet, basename='shopping_cart')
# router.register('users', SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    # из теории router.register(r'profile/(?P<username>[\w.@+-]+)/', AnyViewSet)
    path('users/subscriptions', SubscriptionViewSet.as_view({'get': 'list'})),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
