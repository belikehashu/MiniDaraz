from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from orders.services.order_service import create_order, create_order_items
from orders.models.guest_order import GuestOrder, GuestOrderItem
from cart.models.cart_item import CartItem
from products.models.product import Product
from users.models.address import Address
from cart.models.cart import Cart

def get_selected_cart_items(request):
    selected_raw = request.POST.get('selected_items', '')
    selected_ids = [int(x.strip()) for x in selected_raw.split(',') if x.strip().isdigit()]

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart, id__in=selected_ids)
        return [item.id for item in items]
    else:
        guest_cart = request.session.get("guest_cart", [])
        return [item["product_id"] for item in guest_cart if item["product_id"] in selected_ids]

def prepare_checkout_items(request, product_id, is_buy_now):
    class FakeItem:
        def __init__(self, product, quantity):
            self.product = product
            self.quantity = quantity
            self.id = product.id  # required for template

    items = []

    if is_buy_now:
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get(f'quantity_{product.id}', 1)) if request.method == 'POST' else 1
        items = [FakeItem(product, quantity)]

    elif request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        selected_ids = request.session.get('selected_cart_items', [])
        cart_items = CartItem.objects.filter(id__in=selected_ids, cart=cart)
        items = list(cart_items)

    else:
        guest_cart = request.session.get("guest_cart", [])
        selected_ids = request.session.get("selected_cart_items", [])
        for entry in guest_cart:
            pid = entry["product_id"]
            if pid in selected_ids:
                qty = int(request.POST.get(f'quantity_{pid}', entry["quantity"])) if request.method == 'POST' else entry["quantity"]
                product = get_object_or_404(Product, id=pid)
                items.append(FakeItem(product, qty))

    total_price = sum(item.product.price * item.quantity for item in items)
    return items, total_price

def handle_cod_order(request, user, address_id, items, is_buy_now):
    if not (user and user.is_authenticated):
        messages.error(request, "Guest users are not allowed to use Cash on Delivery.")
        return redirect('checkout_confirmation')

    total_price = 0
    for item in items:
        product = item.product
        qty = int(request.POST.get(f'quantity_{product.id}', item.quantity))
        if qty > product.stock:
            messages.error(request, f"Not enough stock for {product.name}.")
            return redirect('cart_view' if not is_buy_now else 'buy_now', product_id=product.id)
        total_price += product.price * qty

    branch = items[0].product.branch
    address = get_object_or_404(Address, id=address_id)

    order = create_order(user, total_price, address, 'cod', True, branch)
    create_order_items(order, items, request)

    if not is_buy_now:
        item_ids = [i.id for i in items]
        CartItem.objects.filter(id__in=item_ids).delete()
        request.session.pop('selected_cart_items', None)

    messages.success(request, "Order placed with Cash on Delivery.")
    return redirect('order_history')

def handle_stripe_checkout(request, address_id, items, is_buy_now):
    branch = items[0].product.branch
    user = request.user

    if user.is_authenticated:
        checkout_data = {
            'items': [
                {
                    'product_id': item.product.id,
                    'quantity': int(request.POST.get(f'quantity_{item.product.id}', item.quantity))
                } for item in items
            ],
            'address_id': address_id,
            'is_buy_now': is_buy_now,
            'branch_id': branch.id,
        }
    else:
        guest_data = request.session.get("guest_order_data", {})
        checkout_data = {
            'items': [
                {
                    'product_id': item.product.id,
                    'quantity': int(request.POST.get(f'quantity_{item.product.id}', item.quantity))
                } for item in items
            ],
            'guest_order_data': guest_data,
            'is_buy_now': is_buy_now,
            'branch_id': branch.id,
        }

    request.session['stripe_checkout_data'] = checkout_data
    return redirect('start_payment_temp')
