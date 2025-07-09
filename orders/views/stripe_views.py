from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.services.stripe_service import process_stripe_success
import stripe
from django.conf import settings
from products.models.product import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def start_payment_temp(request):
    data = request.session.get('stripe_checkout_data')
    if not data:
        messages.error(request, "No checkout data found.")
        return redirect('cart_view')
    line_items = []
    for entry in data['items']:
        product = Product.objects.get(id=entry['product_id'])
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': product.name},
                'unit_amount': int(product.price * 100),
            },
            'quantity': entry['quantity'],
        })
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=f"{settings.DOMAIN}/orders/payment-success-stripe/",
        cancel_url=f"{settings.DOMAIN}/orders/payment-cancel-stripe/",
    )
    request.session['stripe_session_id'] = session.id
    return redirect(session.url)

@login_required
def payment_success_stripe_view(request):
    return process_stripe_success(request)
