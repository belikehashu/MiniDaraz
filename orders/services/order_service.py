from django.shortcuts import get_object_or_404
from orders.models.order import Order
from orders.models.order_item import OrderItem
from products.models.product import Product
from notifications.services.notification_service import create_notification


def create_order(user, total_price, address, payment_method, is_paid):
    order = Order.objects.create(
        user=user,
        total_price=total_price,
        shipping_address=str(address),
        payment_method=payment_method,
        is_paid=is_paid
    )
    return order

def create_order_items(order, items_data, request=None):
    for item in items_data:
        product = item.product if hasattr(item, 'product') else item[0]
        qty = item.quantity if hasattr(item, 'quantity') else item[1]
        if request:
            qty = int(request.POST.get(f'quantity_{product.id}', qty))
        OrderItem.objects.create(order=order, product=product, quantity=qty)
        product.stock -= qty
        product.save()
        create_notification(order.user, f"Your order #{order.id} has been placed successfully.")
