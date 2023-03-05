from django.core.validators import MinValueValidator
from django.db import models
from foodgram.constants import (MINIMUM_COOCING_TIME_IN_MINUTES,
                                MINIMUM_RECIPE_INGREDIENTS_AMOUNT)
from users.models import User

ORANGE = '#E26C2D'
GREEN = '#49B64E'
PURPLE = '#8775D2'


class Tag(models.Model):
    """Описание модели Тег"""

    COLOR = (
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зелёный'),
        (PURPLE, 'Фолетовый'),
    )

    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        blank=False
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=7,
        choices=COLOR
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=200,
        unique=True
    )

    class Meta:

        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Описание модели Ингрдиенты"""

    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=200,
        blank=False,
        null=False
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient',
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipes(models.Model):
    """Модель Рецепты"""

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True
    )
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=200,
        help_text='Название блюда',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Текст рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время (мин.)',
        help_text='Время приготовления (в мин.)',
        default=1,
        validators=[
            MinValueValidator(
                MINIMUM_COOCING_TIME_IN_MINUTES,
                message='Время приготовления не может быть меньше минуты!'
            )
        ]
    )

    class Meta:

        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'

    def __str__(self):
        return self.name


class RecipeIngredientsAmount(models.Model):
    """Описание модели Количество ингридиентов"""

    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Название блюда',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Название ингредиента',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиентов',
        default=1,
        validators=[
            MinValueValidator(
                MINIMUM_RECIPE_INGREDIENTS_AMOUNT,
                message='Укажите хотя бы 1 ингридиент!'
            ),
        ]
    )

    class Meta:

        ordering = ['recipes']
        verbose_name = 'Количество ингридиентов'
        verbose_name_plural = 'Количество ингридиентов'

    def __str__(self):
        return f'{self.ingredient}, {self.amount}'


class Favourites(models.Model):
    """Описание модели Избранное"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Название рецепта',
    )

    class Meta:

        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        default_related_name = 'favourites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite',
            )
        ]

    def __str__(self):
        return f'{self.user} -> {self.recipe}'


class ShoppingList(models.Model):
    """Описание модели Список покупок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Мой список',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Спиок рецептов',
    )

    class Meta:

        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        default_related_name = 'shopping_list'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_list',
            )
        ]

    def __str__(self):
        return f'{self.user} -> {self.recipe}'
