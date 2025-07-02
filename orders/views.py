import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from products.models import Product
from users.models import Address
from .forms import CartCheckoutForm
from django.contrib.auth import get_user_model

User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout_view(request):
    if request.method == 'POST':
        selected_raw = request.POST.get('selected_items', '')
        selected_ids = [int(id) for id in selected_raw.split(',') if id.strip().isdigit()]
        cart_items = CartItem.objects.filter(id__in=selected_ids, cart__user=request.user)

        if not cart_items.exists():
            messages.error(request, "Please select at least one item to checkout.")
            return redirect('cart_view')

        request.session['selected_cart_items'] = selected_ids
        return redirect('checkout_confirmation')

    return redirect('cart_view')

@login_required
def unified_checkout_view(request, product_id=None):
    user = request.user
    addresses = Address.objects.filter(user=user)
    items = []
    total_price = 0
    is_buy_now = bool(product_id)

    # For Buy Now, wrap product in fake item class to mimic cart item
    class FakeItem:
        def __init__(self, product, quantity):
            self.product = product
            self.quantity = quantity

    # BUY NOW FLOW
    if is_buy_now:
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get(f'quantity_{product.id}', 1)) if request.method == 'POST' else 1
        items = [FakeItem(product, quantity)]
        total_price = product.price * quantity

    # CART FLOW
    else:
        cart = Cart.objects.filter(user=user).first()
        selected_ids = request.session.get('selected_cart_items', [])
        cart_items = CartItem.objects.filter(id__in=selected_ids, cart=cart)
        items = list(cart_items)
        total_price = sum(item.product.price * item.quantity for item in items)

    if request.method == 'POST':
        form = CartCheckoutForm(request.POST, addresses=addresses)
        payment_method = request.POST.get('payment_method', 'cod')

        if form.is_valid():
            address_id = form.cleaned_data['address']
            address = get_object_or_404(Address, id=address_id)

            # STOCK CHECK
            for item in items:
                product = item.product
                qty = int(request.POST.get(f'quantity_{product.id}', item.quantity))
                if qty > product.stock:
                    messages.error(request, f"Not enough stock for {product.name}.")
                    return redirect('cart_view' if not is_buy_now else 'buy_now', product_id=product_id)

            # CREATE ORDER
            order = Order.objects.create(
                user=user,
                total_price=total_price,
                shipping_address=str(address),
                payment_method=payment_method,
                is_paid=(payment_method == 'cod')  # Mark paid only if COD
            )

            for item in items:
                product = item.product
                qty = int(request.POST.get(f'quantity_{product.id}', item.quantity))
                OrderItem.objects.create(order=order, product=product, quantity=qty)
                product.stock -= qty
                product.save()

            # Clean cart if from cart
            if not is_buy_now:
                cart_items.delete()
                request.session.pop('selected_cart_items', None)

            # Redirect Based on Payment Method
            if payment_method == 'stripe':
                return redirect('start_payment', order_id=order.id)
            elif payment_method == 'cod':
                messages.success(request, "Order placed with Cash on Delivery.")
                return redirect('order_history')
            else:
                messages.info(request, "Online payment method selected. Integration coming soon.")
                return redirect('order_detail', order_id=order.id)

    else:
        form = CartCheckoutForm(addresses=addresses)

    return render(request, 'orders/unified_checkout.html', {
        'items': items,
        'form': form,
        'product_id': product_id,
        'addresses': addresses,
        'total_price': total_price
    })


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to view this order.")

    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': order_items
    })

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Only order owner can cancel
    if request.user != order.user and not request.user.is_superuser:
        return HttpResponseForbidden("You cannot cancel this order.")

    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f"Order #{order.id} cancelled.")
    return redirect('order_history')

@login_required
def delete_order_history_entry(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.user:
        return HttpResponseForbidden("You cannot delete this order.")

    if order.status.lower() == 'cancelled' and request.method == 'POST':
        order.delete()
        messages.success(request, f"Order #{order.id} removed from history.")
    else:
        messages.error(request, "Only cancelled orders can be deleted.")
    return redirect('order_history')

@login_required
def start_payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.is_paid:
        messages.info(request, "Order already paid.")
        return redirect('order_detail', order_id=order.id)

    line_items = []
    for item in order.orderitem_set.all():
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': item.product.name},
                'unit_amount': int(item.product.price * 100),  # cents
            },
            'quantity': item.quantity,
        })

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=f"{settings.DOMAIN}/orders/payment-success/{order.id}/",
        cancel_url=f"{settings.DOMAIN}/orders/payment-cancel/{order.id}/",
    )

    order.stripe_session_id = checkout_session.id
    order.save()

    return redirect(checkout_session.url)

@login_required
def payment_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.is_paid = True
    order.save()
    messages.success(request, f"Payment successful for Order #{order.id}")
    return redirect('order_detail', order_id=order.id)

@login_required
def payment_cancel_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()  # Optional: cancel unpaid order
    messages.error(request, "Payment cancelled.")
    return redirect('cart_view')

