from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True, blank=False,
                              null=False)
    username = models.CharField(max_length=150, unique=True, blank=False,
                                null=False)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    password = models.CharField(max_length=150, blank=False, null=False)

    class Meta:
        ordering = ['id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        default_related_name = 'user'

    def __str__(self):
        return self.username
