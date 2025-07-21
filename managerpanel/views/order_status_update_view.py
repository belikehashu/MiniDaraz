from django.shortcuts import render, get_object_or_404, redirect
from orders.models.order import Order
from managerpanel.models.manager import Manager
from brandpanel.models.owner import Owner
from brandpanel.models.brand import Brand
from orders.forms.order_status_form import OrderStatusForm
from django.contrib import messages
from managerpanel.decorators import is_owner_or_manager_required

@is_owner_or_manager_required
def manager_update_order_status_view(request, order_id):
    user = request.user
    order = get_object_or_404(Order, id=order_id)
    branch = order.branch

    is_manager = Manager.objects.filter(user=user, branches=branch).exists()
    is_owner = Owner.objects.filter(user=user).exists() and branch.brand.owner.user == user

    if not (is_manager or is_owner):
        return redirect('login')

    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order status updated.")
            return redirect('manager:order_list')
    else:
        form = OrderStatusForm(instance=order)

    return render(request, 'managerpanel/order_status_update.html', {
        'form': form,
        'order': order
    })
