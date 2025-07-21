from django.urls import path
from cart.views.cart_views import cart_view
from cart.views.cart_views import add_to_cart
from cart.views.cart_views import remove_from_cart
from cart.views.cart_views import update_cart
from cart.views.ajax_views import ajax_add_to_cart

urlpatterns = [
    path('', cart_view, name='cart_view'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', update_cart, name='update_cart'),
    path('ajax/add/', ajax_add_to_cart, name='ajax_add_to_cart'),
]
