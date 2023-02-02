from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Модель юзера.'''
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True,
        unique=True
    )

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
    )

    first_name = models.TextField(
        max_length=150,
    )

    last_name = models.TextField(
        max_length=150,
    )

    bio = models.TextField(
        verbose_name='Биография',
        null=True,
        blank=True
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
