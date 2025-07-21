import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from users.models.address import Address
from products.models.product import Product
from orders.models.order import Order
from cart.models.cart import Cart
from cart.models.cart_item import CartItem
from brandpanel.models.branch import Branch
from orders.models.guest_order import GuestOrder, GuestOrderItem
from orders.services.order_service import create_order
from orders.services.order_service import create_order_items

stripe.api_key = settings.STRIPE_SECRET_KEY

def process_stripe_success(request):
    data = request.session.pop('stripe_checkout_data', None)
    session_id = request.session.pop('stripe_session_id', None)

    if not data or not session_id:
        messages.error(request, "Invalid or expired session.")
        return redirect('cart_view')

    is_guest = not request.user.is_authenticated
    total_price = 0
    order_items_data = []
    for entry in data['items']:
        product = get_object_or_404(Product, id=entry['product_id'])
        qty = entry['quantity']
        subtotal = product.price * qty
        total_price += subtotal
        order_items_data.append((product, qty))

    branch = get_object_or_404(Branch, id=data['branch_id'])

    if is_guest:
        guest_data = request.session.pop("guest_order_data", {})
        guest_order = GuestOrder.objects.create(
            first_name=guest_data.get('first_name'),
            last_name=guest_data.get('last_name'),
            email=guest_data.get('email'),
            phone=guest_data.get('phone'),
            home_address=guest_data.get('street'),
            city=guest_data.get('city'),
            zip_code=guest_data.get('zip_code'),
            province=guest_data.get('province'),
            country=guest_data.get('country'),
            total_price=total_price,
            payment_method='stripe',
            is_paid=True,
            branch=branch,
        )
        for product, qty in order_items_data:
            GuestOrderItem.objects.create(
                order=guest_order,
                product=product,
                quantity=qty
            )
            
        product.stock -= qty
        product.save()
        messages.success(request, f"Payment successful for Guest Order #{guest_order.id}")
        return redirect('index')
    else:
        user = request.user
        address = get_object_or_404(Address, id=data['address_id'])
        order = create_order(user, total_price, address, 'stripe', True, branch)
        create_order_items(order, order_items_data)
        if not data.get('is_buy_now'):
            cart = Cart.objects.filter(user=user).first()
            CartItem.objects.filter(cart=cart, product_id__in=[p.id for p, _ in order_items_data]).delete()
        messages.success(request, f"Payment successful for Order #{order.id}")
        return redirect('order_detail', order_id=order.id)

def start_direct_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.is_paid:
        messages.info(request, "Order already paid.")
        return redirect('order_detail', order_id=order.id)
    line_items = []
    for item in order.orderitem_set.all():
        line_items.append({
            'price_data': {
                'currency': 'pkr',
                'product_data': {'name': item.product.name},
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        })
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=f"{settings.DOMAIN}/orders/payment-success/{order.id}/",
        cancel_url=f"{settings.DOMAIN}/orders/payment-cancel/{order.id}/",
    )
    order.stripe_session_id = session.id
    order.save()
    return redirect(session.url)
