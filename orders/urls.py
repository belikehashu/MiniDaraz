from django.urls import path
from orders.views.checkout_views import checkout_view
from orders.views.checkout_views import unified_checkout_view
from orders.views.history_views import order_history_view
from orders.views.history_views import order_detail_view
from orders.views.history_views import cancel_order
from orders.views.history_views import delete_order_history_entry
from orders.views.payment_views import start_payment_view
from orders.views.payment_views import payment_cancel_view
from orders.views.stripe_views import start_payment_temp
from orders.views.stripe_views import payment_success_stripe_view

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('history/', order_history_view, name='order_history'),
    path('buy/<int:product_id>/', unified_checkout_view, name='buy_now'),
    path('cancel/<int:order_id>/', cancel_order, name='cancel_order'),
    path('details/<int:order_id>/', order_detail_view, name='order_detail'),
    path('delete-history/<int:order_id>/', delete_order_history_entry, name='delete_order_history'),
    path('checkout/confirm/', unified_checkout_view, name='checkout_confirmation'),
    path('pay/<int:order_id>/', start_payment_view, name='start_payment'),
    path('payment-cancel/<int:order_id>/', payment_cancel_view, name='payment_cancel'),
    path('start-stripe/', start_payment_temp, name='start_payment_temp'),
    path('payment-success-stripe/', payment_success_stripe_view, name='payment_success_stripe'),
]
