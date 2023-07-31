from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, RecipeViewSet, SubscriptionViewSet,
                       TagViewSet, UserSubscribeView)


router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('users/subscriptions/', SubscriptionViewSet.as_view({'get': 'list'})),
    path('users/<int:pk>/subscribe/', UserSubscribeView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
