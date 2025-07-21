from django import forms
from orders.models.guest_order import GuestOrder

class GuestOrderStatusForm(forms.ModelForm):
    class Meta:
        model = GuestOrder
        fields = ['status']
