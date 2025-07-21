from django.contrib import admin
from .models.order import Order
from .models.order_item import OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
