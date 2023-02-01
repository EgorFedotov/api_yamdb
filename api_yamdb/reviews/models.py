from django.db import models


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)