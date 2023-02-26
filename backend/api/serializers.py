import base64
from collections import OrderedDict

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import (Favourites, Ingredient, RecipeIngredientsAmount,
                            Recipes, ShoppingList, Tag)
from rest_framework import serializers
from users.models import Subscription, User


class UsersListSerializer(UserSerializer):
    """Преобразование списка пользователей"""

    is_subscribed = serializers.SerializerMethodField()

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

        if Subscription.objects.filter(
            user=request.user, author=obj
        ).exists():

            return True

        return False


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

    recipes = NoneIngredientsRecipeSerializer(many=True, read_only=False)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
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

    def get_is_subscribed(*args):

        return True

    def get_recipes_count(self, obj):

        return obj.recipes.count()


class SubscribeAuthorSerializer(serializers.ModelSerializer):
    """Преобразование данных
        Подписаться/отписаться от пользователя"""

    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
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

    def validate_subscribe(self, obj):

        if (self.context['request'].user == obj):
            raise serializers.ValidationError({'errors': 'Ошибка подписки.'})

        return obj

    def get_is_subscribed(self, obj):

        return (
            self.context.get('request').user.is_authenticated
            and Subscription.objects.filter(
                user=self.context['request'].user,
                author=obj
            ).exists()
        )

    def get_recipes(self, obj):

        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()

        if limit:
            recipes = recipes[:int(limit)]
        serializer = NoneIngredientsRecipeSerializer(
            recipes, many=True, read_only=True
        )

        return serializer.data

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

    id = serializers.IntegerField()
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredientsAmount
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class CreateRecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор данных количество ингридиентов
        для создания рецепта"""

    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredientsAmount
        fields = (
            'id',
            'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Преобразование данных
        Получение списка рецептов"""

    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UsersListSerializer(many=False, read_only=True)
    ingredients = IngredientAmountSerializer(many=True)
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

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        representation['id'] = instance.id

        representation['ingredients'] = IngredientAmountSerializer(
            RecipeIngredientsAmount.objects.filter(recipes=instance), many=True
        ).data
        representation['tags'] = TagSerializer(
            instance.tags, many=True
        ).data

        representation = OrderedDict([
            ('id', representation['id']),
            ('tags', representation['tags']),
            ('author', representation['author']),
            ('ingredients', representation['ingredients']),
            ('is_favorited', representation['is_favorited']),
            ('is_in_shopping_cart', representation['is_in_shopping_cart']),
            ('image', representation['image']),
            ('name', representation['name']),
            ('text', representation['text']),
            ('cooking_time', representation['cooking_time']),
        ])
        return representation

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
    ingredients = IngredientAmountSerializer(many=True,)
    author = UsersListSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def to_representation(self, instance):
        self.fields.pop('ingredients')
        self.fields.pop('tags')
        representation = super().to_representation(instance)
        representation['id'] = instance.id

        representation['ingredients'] = IngredientAmountSerializer(
            RecipeIngredientsAmount.objects.filter(recipes=instance), many=True
        ).data
        representation['tags'] = TagSerializer(
            instance.tags, many=True
        ).data

        representation = OrderedDict([
            ('id', representation['id']),
            ('tags', representation['tags']),
            ('author', representation['author']),
            ('ingredients', representation['ingredients']),
            ('is_favorited', representation['is_favorited']),
            ('is_in_shopping_cart', representation['is_in_shopping_cart']),
            ('image', representation['image']),
            ('name', representation['name']),
            ('text', representation['text']),
            ('cooking_time', representation['cooking_time']),
        ])
        return representation

    def create(self, validated_data):
        tag_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipes = Recipes.objects.create(**validated_data)
        recipes.tags.set(tag_data)
        for ingredient in ingredients_data:
            current_ingredient = (
                Ingredient.objects.get(id=ingredient['id'])
            )
            RecipeIngredientsAmount.objects.create(
                ingredient=current_ingredient,
                recipes=recipes,
                amount=ingredient['amount']
            )
            recipes.ingredients.add(current_ingredient)

        return recipes

    def update(self, instance, validated_data):
        instance.tags.clear()
        RecipeIngredientsAmount.objects.filter(recipes=instance).delete()
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients')
        for ingredient in ingredients:
            current_ingredient = (
                Ingredient.objects.get(id=ingredient['id'])
            )
            RecipeIngredientsAmount.objects.create(
                ingredient=current_ingredient,
                recipes=instance,
                amount=ingredient['amount']
            )
        return super().update(instance, validated_data)

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
