from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from users.models.user import User
from brandpanel.models.owner import Owner
from managerpanel.models.manager import Manager

def owner_manager_login_view(request):
    context = {'active_tab': 'owner'}
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        login_type = request.POST.get('login_type')

        user = authenticate(request, email=email, password=password)

        if user:
            if login_type == 'owner' and Owner.objects.filter(user=user).exists():
                login(request, user)
                return redirect('brand:dashboard')

            elif login_type == 'manager' and Manager.objects.filter(user=user).exists():
                login(request, user)
                return redirect('manager:dashboard')

            else:
                messages.error(request, "Invalid login type or unauthorized access.")
        else:
            messages.error(request, "Invalid email or password.")

        context['active_tab'] = login_type

    return render(request, 'brandpanel/login.html', context)
