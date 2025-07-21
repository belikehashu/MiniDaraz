from django.urls import path
from managerpanel.views import *
from managerpanel.views.guest_order_status_update_view import guest_order_status_update_view
from managerpanel.views.auth_views import manager_login_view
from managerpanel.views.order_status_update_view import manager_update_order_status_view
from managerpanel.views.branch_views import branch_detail_view
from managerpanel.views.order_views import manager_order_detail, manager_guest_order_detail

app_name = 'manager'

urlpatterns = [
    path('login/', manager_login_view, name='login'),
    path('dashboard/', manager_dashboard_view, name='dashboard'),
    path('branches/<int:branch_id>/', branch_detail_view, name='branch_detail'),
    path('products/', product_list_view, name='product_list'),
    path('products/create/', product_create_view, name='product_create'),
    path('products/update/<int:product_id>/', product_update_view, name='product_update'),
    path('products/delete/<int:product_id>/', product_delete_view, name='product_delete'),
    path('guest-orders/update-status/<int:order_id>/', guest_order_status_update_view, name='guest_order_status_update'),
    path('categories/', category_list_view, name='category_list'),
    path('categories/create/', category_create_view, name='category_create'),
    path('categories/update/<int:category_id>/', category_update_view, name='category_update'),
    path('categories/delete/<int:category_id>/', category_delete_view, name='category_delete'),
    path('orders/update-status/<int:order_id>/', manager_update_order_status_view, name='order_status_update'),
    path('orders/', order_list_view, name='order_list'),
    path('orders/<int:order_id>/detail/', manager_order_detail, name='order_detail'),
    path('guest-orders/<int:order_id>/detail/', manager_guest_order_detail, name='guest_order_detail'),
]
