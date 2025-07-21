from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from managerpanel.forms import ManagerLoginForm
from managerpanel.models import Manager

def manager_login_view(request):
    if request.method == 'POST':
        form = ManagerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if Manager.objects.filter(user=user).exists():
                    login(request, user)
                    return redirect('manager:dashboard')
                else:
                    messages.error(request, "You are not registered as a manager.")
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = ManagerLoginForm()

    return render(request, 'managerpanel/login.html', {
        'form': form,
        'active_tab': 'manager'
    })
