from django.db import models
from django.conf import settings

class Manager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.email
