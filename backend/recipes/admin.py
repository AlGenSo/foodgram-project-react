from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Sum

from .models import (Favourites, Ingredient, RecipeIngredientsAmount, Recipes,
                     ShoppingList, Tag)

admin.site.site_header = 'Управление сайтом Foodgram'
admin.site.site_title = 'Администратор сайта'

admin.site.unregister(Group)


class IngredientInline(admin.TabularInline):

    model = RecipeIngredientsAmount
    extra = 0
    min_num = 1


class FauoritesInline(admin.TabularInline):

    model = Favourites
    extra = 0


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}

    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    list_editable = (
        'name',
        'color',
        'slug'
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
        'list_ingredients',
        'count'
    )
    list_editable = (
        'author',
        'name',
        'cooking_time',
        'image'
    )
    filter_horizontal = ('tags', 'ingredients',)
    inlines = (IngredientInline, FauoritesInline)
    list_filter = (
        'author',
        'name',
        'tags'
    )

    def count(self, obj):

        return Favourites.objects.filter(recipe=obj).count()
    count.short_description = 'В избранном'

    def list_ingredients(self, obj):

        ingredients = (
            RecipeIngredientsAmount.objects
            .filter(recipes=obj)
            .order_by('ingredient__name').values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list(
                'ingredient__name',
                'ingredient__measurement_unit',
                'total_amount'

            )
        )
        ingredient_list = []
        [ingredient_list.append('{} ({}.) - {}'.format(*ingredient))
         for ingredient in ingredients]

        return ingredient_list

    list_ingredients.short_description = 'Ингредиенты'


@admin.register(Favourites)
class FavouritesAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'recipe'
    )
    list_filter = (
        'recipe',
    )


@admin.register(ShoppingList)
class ShoppingListADmin(admin.ModelAdmin):

    list_display = (
        'user',
        'recipe'
    )
    list_filter = (
        'recipe',
    )
