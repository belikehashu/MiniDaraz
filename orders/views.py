from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib.auth.decorators import login_required
from cart.models import CartItem, Cart
from .models import Order, OrderItem

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
    return redirect('order_history')  # replace with your orders list page name

@login_required
def checkout_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    if request.method == 'POST':
        if not items:
            return redirect('cart_view')
        order = Order.objects.create(user=request.user, total_price=total)
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
        items.delete()
        return redirect('order_history')
    return render(request, 'orders/checkout.html', {'items': items, 'total': total})

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})
