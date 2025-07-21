from django.shortcuts import render, get_object_or_404, redirect
from managerpanel.models.manager import Manager
from brandpanel.models.owner import Owner
from brandpanel.models.brand import Brand
from orders.models.guest_order import GuestOrder
from orders.forms.guest_order_status_form import GuestOrderStatusForm
from django.contrib import messages
from managerpanel.decorators import is_owner_or_manager_required

@is_owner_or_manager_required
def guest_order_status_update_view(request, order_id):
    user = request.user
    order = get_object_or_404(GuestOrder, id=order_id)
    branch = order.branch

    is_manager = Manager.objects.filter(user=user, branches=branch).exists()
    is_owner = Owner.objects.filter(user=user).exists() and branch.brand.owner.user == user

    if not (is_manager or is_owner):
        return redirect('login')

    if request.method == 'POST':
        form = GuestOrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Guest order status updated.")
            return redirect('manager:order_list')
    else:
        form = GuestOrderStatusForm(instance=order)

    return render(request, 'managerpanel/guest_order_status_update.html', {
        'form': form,
        'order': order
    })
