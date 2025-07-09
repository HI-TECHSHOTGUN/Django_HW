from django.db import models
from users.models import User


# Create your models here.


class Product(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование",
        help_text="Введите наименование товара",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание товара"
    )
    photo = models.ImageField(
        upload_to="config/photo",
        blank=True,
        null=True,
        verbose_name="Фото товара",
        help_text="Загрузите фото",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        related_name="catalog",
        verbose_name="Категория",
        null=True,
        blank=True,
    )
    price = models.IntegerField(verbose_name="Цена", help_text="Введите стоимость товара")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_published = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "description", "price"]
        permissions = [
            ('can_unpublish_product', 'Can unpublish product'),
            ('delete_any_product', 'Can delete any product')
        ]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
