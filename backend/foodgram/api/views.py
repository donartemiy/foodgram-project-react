from django.shortcuts import get_object_or_404
from api.serializers import (FavoriteSerializer, ShoppingCartSerializer,
                             IngredientSerializer, RecipeSerializer,
                             SubscriptionSerializer, TagSerializer,
                             RecipeCreateSerializer,
                             RecipeForFavoriteSerializer,
                             SubscriptionListSerializer,
                             UserSerializer)
from recipes.models import (Favorite, ShoppingCart, Ingredient, Recipe,
                            Subscription, Tag)
from users.models import User
from rest_framework import viewsets
# для favorite
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        """При create используем сериализатор с одними полями,
        иначе с другими."""
        if self.action in ["create", "update", "partial_update"]:
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        """Подставляем текущего пользователя к данным из запроса create."""
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """Оптимизация запросов M2M."""
        recipes = Recipe.objects.prefetch_related(
            'rname_recipe_ingredients__ingredient', 'tags')
        return recipes

    @action(methods=['post', 'delete'], detail=True, url_path='favorite', url_name='favorite')
    def favorite(self, request, pk=None):
        """Создает ссылку recipes/{pk}/favorite
        и добавляет/удаляет запись в таблицу. """
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response({"errors": "Is already exist"},
                                status=status.HTTP_400_BAD_REQUEST)
            obj_favorite = Favorite.objects.create(user=user, recipe=recipe)
            obj_recipe = obj_favorite.recipe
            serialised_data = RecipeForFavoriteSerializer(instance=obj_recipe)
            return Response(serialised_data.data,
                            status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response({"errors": "Is already deleted"},
                                status=status.HTTP_400_BAD_REQUEST)
            obj_favorite = Favorite.objects.get(user=user, recipe=recipe)
            obj_favorite.delete()
            return Response(None)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def list(self, request):
        author = self.request.user
        queryset = Subscription.objects.filter(follower=author.id)
        serializer = SubscriptionListSerializer(queryset, many=True)
        return Response(serializer.data)


class UserListViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
