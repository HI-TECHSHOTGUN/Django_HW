from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Del all products and categories'

    def handle(self, *args, **kwargs):
        # Удаляем все продукты
        product_count, _ = Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено продуктов: {product_count}'))

        # Удаляем все категории
        category_count, _ = Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено категорий: {category_count}'))


