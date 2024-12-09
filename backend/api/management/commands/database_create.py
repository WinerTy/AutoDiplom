import random

from django.core.management.base import BaseCommand

from database.models import (
    AutoPart,
    AutoMark,
    Atribute,
    AutoPartCharacteristic,
    Category,
)
from .utils import car_brands, attribute, values, auto_parts, categories


class CategoryCreator:
    def __init__(self, count: int = 10):
        self.count = count
        self.categories = categories

    def create(self):
        try:
            for i in range(self.count):
                Category.objects.create(name=self.categories[i])
        except Exception as e:
            print(f"Error: {e}")


class AutoMarkCreator:
    def __init__(self, count: int = 10):
        self.count = count
        self.names = car_brands

    def create(self):
        try:
            for i in range(self.count):
                AutoMark.objects.create(name=self.names[i])
        except Exception:
            pass


class AtributeCreator:
    def __init__(self, count: int = 10):
        self.count = count
        self.names = attribute
        self.values = values

    def create(self):
        try:
            for i in range(self.count):
                Atribute.objects.create(name=self.names[i])
        except Exception as e:
            print(f"Error: {e}")


class AutoPartCreator:
    def __init__(self, count: int = 10):
        self.count = count
        self.data = auto_parts
        self.values = values

    def get_random_mark(self):
        return AutoMark.objects.order_by("?").first()

    def get_random_attribute(self):
        return Atribute.objects.order_by("?").first()

    def get_random_attribute_value(self):
        return random.choice(self.values)

    def get_random_category(self):
        return Category.objects.order_by("?").first()

    def create(self):
        try:
            for i in range(len(self.data)):
                detail = AutoPart.objects.create(
                    name=self.data[i]["name"],
                    category=self.get_random_category(),
                    description=self.data[i]["description"],
                    price=self.data[i]["price"],
                    mark=self.get_random_mark(),
                    count=self.data[i]["count"],
                )
                for j in random.sample(range(1, 5), 3):
                    AutoPartCharacteristic.objects.create(
                        auto_part=detail,
                        atribute=self.get_random_attribute(),
                        value=self.get_random_attribute_value(),
                    )
            pass

        except Exception as e:
            print(f"Error: {e}")


class Command(BaseCommand):

    def handle(self, *args, **options):

        category_creator = CategoryCreator()
        category_creator.create()

        mark_creator = AutoMarkCreator(30)
        mark_creator.create()

        atribute_creator = AtributeCreator()
        atribute_creator.create()

        aoto_part_creator = AutoPartCreator()
        aoto_part_creator.create()
        print("Database data created")
