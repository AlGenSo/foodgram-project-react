# Generated by Django 3.2.18 on 2023-02-24 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230217_2333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipes',
            old_name='CookingTimeInMinutes',
            new_name='cooking_time',
        ),
    ]
