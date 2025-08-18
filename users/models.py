from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User, где email является уникальным идентификатором
    для аутентификации вместо username.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным email и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Убираем поле username
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(
        max_length=25,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
        help_text="Введите страну",
        blank=True, # Добавлено, чтобы поле не было обязательным в админке
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        help_text="Загрузите аватар",
    )

    # Указываем, что email теперь используется как логин
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # --- НАЧАЛО ИСПРАВЛЕНИЙ ---
    # Привязываем наш кастомный менеджер к модели
    objects = UserManager()
    # --- КОНЕЦ ИСПРАВЛЕНИЙ ---


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email