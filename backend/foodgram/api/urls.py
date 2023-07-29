from api.views import (FavoriteViewSet, ShoppingCartViewSet, IngredientViewSet,
                       RecipeViewSet, SubscriptionViewSet, TagViewSet,
                       UserListViewSet, MyUserViewSet,
                       UserSubscribeView)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from djoser.views import UserViewSet


router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
# router.register('users', TagViewSet, basename='users')

urlpatterns = [
    path('users/subscriptions/', SubscriptionViewSet.as_view({'get': 'list'})),
    path('users/<int:pk>/subscribe/', UserSubscribeView.as_view()),
    # url(..., include('djoser.urls.authtoken')), сделать для токенов
    # path('users/', MyUserViewSet.as_view({'get': 'list'})),
    # path('users/<int:pk>/', MyUserViewSet.as_view({'get': 'retrieve'})),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
