from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('history/', views.order_history_view, name='order_history'),
    path('buy/<int:product_id>/', views.unified_checkout_view, name='buy_now'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('details/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('delete-history/<int:order_id>/', views.delete_order_history_entry, name='delete_order_history'),
    path('checkout/confirm/', views.unified_checkout_view, name='checkout_confirmation'),
    path('pay/<int:order_id>/', views.start_payment_view, name='start_payment'),
    path('payment-success/<int:order_id>/', views.payment_success_view, name='payment_success'),
    path('payment-cancel/<int:order_id>/', views.payment_cancel_view, name='payment_cancel'),

]
