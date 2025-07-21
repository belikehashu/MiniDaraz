from django.shortcuts import render
from orders.models.order import Order
from orders.models.guest_order import GuestOrder
from managerpanel.models import Manager
from brandpanel.models.owner import Owner
from brandpanel.models.brand import Brand
from managerpanel.decorators import is_owner_or_manager_required

@is_owner_or_manager_required
def order_list_view(request):
    user = request.user
    branch_id = request.GET.get('branch')
    orders = []
    guest_orders = []

    try:
        manager = Manager.objects.get(user=user)
        if branch_id:
            orders = Order.objects.filter(branch_id=branch_id, branch__in=manager.branches.all()).order_by('-created_at')
            guest_orders = GuestOrder.objects.filter(branch_id=branch_id, branch__in=manager.branches.all()).order_by('-created_at')
        else:
            orders = Order.objects.filter(branch__in=manager.branches.all()).order_by('-created_at')
            guest_orders = GuestOrder.objects.filter(branch__in=manager.branches.all()).order_by('-created_at')
    except Manager.DoesNotExist:
        try:
            owner = Owner.objects.get(user=user)
            if branch_id:
                orders = Order.objects.filter(branch_id=branch_id, branch__brand__owner=owner).order_by('-created_at')
                guest_orders = GuestOrder.objects.filter(branch_id=branch_id, branch__brand__owner=owner).order_by('-created_at')
            else:
                orders = Order.objects.filter(branch__brand__owner=owner).order_by('-created_at')
                guest_orders = GuestOrder.objects.filter(branch__brand__owner=owner).order_by('-created_at')
        except:
            pass

    return render(request, 'managerpanel/order_list.html', {
        'orders': orders,
        'guest_orders': guest_orders,
    })
