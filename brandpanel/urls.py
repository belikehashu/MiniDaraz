from django.urls import path
from brandpanel.views import *
from brandpanel.views.assign_manager_view import remove_manager_view
from brandpanel.views.auth_views import owner_manager_login_view

app_name = 'brand'

urlpatterns = [
    path('register/', owner_register_view, name='register'),
    path('login/', owner_manager_login_view, name='seller_login'),
    path('dashboard/', owner_dashboard_view, name='dashboard'),
    path('branches/create/', branch_create_view, name='branch_create'),
    path('branches/update/<int:branch_id>/', branch_update_view, name='branch_update'),
    path('branches/delete/<int:branch_id>/', branch_delete_view, name='branch_delete'),
    path('managers/create/', manager_create_view, name='manager_create'),
    path('branches/<int:branch_id>/assign-manager/', assign_manager_view, name='assign_manager'),
    path('branch/<int:branch_id>/remove-manager/<int:manager_id>/', remove_manager_view, name='remove_manager'),

]
