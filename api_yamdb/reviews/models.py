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
        on_delete=models.DO_NOTHING,
        related_name='titles',
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        null=False,
        related_name='titles',
        on_delete=models.DO_NOTHING
    )

    title = models.ForeignKey(
        Title,
        null=False,
        related_name='genres',
        on_delete=models.DO_NOTHING
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('genre', 'title'),
                                    name='constraint_pair')
        ]
