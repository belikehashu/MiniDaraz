from wishlist.models import WishlistItem

def add_item_to_wishlist(user, product, headers):
    existing = WishlistItem.objects.filter(user=user, product=product).first()
    if existing:
        msg = "Product already in your wishlist."
        return {
            'success': False,
            'message': msg,
            'wishlist_count': WishlistItem.objects.filter(user=user).count()
        }
    WishlistItem.objects.create(user=user, product=product)
    return {
        'success': True,
        'message': "Product added to your wishlist.",
        'wishlist_count': WishlistItem.objects.filter(user=user).count()
    }

def remove_item_from_wishlist(user, item, headers):
    item.delete()
    return {
        'success': True,
        'message': "Removed from wishlist.",
        'wishlist_count': WishlistItem.objects.filter(user=user).count()
    }
