from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q

def index_view(request):
    query = request.GET.get('q')  # search text
    category_id = request.GET.get('category')  # category id

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category_id and category_id != "all":
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, 'products/index.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'search_query': query
    })

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {
        'product': product
    })
