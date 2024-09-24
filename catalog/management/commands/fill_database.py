from django.core.management import BaseCommand
from catalog.models import Product, Category
import json


class Command(BaseCommand):
    @staticmethod
    def json_read_categories():
        """Читает данные категорий из JSON-файла."""
        with open('data_category.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def json_read_products():
        """Читает данные продуктов из JSON-файла."""
        with open('data_product.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def handle(self, *args, **options):
        # Удаляем все существующие продукты и категории
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создаем списки для хранения объектов
        category_for_create = []
        product_for_create = []

        # Обрабатываем данные категорий из JSON и создаем словарь для сопоставления индексов с названиями
        category_index_mapping = {}
        for category_data in self.json_read_categories():
            fields = category_data['fields']
            category = Category(
                name=fields['name'],
                description=fields['description']
            )
            category_for_create.append(category)
            category_index_mapping[category_data['pk']] = fields['name']

        # Сохраняем категории в базу данных
        Category.objects.bulk_create(category_for_create)

        # Создаем словарь для сопоставления названий категорий с объектами категорий
        category_objects = {category.name: category for category in Category.objects.all()}

        # Обрабатываем данные продуктов из JSON и создаем объекты продуктов
        for product_data in self.json_read_products():
            fields = product_data['fields']
            category_name = category_index_mapping.get(fields['category'])
            product = Product(
                name=fields['name'],
                description=fields['description'],
                image=fields['image'],
                category=category_objects.get(category_name),
                price=fields['price'],
                created_at=fields['created_at'],
                updated_at=fields['updated_at']
            )
            product_for_create.append(product)

        # Сохраняем продукты в базу данных
        Product.objects.bulk_create(product_for_create)
