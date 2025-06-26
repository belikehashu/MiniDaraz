from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('products/', views.product_list, name='admin_products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('orders/', views.all_orders, name='admin_orders'),
    path('orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
]
