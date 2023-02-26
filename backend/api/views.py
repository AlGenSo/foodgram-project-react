from api.filters import IngredientFilter, RecipesFilter
from api.pagination import MyCustomPagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (IngridientSerializer,
                             NoneIngredientsRecipeSerializer,
                             RecipeCreateSerializer, RecipeSerializer,
                             SubscriptionsSerializer, TagSerializer,
                             UsersListSerializer)
from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from recipes.models import (Favourites, Ingredient, RecipeIngredientsAmount,
                            Recipes, ShoppingList, Tag)
from rest_framework import pagination, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Subscription, User


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
        user = self.request.user
        author = get_object_or_404(self.queryset, id=id)
        serializer = SubscriptionsSerializer(author)
        if request.method == 'POST':
            if Subscription.objects.filter(
                    user=request.user,
                    author=author).exists():
                raise ValidationError(
                    'Вы уже подписаны на автора')
            if user == author:
                raise ValidationError(
                    'Нельзя подписываться на самого себя!')
            Subscription.objects.create(
                user=user,
                author=author)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            in_subscrabed = Subscription.objects.filter(
                user=request.user,
                author=author).exists()
            if in_subscrabed is False:
                raise ValidationError("Вы не были подписаны на автора!")
        Subscription.objects.filter(
            user=request.user,
            author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False)
    def subscriptions(self, request):
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        pages = self.paginate_queryset(
            User.objects.filter(blogger__user=self.request.user)
        )
        serializer = SubscriptionsSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Реализация операций модели Ingredient"""

    queryset = Ingredient.objects.all()
    serializer_class = IngridientSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = IngredientFilter
    search_fields = ('name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Реализация операций модели Tag"""

    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, ]
    search_fields = ('name',)


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
        user = self.request.user
        recipe = get_object_or_404(self.queryset, id=kwargs['pk'])
        serializer = NoneIngredientsRecipeSerializer(recipe)
        if request.method == 'POST':
            if Favourites.objects.filter(
                    user=request.user, recipe=recipe).exists():
                raise ValidationError('Рецепт уже в добален в избранное!')
            Favourites.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            in_subscribed = Favourites.objects.filter(
                user=request.user, recipe=recipe).exists()
            if in_subscribed is False:
                raise ValidationError("В избранном нет такого рецепта!")
        Favourites.objects.filter(user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,),
        pagination_class=None
    )
    def shopping_cart(self, request, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(self.queryset, id=kwargs['pk'])
        serializer = NoneIngredientsRecipeSerializer(recipe)
        if request.method == 'POST':
            if ShoppingList.objects.filter(
                    user=request.user, recipe=recipe).exists():
                raise ValidationError('Рецепт уже в списке покупок!')
            ShoppingList.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            in_shopping_list = ShoppingList.objects.filter(
                user=request.user, recipe=recipe).exists()
            if in_shopping_list is False:
                raise ValidationError("Рецепт удален из списка покупок!")
        ShoppingList.objects.filter(user=request.user, recipe=recipe).delete()
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
            .values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list(
                'ingredient__name',
                'ingredient__measurement_unit',
                'total_amount'
            )
        )

        filename = 'shopping_list.txt'

        file_list = []

        [
            file_list.append(
                # '{} - {} {}.'
                '{} ({}.) - {}'
                .format(*ingredient)) for ingredient in ingredients
        ]

        file = HttpResponse(
            'Список покупок: \n' + '\n'.join(file_list),
            content_type='text/plain'
        )

        file['Content-Disposition'] = (f'attachment; filename={filename}')

        return file
