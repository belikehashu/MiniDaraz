from django.db import models
from users.models.user import User

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    shipping_address = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    payment_method = models.CharField(max_length=20, choices=[
        ('cod', 'Cash on Delivery'),
        ('stripe', 'Stripe'),
        ('jazzcash', 'JazzCash'),
        ('easypaisa', 'EasyPaisa'),
    ], default='cod')

    is_paid = models.BooleanField(default=False)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"
