from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from orders.services.order_service import create_order
from orders.services.order_service import create_order_items
from orders.models.order import Order
from cart.models.cart_item import CartItem
from products.models.product import Product
from users.models.address import Address

def get_selected_cart_items(request):
    selected_raw = request.POST.get('selected_items', '')
    selected_ids = [int(id) for id in selected_raw.split(',') if id.strip().isdigit()]
    cart_items = CartItem.objects.filter(id__in=selected_ids, cart__user=request.user)
    if not cart_items.exists():
        return []
    return selected_ids

def prepare_checkout_items(request, product_id, is_buy_now):
    from cart.models import Cart
    class FakeItem:
        def __init__(self, product, quantity):
            self.product = product
            self.quantity = quantity
    items = []
    if is_buy_now:
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get(f'quantity_{product.id}', 1)) if request.method == 'POST' else 1
        items = [FakeItem(product, quantity)]
    else:
        cart = Cart.objects.filter(user=request.user).first()
        selected_ids = request.session.get('selected_cart_items', [])
        cart_items = CartItem.objects.filter(id__in=selected_ids, cart=cart)
        if not cart_items.exists():
            request.session.pop('selected_cart_items', None)
            return [], 0
        items = list(cart_items)
    total_price = 0
    for item in items:
        qty = int(request.POST.get(f'quantity_{item.product.id}', item.quantity)) if request.method == 'POST' else item.quantity
        total_price += item.product.price * qty
    return items, total_price

def handle_cod_order(request, user, address_id, items, is_buy_now):
    address = get_object_or_404(Address, id=address_id)
    total_price = 0
    for item in items:
        product = item.product
        qty = int(request.POST.get(f'quantity_{product.id}', item.quantity))
        if qty > product.stock:
            messages.error(request, f"Not enough stock for {product.name}.")
            return redirect('cart_view' if not is_buy_now else 'buy_now', product_id=product.id)
        total_price += product.price * qty
    order = create_order(user, total_price, address, 'cod', True)
    create_order_items(order, items, request)
    if not is_buy_now:
        item_ids = [i.id for i in items]
        CartItem.objects.filter(id__in=item_ids).delete()
        request.session.pop('selected_cart_items', None)
    messages.success(request, "Order placed with Cash on Delivery.")
    return redirect('order_history')

def handle_stripe_checkout(request, address_id, items, is_buy_now):
    checkout_data = {
        'items': [
            {
                'product_id': item.product.id,
                'quantity': int(request.POST.get(f'quantity_{item.product.id}', item.quantity))
            } for item in items
        ],
        'address_id': address_id,
        'is_buy_now': is_buy_now,
    }
    request.session['stripe_checkout_data'] = checkout_data
    return redirect('start_payment_temp')
