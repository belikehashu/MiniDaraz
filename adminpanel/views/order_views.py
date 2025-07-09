from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from orders.models.order import Order
from adminpanel.forms.order_status_form import OrderStatusForm
from adminpanel.services.order_service import notify_order_status_update

def is_superadmin(user):
    return user.is_superuser

@user_passes_test(is_superadmin)
def all_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/orders.html', {'orders': orders})

@user_passes_test(is_superadmin)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order status updated.")
            order.refresh_from_db()
            notify_order_status_update(order)
            return redirect('admin_orders')
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'adminpanel/update_order_status.html', {'form': form, 'order': order})
