from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from orders.forms.cart_checkout_form import CartCheckoutForm
from orders.forms.guest_checkout_form import GuestCheckoutForm
from users.models.address import Address
from orders.services.checkout_service import (
    get_selected_cart_items,
    prepare_checkout_items,
    handle_cod_order,
    handle_stripe_checkout
)

def checkout_view(request):
    if request.method == 'POST':
        selected_ids = get_selected_cart_items(request)
        if not selected_ids:
            messages.error(request, "Please select at least one item to checkout.")
            return redirect('cart_view')
        request.session['selected_cart_items'] = selected_ids
        return redirect('checkout_confirmation')
    return redirect('cart_view')


def unified_checkout_view(request, product_id=None):
    user = request.user
    is_buy_now = bool(product_id)
    addresses = Address.objects.filter(user=user) if user.is_authenticated else None

    if request.method == 'POST':
        # ✅ first initialize the form
        form = (
            CartCheckoutForm(request.POST, addresses=addresses)
            if user.is_authenticated
            else GuestCheckoutForm(request.POST)
        )

        # ✅ second get items with updated quantity from POST
        items, total_price = prepare_checkout_items(request, product_id, is_buy_now)

        if form.is_valid():
            if user.is_authenticated:
                address_id = form.cleaned_data['address']
                payment_method = form.cleaned_data['payment_method']

                if payment_method == "cod":
                    return handle_cod_order(request, user, address_id, items, is_buy_now)

                if payment_method == "stripe":
                    if total_price < 500:
                        messages.error(request, "Minimum order amount for Stripe payment must be Rs. 500.")
                    else:
                        return handle_stripe_checkout(request, address_id, items, is_buy_now)

            else:
                guest_data = {
                    "first_name": form.cleaned_data['first_name'],
                    "last_name": form.cleaned_data['last_name'],
                    "email": form.cleaned_data['email'],
                    "phone": form.cleaned_data['phone'],
                    "street": form.cleaned_data['guest_address'],
                    "city": form.cleaned_data['city'],
                    "zip_code": form.cleaned_data['zip_code'],
                    "province": form.cleaned_data['province'],
                    "country": form.cleaned_data['country'],
                    "payment_method": form.cleaned_data['payment_method'],
                }

                request.session["guest_order_data"] = guest_data

                if guest_data["payment_method"] == "cod":
                    return handle_cod_order(request, None, None, items, is_buy_now)

                if guest_data["payment_method"] == "stripe":
                    if total_price < 500:
                        messages.error(request, "Minimum order amount for Stripe payment must be Rs. 500.")
                    else:
                        return handle_stripe_checkout(request, None, items, is_buy_now)

    else:
        items, total_price = prepare_checkout_items(request, product_id, is_buy_now)
        form = (
            CartCheckoutForm(addresses=addresses)
            if user.is_authenticated
            else GuestCheckoutForm()
        )

    return render(request, 'orders/unified_checkout.html', {
        'form': form,
        'items': items,
        'addresses': addresses,
        'product_id': product_id,
        'total_price': total_price
    })


