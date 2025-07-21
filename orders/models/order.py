from django.db import models
from users.models.user import User
from brandpanel.models.branch import Branch

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    guest_first_name = models.CharField(max_length=100, blank=True, null=True)
    guest_last_name = models.CharField(max_length=100, blank=True, null=True)
    guest_email = models.EmailField(blank=True, null=True)
    guest_phone = models.CharField(max_length=20, blank=True, null=True)

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
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='orders')
    def __str__(self):
        return f"Order #{self.id} by {self.user if self.user else self.guest_email}"
    
@property
def payment_status(self):
    if self.payment_method == 'cod':
        return 'Pending'
    return 'Paid' if self.is_paid else 'Unpaid'

