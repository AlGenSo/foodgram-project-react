from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import mixins, pagination, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipesFilter
from api.pagination import MyCustomPagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (FaouriteSerializer, IngridientSerializer,
                             RecipeCreateSerializer, RecipeSerializer,
                             ShoppingListSerializer, SubscriptionsSerializer,
                             TagSerializer, UsersListSerializer)
from recipes.models import (Favourites, Ingredient, RecipeIngredientsAmount,
                            Recipes, ShoppingList, Tag)
from users.models import Subscription

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Реализация модели User"""
    queryset = User.objects.all()
    serializer_class = UsersListSerializer
    permission_classes = (AllowAny,)
    pagination_class = pagination.LimitOffsetPagination

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(AuthorOrReadOnly,)
            )
    def subscribe(self, request, id):
        author = get_object_or_404(self.queryset, id=id)
        serializer = SubscriptionsSerializer(
            author, data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        print(str(serializer))

        if request.method == 'POST':
            Subscription.objects.create(user=request.user, author=author)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        get_object_or_404(Subscription,
                          user=request.user,
                          author=author).delete()

        return Response({'detail': 'Успешная отписка'},
                        status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False,
            pagination_class=MyCustomPagination)
    def subscriptions(self, request):

        if self.request.user.is_anonymous:

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        pages = self.paginate_queryset(
            User.objects.filter(blogger__user=self.request.user)
        )
        serializer = SubscriptionsSerializer(pages, many=True,
                                             context={'request': request})

        return self.get_paginated_response(serializer.data)


class RetrieveMixinViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Mixin для Ingredient и Tag"""
    pagination_class = None
    filter_backends = [DjangoFilterBackend, ]
    search_fields = ('name',)


class IngredientViewSet(RetrieveMixinViewSet):
    """Реализация операций модели Ingredient"""

    queryset = Ingredient.objects.all()
    serializer_class = IngridientSerializer
    filterset_class = IngredientFilter


class TagViewSet(RetrieveMixinViewSet):
    """Реализация операций модели Tag"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Реализация операций модели Recipes"""

    queryset = Recipes.objects.all()
    pagination_class = MyCustomPagination
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter

    def get_serializer_class(self):

        if self.request.method == 'GET':

            return RecipeSerializer

        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(AuthorOrReadOnly,))
    def favorite(self, request, **kwargs):

        recipe = get_object_or_404(self.queryset, id=kwargs['pk'])
        serializer = FaouriteSerializer(
            recipe,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        if request.method == 'POST':

            Favourites.objects.create(user=request.user, recipe=recipe)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':

            Favourites.objects.filter(
                user=request.user,
                recipe=recipe
            ).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(AuthorOrReadOnly,),
        pagination_class=None
    )
    def shopping_cart(self, request, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(self.queryset, id=kwargs['pk'])
        serializer = ShoppingListSerializer(
            recipe,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        if request.method == 'POST':

            ShoppingList.objects.create(user=user, recipe=recipe)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':

            ShoppingList.objects.filter(
                user=request.user,
                recipe=recipe
            ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):

        ingredients = (
            RecipeIngredientsAmount.objects
            .filter(recipes__shopping_list__user=request.user)
            .order_by('ingredient__name')
            .values_list(
                'ingredient__name',
                'amount',
                'ingredient__measurement_unit'
            )
        )

        filename = 'Список покупок: \n\n'
        file_list = {}

        for name, amount, unit in ingredients:

            if name not in file_list:
                file_list[name] = {'amount': amount, 'unit': unit}
            else:
                file_list[name]['amount'] += amount

        for ingredient in file_list:

            filename += ingredient + ' - ' + str(
                file_list[ingredient]['amount']
            ) + ' ' + file_list[ingredient]['unit'] + '.\n'

        return HttpResponse(filename, content_type='text/plain')
