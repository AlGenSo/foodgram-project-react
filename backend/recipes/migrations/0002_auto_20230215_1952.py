# Generated by Django 2.2.19 on 2023-02-15 16:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglist',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to=settings.AUTH_USER_MODEL, verbose_name='Мой список'),
        ),
        migrations.AddField(
            model_name='recipes',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AddField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(help_text='Распишите ингредиенты', related_name='recipes', to='recipes.Ingredient', verbose_name='ингридиенты'),
        ),
        migrations.AddField(
            model_name='recipes',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='Тег'),
        ),
        migrations.AddField(
            model_name='recipeingredientsamount',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Ingredient', verbose_name='Название ингредиента'),
        ),
        migrations.AddField(
            model_name='recipeingredientsamount',
            name='recipes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_amount', to='recipes.Recipes', verbose_name='Название блюда'),
        ),
        migrations.AddField(
            model_name='favourites',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='recipes.Recipes', verbose_name='Название рецепта'),
        ),
        migrations.AddField(
            model_name='favourites',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AddConstraint(
            model_name='shoppinglist',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopping_list'),
        ),
        migrations.AddConstraint(
            model_name='favourites',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favourite'),
        ),
    ]
