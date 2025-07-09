from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.forms import CartCheckoutForm
from products.models.product import Product
from users.models.address import Address
from orders.services.checkout_service import get_selected_cart_items
from orders.services.checkout_service import prepare_checkout_items
from orders.services.checkout_service import handle_cod_order
from orders.services.checkout_service import handle_stripe_checkout

@login_required
def checkout_view(request):
    if request.method == 'POST':
        selected_ids = get_selected_cart_items(request)
        if not selected_ids:
            messages.error(request, "Please select at least one item to checkout.")
            return redirect('cart_view')
        request.session['selected_cart_items'] = selected_ids
        return redirect('checkout_confirmation')
    return redirect('cart_view')

@login_required
def unified_checkout_view(request, product_id=None):
    user = request.user
    addresses = Address.objects.filter(user=user)
    is_buy_now = bool(product_id)
    items, total_price = prepare_checkout_items(request, product_id, is_buy_now)

    if request.method == 'POST':
        form = CartCheckoutForm(request.POST, addresses=addresses)
        payment_method = request.POST.get('payment_method', 'cod')

        if form.is_valid():
            address_id = form.cleaned_data['address']
            if payment_method == 'cod':
                return handle_cod_order(request, user, address_id, items, is_buy_now)
            if payment_method == 'stripe':
                return handle_stripe_checkout(request, address_id, items, is_buy_now)
    else:
        form = CartCheckoutForm(addresses=addresses)

    return render(request, 'orders/unified_checkout.html', {
        'items': items,
        'form': form,
        'product_id': product_id,
        'addresses': addresses,
        'total_price': total_price
    })
