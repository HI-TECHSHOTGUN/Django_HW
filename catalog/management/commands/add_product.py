from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Add new product'

    def handle(self, *args, **options):
        categories, _ = Category.objects.get_or_create(name='Овощи', description='Разные овощи поставкой из 32 стран')

        product = [{'name': 'Морковь', 'description': 'Рыжая морковь', 'category': categories, 'price': '90',
                                           'created_at': '2025-05-30', 'updated_at': '2025-05-30'},
                   {'name': 'Картофель', 'description': 'Картофель Белорусский', 'category': categories, 'price': '70',
                    'created_at': '2025-05-30', 'updated_at': '2025-05-30'},
                   ]

        for product_data in product:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.name}'))

            else:
                self.stdout.write(self.style.WARNING(f'Product already exist: {product.name}'))