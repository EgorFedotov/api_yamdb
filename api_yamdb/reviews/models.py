from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


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
    # rating = TODO: review.score 
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
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
