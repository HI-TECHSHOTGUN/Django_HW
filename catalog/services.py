from .models import Product, Category


class ProductService:

    @staticmethod
    def get_products_by_category(category_name):
        try:
            category = Category.objects.get(name=category_name)
            return Product.objects.filter(category=category, is_published=True)
        except Category.DoesNotExist:
            return []
