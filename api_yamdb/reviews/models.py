from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

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
        validators=(validate_username,),
        max_length=150,
        unique=True
    )

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True
    )

    first_name = models.TextField(
        verbose_name='Имя',
        max_length=150,
        null=True,
        blank=True
    )

    last_name = models.TextField(
        verbose_name='Фамилия',
        max_length=150,
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
        max_length=150,
        choices=ROLES,
        default=USER
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username


class Category(models.Model):
    """Катерогии произведений."""
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(2100, 'Год еще не наступил'),
            MinValueValidator(600, 'Минимальное значение 600'),
        ],
    )
    #rating = TODO: review.score
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None
    )
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
        verbose_name='Жанр'
    )


class GenreTitle(models.Model):
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
    """Модель отзыва."""
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
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    text = models.TextField(

    )
    score = models.IntegerField(
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
    """Модель комментария."""
    text = models.TextField(
        verbose_name='текст комментария',
        help_text='введите текст комментария',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
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
