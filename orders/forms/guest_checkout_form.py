from django import forms

class GuestCheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)

    guest_address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=20)
    province = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)

    payment_method = forms.ChoiceField(choices=[
        ('stripe', 'Stripe'),
    ])
