from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    account_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    role_choices = [
        ('admin', 'Admin'),
        ('meter_reader', 'Meter Reader'),
        ('resident', 'Resident')
    ]
    role = models.CharField(max_length=20, choices=role_choices, default='resident')
    groups = models.ManyToManyField(
        'auth.Group', related_name='custom_user_groups', blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
    )

    def __str__(self):
        return self.username