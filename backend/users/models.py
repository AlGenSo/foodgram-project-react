from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель User"""

    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=150,
        blank=False,
        null=False,
    )
    is_superuser = models.BooleanField(
        verbose_name='Админ',
        default=False
    )

    class Meta:

        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'

    def __str__(self):

        return str(self.username)

    @property
    def is_admin(self):

        return self.is_superuser
