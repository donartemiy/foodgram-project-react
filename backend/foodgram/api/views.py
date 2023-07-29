from django.shortcuts import get_object_or_404
from api.serializers import (FavoriteSerializer, ShoppingCartSerializer,
                             IngredientSerializer, RecipeSerializer,
                             SubscriptionSerializer, TagSerializer,
                             RecipeCreateSerializer,
                             RecipeForFavoriteSerializer,
                             SubscriptionListSerializer,
                             UserSerializer,
                             UserSubscribeSerializer)
from recipes.models import (Favorite, ShoppingCart, Ingredient, Recipe,
                            Subscription, Tag)
from users.models import User
from rest_framework import viewsets
# для favorite
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from djoser.views import UserViewSet
from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin


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
    """Не используется. Тут работало отображение всех пользователей
    path('users/', UserListViewSet.as_view({'get': 'list'})),"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MyUserViewSet(UserViewSet):
    """ Отображение всех пользователей. Через
    path('users/', UserViewSet.as_view({'get': 'list'})). """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        """Возвращает всех пользователей
        http://127.0.0.1:8000/api/users/"""
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """ Возвращает информацию о конкретном пользователе
        http://127.0.0.1:8000/api/users/1/. """
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserSubscribeView(APIView):
    """Создание/удаление подписки на пользователя."""
    def post(self, request, pk):
        following = get_object_or_404(User, id=pk)
        serializer = UserSubscribeSerializer(
            data={'follower': request.user.id, 'following': following.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        following = get_object_or_404(User, id=pk)
        if not Subscription.objects.filter(follower=request.user,
                                           following=following).exists():
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscription.objects.get(follower=request.user.id,
                                 following=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
