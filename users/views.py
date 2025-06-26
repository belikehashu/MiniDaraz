from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileUpdateForm, AddressForm
from django.contrib import messages
from .models import Address, User

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, "Invalid email or password")
        except User.DoesNotExist:
            messages.error(request, "Email not found")
    return render(request, 'users/login.html')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        address_form = AddressForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")

        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Address added.")

        return redirect('profile')
    
    else:
        form = ProfileUpdateForm(instance=request.user)
        address_form = AddressForm()

    addresses = Address.objects.filter(user=request.user)

    return render(request, 'users/profile.html', {
        'form': form,
        'address_form': address_form,
        'addresses': addresses
    })

def logout_view(request):
    logout(request)
    return redirect('login')
