from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Recipes, Tag


class IngredientFilter(FilterSet):
    """Поиск ингредиента по полю name регистронезависимо
        начиная с указанного значения"""

    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipesFilter(FilterSet):
    """Фильтрация по:
        тегам, в избранном, в списке покупок"""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='get_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart',
    )

    class Meta:
        model = Recipes
        fields = (
            'tags',
            'author',
        )

    def get_favorited(self, queryset, name, value):

        if value and not self.request.user.is_anonymous:

            return queryset.filter(favourites__user=self.request.user)

        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):

        if value and not self.request.user.is_anonymous:

            return queryset.filter(shopping_list__user=self.request.user)

        return queryset
