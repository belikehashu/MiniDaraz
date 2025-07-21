from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from products.models.product import Product
from orders.services.stripe_service import process_stripe_success
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def start_payment_temp(request):
    data = request.session.get('stripe_checkout_data')
    if not data:
        messages.error(request, "No checkout data found.")
        return redirect('cart_view')

    line_items = []
    total_amount_pkr = 0

    for entry in data['items']:
        product = Product.objects.get(id=entry['product_id'])
        quantity = entry['quantity']
        subtotal = product.price * quantity
        total_amount_pkr += subtotal

        line_items.append({
            'price_data': {
                'currency': 'pkr',
                'product_data': {'name': product.name},
                'unit_amount': int(product.price * 100),
            },
            'quantity': quantity,
        })

    if total_amount_pkr < 500:
        messages.error(request, "Minimum order amount for Stripe payment must be Rs. 500.")
        request.session['stripe_checkout_data'] = data 
        return redirect('checkout_confirmation')


    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=f"{settings.DOMAIN}/orders/payment-success-stripe/",
        cancel_url=f"{settings.DOMAIN}/orders/payment-cancel-stripe/",
    )

    request.session['stripe_session_id'] = session.id
    return redirect(session.url)

def payment_success_stripe_view(request):
    return process_stripe_success(request)
