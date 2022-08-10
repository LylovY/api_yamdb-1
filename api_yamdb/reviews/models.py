from django.core.validators import MaxValueValidator, MinLengthValidator
from django.db import models
from django.utils import timezone
from users.models import User


CHOICES_SCORE = [(i, i) for i in range(1, 11)]


class Review(models.Model):

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
        validators=[MaxValueValidator(timezone.now().year)])
    rating = models.IntegerField(null=True)
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
