# Generated by Django 3.2.18 on 2023-03-02 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20230302_2113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipes',
            options={'default_related_name': 'recipes', 'ordering': ('-pub_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Ingredient', verbose_name='ингридиенты'),
        ),
    ]
