from django.db import models
from brandpanel.models.branch import Branch

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='categories')
    def __str__(self):
        return self.name
