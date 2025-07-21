from django.db import models
from brandpanel.models.owner import Owner

class Brand(models.Model):
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
