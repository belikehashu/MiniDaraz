from django.db import models
from brandpanel.models.branch import Branch
from products.models.product import Product

class GuestOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    home_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    total_price = models.FloatField()
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=[
        ('stripe', 'Stripe'),
    ])
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')  # ✅ Added line
    created_at = models.DateTimeField(auto_now_add=True)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='guest_orders')

    def __str__(self):
        return f"GuestOrder #{self.id} - {self.first_name} {self.last_name}"


class GuestOrderItem(models.Model):
    order = models.ForeignKey(GuestOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (Guest Order #{self.order.id})"
