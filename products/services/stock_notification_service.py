def handle_stock_notification(product, old_stock):

    from wishlist.models import WishlistItem
    from notifications.models import Notification

    wishlist_users = WishlistItem.objects.filter(product=product).select_related('user')

    for item in wishlist_users:
        if product.stock == 0 and old_stock > 0:
            Notification.objects.create(
                user=item.user,
                product=product,
                message="The product is now out of stock."
            )
        elif product.stock > 0 and old_stock == 0:
            Notification.objects.create(
                user=item.user,
                product=product,
                message="The product is back in stock!"
            )
