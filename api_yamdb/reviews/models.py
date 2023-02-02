from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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
    pud_date = models.DateTimeField(
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

    def __str__(self) -> str:
        return f'Комментарий {self.author} к {self.review}'
