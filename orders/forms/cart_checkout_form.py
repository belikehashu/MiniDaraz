from django import forms

class CartCheckoutForm(forms.Form):
    address = forms.ChoiceField(label="Select Delivery Address")

    def __init__(self, *args, **kwargs):
        addresses = kwargs.pop('addresses', [])
        super().__init__(*args, **kwargs)
        self.fields['address'].choices = [
            (addr.id, f"{addr.street}, {addr.city}, {addr.country} - {addr.zip_code}")
            for addr in addresses
        ]
