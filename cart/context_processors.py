from cart.services.get_user_cart import get_user_cart
from cart.models.cart_item import CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = get_user_cart(user=request.user, session=request.session)
        count = CartItem.objects.filter(cart=cart).count() if cart else 0
    else:
        guest_cart = request.session.get("guest_cart", [])
        count = len(guest_cart)  # ✅ just number of unique products

    return {"cart_count": count}

