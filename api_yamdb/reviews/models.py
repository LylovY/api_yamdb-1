from core.models import CreatedModel

from django.conf import settings
from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator)
from django.db import models
from django.utils import timezone

from users.models import User


class Review(CreatedModel):

    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        validators=[MinLengthValidator(1, 'Пустое поле')],
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка произведения от 1 до 10',
        validators=[MinValueValidator(1, 'Минимальная оценка 1'),
                    MaxValueValidator(10, 'Максимальная оценка 10')],
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text[:settings.NUMBER_SYMBOL_TEXT]


class Comment(CreatedModel):
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь',
    )
    text = models.TextField(
        verbose_name='Комментарий к отзыву',
        validators=[MinLengthValidator(1, 'Пустое поле')],
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:settings.NUMBER_SYMBOL_TEXT]


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(
        validators=[MaxValueValidator(timezone.now().year)]
    )
    description = models.TextField()
    genre = models.ManyToManyField('Genre')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
    )

    def __str__(self):
        return self.name
