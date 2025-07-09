from .models import CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        return {
            'cart_count': CartItem.objects.filter(cart__user=request.user).count()
        }
    return {'cart_count': 0}
