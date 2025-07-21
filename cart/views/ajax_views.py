from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models.product import Product
from cart.models.cart_item import CartItem
from cart.services.get_user_cart import get_user_cart

@require_POST
def ajax_add_to_cart(request):
    product_id = request.POST.get("product_id")
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"success": False, "message": "Product not found."})

    if request.user.is_authenticated:
        cart = get_user_cart(user=request.user, session=request.session)
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
    else:
        guest_cart = request.session.get("guest_cart", [])
        found = False
        for item in guest_cart:
            if item["product_id"] == int(product_id):
                item["quantity"] += 1
                found = True
                break
        if not found:
            guest_cart.append({"product_id": int(product_id), "quantity": 1})
        request.session["guest_cart"] = guest_cart
        return JsonResponse({
            "success": True,
            "message": "Product added to cart.",
            "created": not found,
            "quantity": next((item["quantity"] for item in guest_cart if item["product_id"] == int(product_id)), 1),
            "cart_count": len(guest_cart)
        })

