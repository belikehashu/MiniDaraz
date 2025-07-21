from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from orders.models.order import Order
from orders.models.order_item import OrderItem

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user != order.user and not request.user.is_superuser:
        return HttpResponseForbidden()
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'orders/order_detail.html', {'order': order, 'items': order_items})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user != order.user and not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()
        return JsonResponse({'success': True, 'message': f"Order #{order.id} cancelled."})

    return JsonResponse({'success': False, 'message': 'Only pending orders can be cancelled.'})

@login_required
def delete_order_history_entry(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user != order.user:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    if order.status.lower() == 'cancelled' and request.method == 'POST':
        order.delete()
        return JsonResponse({'success': True, 'message': f"Order #{order.id} removed from history."})
    return JsonResponse({'success': False, 'message': 'Only cancelled orders can be deleted.'})
