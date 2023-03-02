# Generated by Django 3.2.18 on 2023-03-02 18:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0008_alter_tag_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favourites',
            options={'default_related_name': 'favourites', 'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='shoppinglist',
            options={'default_related_name': 'shopping_list', 'verbose_name': 'Список покупок', 'verbose_name_plural': 'Список покупок'},
        ),
        migrations.AlterField(
            model_name='favourites',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='recipes.recipes', verbose_name='Название рецепта'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='favourites',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='users.user', verbose_name='Пользователь'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to='recipes.recipes', verbose_name='Спиок рецептов'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to='users.user', verbose_name='Мой список'),
            preserve_default=False,
        ),
    ]