from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from wishlist.models import WishlistItem
from wishlist.services.wishlist_service import add_item_to_wishlist
from wishlist.services.wishlist_service import remove_item_from_wishlist
from products.models.product import Product

@login_required
def wishlist_view(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    response = add_item_to_wishlist(request.user, product, request.headers)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(response)
    if response['success']:
        messages.success(request, response['message'])
    else:
        messages.info(request, response['message'])
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def remove_from_wishlist(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
        response = remove_item_from_wishlist(request.user, item, request.headers)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(response)
        messages.success(request, response['message'])
    return redirect('wishlist')
