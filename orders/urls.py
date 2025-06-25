from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('history/', views.order_history_view, name='order_history'),
    path('buy/<int:product_id>/', views.buy_now_view, name='buy_now'),
]
