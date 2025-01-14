# Generated by Django 2.2.19 on 2023-02-17 20:33

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20230215_1952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipes',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AddField(
            model_name='recipes',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 2, 17, 20, 33, 30, 985539, tzinfo=utc), verbose_name='Дата публикации'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='favourites',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Ingredient', verbose_name='ингридиенты'),
        ),
    ]
