# Generated by Django 3.2.18 on 2023-03-04 22:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20230304_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(default=1, help_text='Время приготовления (в мин.)', validators=[django.core.validators.MinValueValidator(1, message='Время приготовления не может быть меньше минуты!')], verbose_name='Время приготовления в минутах'),
        ),
        migrations.AlterUniqueTogether(
            name='ingredient',
            unique_together={('name', 'measurement_unit')},
        ),
    ]
