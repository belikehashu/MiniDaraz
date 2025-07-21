import random
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from users.models.user import User

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    send_mail(
        subject='Your OTP Code',
        message=f'Your OTP for password reset is: {otp}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )

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

def reset_user_password(email, new_password):
    try:
        user = User.objects.get(email=email)
        if user.check_password(new_password):
            return (False, "New password must be different from the current password.")

        user.set_password(new_password)
        user.save()

        send_mail(
            subject='Password Changed',
            message='Your password has been successfully changed.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        return (True, None)
    except User.DoesNotExist:
        return (False, "User does not exist.")
