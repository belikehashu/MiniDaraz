from django.db import models
from users.models.user import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
