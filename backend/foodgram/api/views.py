from django.shortcuts import get_object_or_404
from api.serializers import (FavoriteSerializer, ShoppingCartSerializer,
                             IngredientSerializer, RecipeSerializer,
                             SubscriptionSerializer, TagSerializer,
                             RecipeCreateSerializer,
                             RecipeForFavoriteSerializer,
                             SubscriptionListSerializer,
                             UserSerializer,
                             UserSubscribeSerializer,
                             #  PasswordSerializer,
                             MyCustomUserSerializer,
                             )
from recipes.models import (Favorite, ShoppingCart, Ingredient, Recipe,
                            Subscription, Tag, RecipeIngredient)
from users.models import User
from rest_framework import viewsets
# для favorite
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework import permissions
from djoser.views import UserViewSet
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
import os
from foodgram.settings import MEDIA_ROOT
from django.http import HttpResponse, FileResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import IsAdminOrAuthorElseReadOnly

# path('users/<int:pk>/', MyUserViewSet.as_view({'get': 'retrieve'})),
# from rest_framework.mixins import RetrieveModelMixin


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAdminOrAuthorElseReadOnly,)

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

    @action(methods=['post', 'delete'],
            detail=True,
            url_path='favorite',
            url_name='favorite',
            permission_classes=['IsAuthenticated'])
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

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=['IsAuthenticated'])
    def shopping_cart(self, request, pk):
        """Работа со списком покупок. Удаление/добавление в список покупок. """
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(data={'user': request.user.id, 'recipe': recipe.id, },)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            error_message = 'У вас нет этого рецепта в списке покупок'
            if not ShoppingCart.objects.filter(user=request.user, recipe=recipe).exists():
                return Response({'errors': error_message}, status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.filter(user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        author = request.user
        shopping_cart = author.shopping_cart.all()
        buying_list = {}
        for record in shopping_cart:
            recipe = record.recipe
            ingredients = RecipeIngredient.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in buying_list:
                    buying_list[name] = {
                        "measurement_unit": measurement_unit,
                        "amount": amount,
                    }
                else:
                    buying_list[name]["amount"] = (
                        buying_list[name]["amount"] + amount
                    )
        wishlist = []
        for name, data in buying_list.items():
            wishlist.append(
                f"\n{name} ({data['measurement_unit']}) - {data['amount']}"
            )
        content = "".join(wishlist)
        
        # Создание файла shopping_cart.txt в папке media
        filename = 'shopping_cart.txt'
        filepath = os.path.join(MEDIA_ROOT, filename)
        with open(filepath, 'w') as file:
            file.write(content)
        
        return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class SubscriptionViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = SubscriptionListSerializer

    def get_queryset(self):
        return User.objects.filter(following__follower=self.request.user)


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

    @action(
        methods=["get"], detail=False,
        # permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = MyCustomUserSerializer(user)
        return Response(serializer.data)

    # @action(["post"], detail=False)
    # def set_password(self, request, *args, **kwargs):
    #     user = self.request.user
    #     serializer = PasswordSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user.set_password(serializer.validated_data["new_password"])
    #         user.save()
    #         return Response({"status": "password set"})
    #     else:
    #         return Response(
    #             serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #         )


class UserSubscribeView(APIView):
    """Создание/удаление подписки на пользователя."""
    permission_classes = (IsAuthenticated,)

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
