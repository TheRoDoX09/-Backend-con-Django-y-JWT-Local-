from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')

    USERNAME_FIELD = 'email'
    # El manual deja esta lista vacía, pero createsuperuser necesita el username
    # que exige AbstractUser; sin él falla con TypeError.
    REQUIRED_FIELDS = ['username']
