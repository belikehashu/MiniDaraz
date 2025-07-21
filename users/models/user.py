from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'customer', 'Customer'
        OWNER = 'owner', 'Owner'
        MANAGER = 'manager', 'Manager'

    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email
