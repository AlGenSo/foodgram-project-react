import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag

PATH_INGREDIENT_CSV = '/app/data/ingredients.csv'
PATH_TAGS_CSV = '/app/data/tags.csv'


class Command(BaseCommand):
    help = 'Загрузка csv в ДТ'

    def handle(self, *args, **options):

        with open(PATH_INGREDIENT_CSV, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for name, measurement_unit in reader:
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement_unit
                )
        self.stdout.write(
            'Данные из списка ингредиентов загружены '
            + str(Ingredient.objects.all().count())
        )

        with open(PATH_TAGS_CSV, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for name, color, slug in reader:
                Tag.objects.get_or_create(
                    name=name,
                    color=color,
                    slug=slug
                )
        self.stdout.write('Данные из списка тегов загружены')
