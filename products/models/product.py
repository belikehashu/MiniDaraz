from django.db import models
from .category import Category
from products.services.stock_notification_service import handle_stock_notification

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        old_stock = None
        if self.pk:
            old = Product.objects.filter(pk=self.pk).first()
            if old:
                old_stock = old.stock

        super().save(*args, **kwargs)

        if old_stock is not None and old_stock != self.stock:
            handle_stock_notification(product=self, old_stock=old_stock)

    def __str__(self):
        return self.name
