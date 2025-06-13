from django.db import models

# Create your models here.

class BlogPost(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Заголовок",
        help_text="Введите заголовок",
    )
    description = models.TextField(
        verbose_name="Содержимое", help_text="Введите содержимое"
    )
    photo = models.ImageField(
        upload_to="config/photo",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите фото",
    )
    created_at = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

