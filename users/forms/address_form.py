from django import forms
from users.models.address import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'zip_code', 'country']
