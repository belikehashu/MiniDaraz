from django.urls import path
from adminpanel.views.dashboard_views import dashboard
from adminpanel.views.product_views import product_list, add_product, edit_product, delete_product
from adminpanel.views.order_views import all_orders, update_order_status
from adminpanel.views.category_views import category_list, add_edit_category, delete_category

urlpatterns = [
    path('', dashboard, name='admin_dashboard'),
    path('products/', product_list, name='admin_products'),
    path('products/add/', add_product, name='add_product'),
    path('products/edit/<int:product_id>/', edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('orders/', all_orders, name='admin_orders'),
    path('orders/<int:order_id>/update/', update_order_status, name='update_order_status'),
    path('categories/', category_list, name='admin_categories'),
    path('categories/add/', add_edit_category, name='add_category'),
    path('categories/edit/<int:category_id>/', add_edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),
]
