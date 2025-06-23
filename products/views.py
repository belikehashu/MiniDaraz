from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def index_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/index.html', {
        'products': products,
        'categories': categories,
    })

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {
        'product': product
    })
