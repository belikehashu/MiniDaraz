from orders.models.order_item import OrderItem
from orders.models.guest_order import GuestOrder, GuestOrderItem
from django.shortcuts import render, get_object_or_404, redirect
from orders.models.order import Order
from managerpanel.models.manager import Manager
from brandpanel.models.owner import Owner
from brandpanel.models.brand import Brand
from managerpanel.decorators import is_owner_or_manager_required

@is_owner_or_manager_required
def manager_order_detail(request, order_id):
    user = request.user
    order = get_object_or_404(Order, id=order_id)
    branch = order.branch

    is_manager = Manager.objects.filter(user=user, branches=branch).exists()
    is_owner = Owner.objects.filter(user=user).exists() and branch.brand.owner.user == user

    if not (is_manager or is_owner):
        return redirect('login')

    items = order.items.all()
    return render(request, 'managerpanel/order_detail.html', {'order': order, 'items': items})


@is_owner_or_manager_required
def manager_guest_order_detail(request, order_id):
    user = request.user
    order = get_object_or_404(GuestOrder, id=order_id)
    branch = order.branch

    is_manager = Manager.objects.filter(user=user, branches=branch).exists()
    is_owner = Owner.objects.filter(user=user).exists() and branch.brand.owner.user == user

    if not (is_manager or is_owner):
        return redirect('login')

    items = order.items.all()
    return render(request, 'managerpanel/guest_order_detail.html', {'order': order, 'items': items})
