from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileUpdateForm, AddressForm
from django.contrib import messages
from .models import Address, User
from django.conf import settings
from django.urls import reverse_lazy
import random
from django.contrib.auth.hashers import make_password

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = str(random.randint(100000, 999999))
        request.session['reset_email'] = email
        request.session['otp'] = otp

        send_mail(
            subject='Your OTP Code',
            message=f'Your OTP for password reset is: {otp}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        return render(request, 'users/verify_otp.html', {'email': email})
    
    return render(request, 'users/forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST['otp']
        if user_otp == request.session.get('otp'):
            return redirect('reset_password')
        else:
            return render(request, 'users/verify_otp.html', {'error': 'Invalid OTP'})
    
    return redirect('forgot_password')
def reset_password(request):
    if request.method == 'POST':
        new_pass = request.POST['new_password']
        confirm_pass = request.POST['confirm_password']
        if new_pass == confirm_pass:
            email = request.session.get('reset_email')
            user = User.objects.get(email=email)
            user.password = make_password(new_pass)
            user.save()

            send_mail(
                subject='Password Changed',
                message='Your password has been successfully changed.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )
            return redirect('login')
        else:
            return render(request, 'users/reset_password.html', {'error': 'Passwords do not match'})
    
    return render(request, 'users/reset_password.html')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.request.user
        send_mail(
            subject='Password Changed Successfully',
            message=f'''Hello {user.first_name or user.username},\nYour password has been changed successfully.\nIf this wasn't you, contact support immediately.\nReagrds,\nMiniDaraz''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(self.request, "Password changed successfully and a confirmation email has been sent.")
        return response

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
