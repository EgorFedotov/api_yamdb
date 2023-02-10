from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_username
from api_yamdb.settings import LENGHT_USER_FIELD

from .validators import validate_username


class User(AbstractUser):
    '''Модель юзера.'''
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        validators=(validate_username, UnicodeUsernameValidator()),
        max_length=LENGHT_USER_FIELD,
        unique=True
    )

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True
    )

    first_name = models.TextField(
        verbose_name='Имя',
        max_length=LENGHT_USER_FIELD,
        null=True,
        blank=True
    )

    last_name = models.TextField(
        verbose_name='Фамилия',
        max_length=LENGHT_USER_FIELD,
        null=True,
        blank=True,
    )

    bio = models.TextField(
        verbose_name='Биография',
        null=True,
        blank=True
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=LENGHT_USER_FIELD,
        choices=ROLES,
        default=USER
    )

    @property
    def is_moderator(self):
        return self.is_staff or self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            ),
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="username_is_not_me"
            )
        ]

    def __str__(self):
        return self.username


class CommonGroupModel(models.Model):
    '''Общий родетельский класс для наследования.'''
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Category(CommonGroupModel):
    '''Катерогии произведений.'''
    pass


class Genre(CommonGroupModel):
    '''Модель жанра.'''
    pass


class Title(models.Model):
    '''Модель произведения.'''
    name = models.CharField('Название', max_length=256)
    year = models.PositiveSmallIntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанры'
    )


class GenreTitle(models.Model):
    '''Связанная модель жанра и заголовка.'''
    genre = models.ForeignKey(
        Genre,
        null=True,
        related_name='titles',
        on_delete=models.SET_NULL
    )

    title = models.ForeignKey(
        Title,
        null=True,
        related_name='genres',
        on_delete=models.SET_NULL
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('genre', 'title'),
                                    name='constraint_pair')
        ]


class Review(models.Model):
    '''Модель отзыва.'''
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    text = models.TextField()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',

    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(10, 'Оценка не может быть выше 10'),
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
        ],
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return f'Отзыв {self.text} оставлен на {self.title}'


class Comment(models.Model):
    '''Модель комментария.'''
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    def __str__(self):
        return f'Комментарий {self.author} к {self.review}'
