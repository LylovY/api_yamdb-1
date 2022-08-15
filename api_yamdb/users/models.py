from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin'))


class User(AbstractUser):
    username = models.CharField(
        unique=True, max_length=150, verbose_name='Ник пользователя'
    )
    email = models.EmailField(
        unique=True, max_length=254, verbose_name='email'
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    code = models.CharField(max_length=40, blank=True, default=0)
    role = models.CharField(
        max_length=15,
        choices=ROLES,
        default='user',
        verbose_name='Роль пользователя',
    )

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username
