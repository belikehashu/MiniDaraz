from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models.user import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password1', 'password2']
