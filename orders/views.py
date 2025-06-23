from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem, Cart
from .models import Order, OrderItem

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
