import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from foodgram.constants import (MINIMUM_COOCING_TIME_IN_MINUTES,
                                MINIMUM_RECIPE_INGREDIENTS_AMOUNT)
from recipes.models import (Favourites, Ingredient, RecipeIngredientsAmount,
                            Recipes, ShoppingList, Tag)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import Subscription

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    """Преобразование данных класса User
        Создание нового пользователя"""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UsersListSerializer(UserSerializer):
    """Преобразование списка пользователей"""

    is_subscribed = serializers.SerializerMethodField()
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()

    class Meta:

        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):

        request = self.context.get('request')
        if not request or request.user.is_anonymous:

            return False

        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()


class Base64ImageField(serializers.ImageField):
    """Преобразование данных
        Кастомное поле для картинки"""

    def to_internal_value(self, data):

        if isinstance(data, str) and data.startswith('data:image'):

            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super(Base64ImageField, self).to_internal_value(data)


class NoneIngredientsRecipeSerializer(serializers.ModelSerializer):
    """Преобразование данных
        Рецепт без ингредиента"""

    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionsSerializer(UsersListSerializer):
    """Преобразование данных
        Мои подписки"""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def validate(self, data):

        request = self.context['request']
        author = self.instance

        if request.method == 'POST':
            if Subscription.objects.filter(
                    user=request.user,
                    author=author).exists():
                raise ValidationError('Вы уже подписаны на автора')
            if request.user == author:
                raise ValidationError(
                    {'detail': 'Нельзя подписываться на самого себя!'}
                )

            return data

        if request.method == 'DELETE':

            if not Subscription.objects.filter(
                    user=request.user,
                    author=author).exists():
                raise ValidationError(
                    {'detail': 'Вы не были подписаны на автора!'}
                )

        return data

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        recipes = Recipes.objects.filter(author=obj).all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = NoneIngredientsRecipeSerializer(
            recipes, many=True, read_only=True,
            context={'request': request}
        )
        return serializer.data

    def get_is_subscribed(self, obj):

        try:
            return Subscription.objects.filter(
                user=self.context.get('request'),
                blogger_id=obj.id
            ).exists()

        except Exception:

            return False

    def get_recipes_count(self, obj):

        return obj.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    """Преобразование данных
        Список тегов"""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngridientSerializer(serializers.ModelSerializer):
    """Преобразование данных
        Список ингредиентов"""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Преобразование данных
        Добавление поля 'количество ингридиентов' """

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredientsAmount
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Преобразование данных
        Получение списка рецептов"""

    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UsersListSerializer(many=False, read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        source='recipeingredientsamount_set'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):

        request = self.context.get('request')
        if request.user.is_anonymous or request is None:

            return False

        return Favourites.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):

        request = self.context.get('request')
        if request.user.is_anonymous or request is None:

            return False

        return ShoppingList.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Преобразование данных
        Создание рецепта"""

    image = Base64ImageField(required=True, allow_null=True)
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='id',
        many=True
    )
    ingredients = IngredientAmountSerializer(
        many=True,
        source='recipeingredientsamount_set'
    )
    author = UsersListSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    cooking_time = serializers.IntegerField()

    def validate(self, attrs):
        tags = []

        for tag in attrs['tags']:

            if tag not in tags:
                tags.append(tag)
            else:
                raise serializers.ValidationError(
                    {'tags': 'Тег должен быть уникальным!'}
                )
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Должен быть выбран хотя бы один тег!'}
            )

        ingredients = []

        for ingredient in attrs['recipeingredientsamount_set']:

            if ingredient['ingredient'] in ingredients:
                raise serializers.ValidationError(
                    {'ingredients': 'Ингредиент должен быть уникальным!'}
                )
            ingredients.append(ingredient['ingredient'])

            if int(ingredient['amount']) < MINIMUM_RECIPE_INGREDIENTS_AMOUNT:
                raise serializers.ValidationError(
                    {'amount': 'Мера объёма|веса не может быть меньше 1!'}
                )
        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients': 'Укажите хотя бы 1 ингридиент!'}
            )
        if int(attrs['cooking_time']) < MINIMUM_COOCING_TIME_IN_MINUTES:
            raise serializers.ValidationError(
                {'cooking_time': 'Минимальное время приготовления 1 минута!'}
            )

        return attrs

    def create(self, validated_data):

        tag_data = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredientsamount_set')
        recipes = Recipes.objects.create(**validated_data)
        recipes.tags.set(tag_data)
        self.recipes_ingredients_add(ingredients, recipes)

        return recipes

    def update(self, instance, validated_data):

        instance.tags.clear()
        RecipeIngredientsAmount.objects.filter(recipes=instance).delete()
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        ingredients = validated_data.pop('recipeingredientsamount_set')
        self.recipes_ingredients_add(ingredients, instance)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data

    @staticmethod
    def recipes_ingredients_add(ingredients, recipes):

        for ingredient in ingredients:
            current_ingredient = (
                Ingredient.objects.get(id=ingredient['ingredient']['id'])
            )
            RecipeIngredientsAmount.objects.create(
                ingredient=current_ingredient,
                recipes=recipes,
                amount=ingredient['amount']
            )

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'image',
            'name',
            'text',
            'cooking_time'
        )


class FaouriteSerializer(NoneIngredientsRecipeSerializer):
    """Сериализация подписок"""

    def validate(self, data):
        request = self.context['request']
        recipe = self.instance

        if request.method == 'POST':
            if Favourites.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                raise serializers.ValidationError(
                    {'detail': 'Рецепт уже в избранном!'}
                )

        if not request.method == "DELETE":
            if Favourites.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                raise serializers.ValidationError(
                    {'detail': 'Рецепта нет в избранном!'}
                )

        return data


class ShoppingListSerializer(NoneIngredientsRecipeSerializer):
    """Сериализация спасика покупок"""

    def validate(self, data):
        request = self.context['request']
        recipe = self.instance

        if request.method == 'POST':
            if ShoppingList.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                raise serializers.ValidationError(
                    {'detail': 'Рецепт уже в спике покупок!'}
                )

        if request.method == 'DELETE':
            if ShoppingList.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists() is False:
                raise serializers.ValidationError(
                    {'detail': 'Рецепта нет в избранном!'}
                )

        return data
