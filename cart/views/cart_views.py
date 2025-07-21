from django.shortcuts import render, redirect, get_object_or_404
from cart.models.cart_item import CartItem
from cart.models.cart import Cart
from products.models.product import Product

class GuestCartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.id = product.id  # Use product ID as fake CartItem ID

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += 1
            item.save()
    else:
        cart = request.session.get("guest_cart", [])
        found = False
        for item in cart:
            if item["product_id"] == product_id:
                item["quantity"] += 1
                found = True
                break
        if not found:
            cart.append({"product_id": product_id, "quantity": 1})
        request.session["guest_cart"] = cart
        request.session.modified = True  # ✅ ensure session updated

    return redirect("cart_view")

def cart_view(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart)
    else:
        raw_cart = request.session.get("guest_cart", [])
        items = []
        for entry in raw_cart:
            try:
                product = Product.objects.get(id=entry["product_id"])
                items.append(GuestCartItem(product, entry["quantity"]))
            except Product.DoesNotExist:
                continue

    total = sum(item.product.price * item.quantity for item in items)
    return render(request, "cart/cart.html", {"items": items, "total": total})

def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
    else:
        cart = request.session.get("guest_cart", [])
        cart = [item for item in cart if item["product_id"] != item_id]
        request.session["guest_cart"] = cart
        request.session.modified = True  # ✅ session consistency

    return redirect("cart_view")

def update_cart(request, item_id):
    if request.method == "POST":
        new_qty = int(request.POST.get("quantity", 1))
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
            item = get_object_or_404(CartItem, id=item_id, cart=cart)
            item.quantity = new_qty
            item.save()
        else:
            cart = request.session.get("guest_cart", [])
            for item in cart:
                if item["product_id"] == item_id:
                    item["quantity"] = new_qty
                    break
            request.session["guest_cart"] = cart
            request.session.modified = True  # ✅ session consistency

    return redirect("cart_view")
