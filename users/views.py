from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
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
from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'users/forgot_password.html', {'error': 'Email not registered.'})

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
        session_otp = request.session.get('otp')
        if user_otp == session_otp:
            return redirect('reset_password')
        else:
            return render(request, 'users/verify_otp.html', {
                'error': 'Invalid OTP',
                'email': request.session.get('reset_email')
            })

    return redirect('forgot_password')

def reset_password(request):
    if request.method == 'POST':
        new_pass = request.POST['new_password']
        confirm_pass = request.POST['confirm_password']
        email = request.session.get('reset_email')

        if new_pass != confirm_pass:
            return render(request, 'users/reset_password.html', {'error': 'Passwords do not match'})

        try:
            user = User.objects.get(email=email)
            if user.check_password(new_pass):
                return render(request, 'users/reset_password.html', {'error': 'New password must be different from the current password'})

            user.set_password(new_pass)
            user.save()

            send_mail(
                subject='Password Changed',
                message='Your password has been successfully changed.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )
            return redirect('login')
        except User.DoesNotExist:
            return redirect('forgot_password')

    return render(request, 'users/reset_password.html')

class PasswordChangeNotifyView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        new_password = form.cleaned_data.get('new_password1')
        old_password = form.cleaned_data.get('old_password')

        if new_password == old_password:
            form.add_error('new_password1', "New password must be different from the current password.")
            return self.form_invalid(form)

        response = super().form_valid(form)

        user = self.request.user
        send_mail(
            subject='Password Changed Successfully',
            message=f'''Hello {user.first_name or user.email},

Your MiniDaraz account password has been successfully changed.

If this wasn't you, please contact support immediately.

Regards,  
MiniDaraz Team
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(self.request, "Password changed successfully!")
        return response

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get('next') or 'profile'
            messages.success(request, "Login successful!")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    profile_form = ProfileUpdateForm(instance=user)
    address_form = AddressForm()
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('profile')
            else:
                messages.error(request, "Please correct the errors in your profile form.")

        elif 'add_address' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = user
                address.save()
                messages.success(request, "Address added successfully.")
                return redirect('profile')
            else:
                messages.error(request, "Please correct the errors in address form.")

    addresses = Address.objects.filter(user=user)
    return render(request, 'users/profile.html', {
        'form': profile_form,
        'address_form': address_form,
        'addresses': addresses,
    })

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully.")
            return redirect('profile')
    else:
        form = AddressForm(instance=address)
    return render(request, 'users/edit_address.html', {'form': form})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, "Address deleted successfully.")
        return redirect('profile')
    return render(request, 'users/delete_address.html', {'address': address})
