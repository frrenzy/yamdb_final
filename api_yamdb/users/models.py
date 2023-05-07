from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserRole(models.TextChoices):
        USER = 'user', 'user'
        MODERATOR = 'moderator', 'moderator'
        ADMIN = 'admin', 'admin'

    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=9,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
