from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from managerpanel.models import Manager

def manager_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            try:
                manager = Manager.objects.get(user=user)
                login(request, user)
                return redirect('manager:dashboard')
            except Manager.DoesNotExist:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'managerpanel/login.html')
