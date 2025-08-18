from .models import Product, Category


class ProductService:

    @staticmethod
    def get_products_by_category(category_name):
        """
        Возвращает опубликованные продукты для указанной категории,
        игнорируя регистр букв в названии.
        """
        try:
            category = Category.objects.get(name__iexact=category_name)
            return Product.objects.filter(category=category, is_published=True)

        except Category.DoesNotExist:
            return Product.objects.none()
