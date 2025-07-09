from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models.order import Order
from orders.services.stripe_service import start_direct_payment

@login_required
def start_payment_view(request, order_id):
    return start_direct_payment(request, order_id)

@login_required
def payment_cancel_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    messages.error(request, "Payment cancelled.")
    return redirect('cart_view')
