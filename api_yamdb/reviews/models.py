from django.db import models


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.PositiveSmallIntegerField()
    # rating = TODO: review.score 
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        related_name='titles',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.DO_NOTHING,
        related_name='titles'
    )
