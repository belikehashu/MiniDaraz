from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from products.models.product import Product
from cart.models.cart_item import CartItem
from cart.services import get_user_cart

@require_POST
@login_required
def ajax_add_to_cart(request):
    product_id = request.POST.get("product_id")
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"success": False, "message": "Product not found."})

    cart = get_user_cart(request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({
        "success": True,
        "message": "Product added to cart.",
        "created": created,
        "quantity": cart_item.quantity,
        "cart_count": cart.cartitem_set.count()
    })
