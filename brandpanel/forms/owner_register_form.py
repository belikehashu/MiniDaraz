from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models.user import User

class OwnerRegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=20)
    brand_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'owner'  
        if commit:
            user.save()
        return user