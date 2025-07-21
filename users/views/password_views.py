from django.shortcuts import render, redirect
from users.services.password_service import send_otp_email, reset_user_password, generate_otp
from users.models.address import User

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'users/forgot_password.html', {'error': 'Email not registered.'})

        otp = generate_otp()
        request.session['reset_email'] = email
        request.session['otp'] = otp

        send_otp_email(email, otp)
        return render(request, 'users/verify_otp.html', {'email': email})

    return render(request, 'users/forgot_password.html')


def reset_password(request):
    if request.method == 'POST':
        new_pass = request.POST['new_password']
        confirm_pass = request.POST['confirm_password']
        email = request.session.get('reset_email')

        if new_pass != confirm_pass:
            return render(request, 'users/reset_password.html', {'error': 'Passwords do not match'})

        success, error = reset_user_password(email, new_pass)
        if not success:
            return render(request, 'users/reset_password.html', {'error': error})

        return redirect('login')

    return render(request, 'users/reset_password.html')


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
