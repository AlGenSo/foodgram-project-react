from django.contrib import admin

from .models import (Favourites, Ingredient, RecipeIngredientsAmount, Recipes,
                     ShoppingList, Tag)

admin.site.site_header = 'Управление сайтом Foodgram'
admin.site.site_title = 'Администратор сайта'


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
        'count',
        'cooking_time'
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
    count.short_description = 'Рецепта в избранном'


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
