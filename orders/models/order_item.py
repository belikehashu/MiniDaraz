from django.db import models
from products.models.product import Product
from .order import Order

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', null=True, blank=True)
    quantity = models.PositiveIntegerField()
