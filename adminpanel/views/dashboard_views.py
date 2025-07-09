from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_superadmin(user):
    return user.is_superuser

@user_passes_test(is_superadmin)
def dashboard(request):
    return render(request, 'adminpanel/dashboard.html')
