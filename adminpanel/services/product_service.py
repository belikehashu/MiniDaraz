from products.models.product import Product
from django.shortcuts import get_object_or_404

def delete_product_by_id(product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
