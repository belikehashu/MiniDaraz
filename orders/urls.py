from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('history/', views.order_history_view, name='order_history'),
    path('buy/<int:product_id>/', views.buy_now_view, name='buy_now'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('details/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('delete-history/<int:order_id>/', views.delete_order_history_entry, name='delete_order_history'),
    path('checkout/confirm/', views.checkout_confirmation_view, name='checkout_confirmation'),
]
