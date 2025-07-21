from cart.models.cart import Cart

def get_user_cart(user, session):
    if user:
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
    else:
        # Guest: use session
        cart_id = session.get("guest_cart_id")
        if cart_id:
            try:
                return Cart.objects.get(id=cart_id, user__isnull=True)
            except Cart.DoesNotExist:
                pass

        cart = Cart.objects.create(user=None)
        session["guest_cart_id"] = cart.id
        return cart
