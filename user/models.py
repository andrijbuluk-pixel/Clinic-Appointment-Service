from django.contrib.auth.models import AbstractUser, UserManager

from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
