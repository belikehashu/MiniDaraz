from django.urls import path
from users.views.auth_views import register_view
from users.views.auth_views import login_view
from users.views.auth_views import logout_view
from users.views.profile_views import profile_view
from users.services.password_service import PasswordChangeNotifyView
from users.views.password_views import forgot_password
from users.views.password_views import verify_otp
from users.views.password_views import reset_password

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change-password/', PasswordChangeNotifyView.as_view(), name='change_password'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('reset-password/', reset_password, name='reset_password'),
]
