# orders/scripts/fill_missing_products.py

from orders.models import OrderItem
from products.models import Product

def run():
    default_product = Product.objects.first()
    if not default_product:
        print("❌ No product found to use as default.")
        return

    null_items = OrderItem.objects.filter(product__isnull=True)
    for item in null_items:
        item.product = default_product
        item.save()
        print(f"✅ Fixed OrderItem #{item.id}")
    
    print("🎉 All null product fields updated!")
