from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem

def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

@login_required
def cart_view(request):
    cart = get_user_cart(request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart/cart.html', {'items': items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    cart = get_user_cart(request.user)
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_view')

@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        new_qty = int(request.POST.get('quantity', 1))
        if new_qty > 0:
            item.quantity = new_qty
            item.save()
    return redirect('cart_view')
