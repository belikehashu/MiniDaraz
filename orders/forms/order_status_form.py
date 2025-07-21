from django import forms
from orders.models.order import Order

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
