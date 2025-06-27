from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib.auth.decorators import login_required
from cart.models import CartItem, Cart
from .models import Order, OrderItem
from django.contrib import messages

@login_required
def buy_now_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_price=product.price)
        OrderItem.objects.create(order=order, product=product, quantity=1)
        return redirect('order_history')
    return render(request, 'orders/buy_now.html', {'product': product})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()
    return redirect('order_history')

@login_required
def delete_order_history_entry(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status.lower() == 'cancelled' and request.method == 'POST':
        messages.success(request, f"Order #{order.id} removed from history.")
        order.delete()
        
    else:
        messages.error(request, "Only cancelled orders can be deleted.")
    return redirect('order_history')

@login_required
def checkout_view(request):
    if request.method == 'POST':
        selected_raw = request.POST.get('selected_items', '')
        selected_ids = [int(id) for id in selected_raw.split(',') if id.strip().isdigit()]

        cart_items = CartItem.objects.filter(id__in=selected_ids, cart__user=request.user)

        if not cart_items.exists():
            messages.error(request, "Please select at least one item to checkout.")
            return redirect('cart_view')

        total = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(user=request.user, total_price=total)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        cart_items.delete()

        messages.success(request, "Order placed successfully.")
        return redirect('order_history')

    cart = Cart.objects.filter(user=request.user).first()
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'orders/checkout.html', {'items': items, 'total': total})


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})
