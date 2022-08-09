from django.core.validators import MinLengthValidator
from django.db import models

from users.models import User


class Review(models.Model):
    CHOICES_SCORE = [(i, i) for i in range(1, 11)]

    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        validators=[MinLengthValidator(1, 'Пустое поле')]
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка произведения от 1 до 10',
        choices=CHOICES_SCORE,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата написания отзыва',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь'
    )
    text = models.TextField(
        verbose_name='Комментарий к отзыву',
        validators=[MinLengthValidator(1, 'Пустое поле')]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата написания отзыва',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
