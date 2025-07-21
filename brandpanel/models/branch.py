from django.db import models
from brandpanel.models.brand import Brand
from managerpanel.models.manager import Manager 

class Branch(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    managers = models.ManyToManyField(Manager, blank=True, related_name='branches')

    def __str__(self):
        return f"{self.name} - {self.brand.name}"
