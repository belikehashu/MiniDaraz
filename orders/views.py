from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib.auth.decorators import login_required
from cart.models import CartItem, Cart
from .models import Order, OrderItem
from django.contrib import messages
from users.models import Address
from .forms import BuyNowForm, CartCheckoutForm
from django.contrib.auth import get_user_model
User = get_user_model()

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
def buy_now_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    addresses = Address.objects.filter(user=user)

    if request.method == 'POST':
        form = BuyNowForm(request.POST, addresses=addresses)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            address_id = form.cleaned_data['address']
            address_obj = Address.objects.get(id=address_id)

            total_price = product.price * quantity

            order = Order.objects.create(
                user=user,
                total_price=total_price,
                shipping_address=str(address_obj)
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )
            product.stock -= quantity
            product.save()


            return redirect('order_history')
    else:
        form = BuyNowForm(addresses=addresses)

    return render(request, 'orders/buy_now.html', {
        'product': product,
        'form': form,
        'addresses': addresses
    })

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
        request.session['selected_cart_items'] = selected_ids
        return redirect('checkout_confirmation')

    return redirect('cart_view')

@login_required
def checkout_confirmation_view(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    selected_ids = request.session.get('selected_cart_items', [])
    cart_items = CartItem.objects.filter(id__in=selected_ids, cart=cart)
    addresses = Address.objects.filter(user=user)

    if request.method == 'POST':
        form = CartCheckoutForm(request.POST, addresses=addresses)
        if form.is_valid():
            address_id = form.cleaned_data['address']
            address = Address.objects.get(id=address_id)

            for item in cart_items:
                if item.quantity > item.product.stock:
                    messages.error(request, f"Not enough stock for {item.product.name}.")
                    return redirect('cart_view')

            total_price = sum(item.product.price * item.quantity for item in cart_items)

            order = Order.objects.create(
                user=user,
                total_price=total_price,
                shipping_address=str(address)
            )

            for item in cart_items:
                item.product.stock -= item.quantity
                item.product.save()

                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

            cart_items.delete()
            del request.session['selected_cart_items']

            messages.success(request, "Order placed successfully.")
            return redirect('order_history')

    else:
        if not cart_items:
            messages.error(request, "No valid items selected.")
            return redirect('cart_view')

        form = CartCheckoutForm(addresses=addresses)

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'orders/checkout_confirmation.html', {
        'items': cart_items,
        'form': form,
        'total_price': total_price
    })



@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})
