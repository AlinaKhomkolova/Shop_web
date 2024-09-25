from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to= 'users/', verbose_name='Аватарка', **NULLABLE)
    side = models.CharField(max_length=50, verbose_name='Страна' ,**NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []