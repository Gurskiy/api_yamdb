from django.db import models

from .validators import validate_year


class Category(models.Model):
    """Модель категории"""
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Дайте название категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Адрес для страницы категории',
        help_text=(
            'Укажите адрес для страницы категории. '
            'Используйте только латиницу, цифры, '
            'дефисы и знаки подчёркивания'
        )
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Genre(models.Model):
    """Модель жанр"""
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Дайте название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Адрес для страницы жанра',
        help_text=(
            'Укажите адрес для страницы жанра. '
            'Используйте только латиницу, цифры, '
            'дефисы и знаки подчёркивания'
        )
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    """Модель произведения"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения',
        help_text='Дайте название произведению'
    )
    year = models.IntegerField(
        validators=[validate_year],
        verbose_name='Год',
        help_text='Укажите год произведения'
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание произведения',
        help_text='Укажите описание произведения.'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        related_name='titles',
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']


class GenreTitle(models.Model):
    """Связующая модель жанра и произведения."""
    genre = models.ForeignKey(
        Genre,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    def __str__(self):
        return f'{self.title}, жанр: {self.genre}'
