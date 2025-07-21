from django import forms

class CartCheckoutForm(forms.Form):
    address = forms.ChoiceField(label="Select Delivery Address")

    payment_method = forms.ChoiceField(choices=[
        ('cod', 'Cash on Delivery'),
        ('stripe', 'Stripe'),
    ])

    def __init__(self, *args, **kwargs):
        addresses = kwargs.pop('addresses', None)
        super().__init__(*args, **kwargs)

        if addresses:
            self.fields['address'].choices = [
                (addr.id, f"{addr.street}, {addr.city}, {addr.country} - {addr.zip_code}")
                for addr in addresses
            ]
