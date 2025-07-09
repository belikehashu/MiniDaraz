from django.shortcuts import render
from django.core.paginator import Paginator
from products.models.product import Product
from products.models.category import Category

def index_view(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    sort = request.GET.get('sort')

    products = Product.objects.filter(stock__gt=0)

    if query:
        products = products.filter(name__icontains=query)

    if category_id and category_id != "all":
        products = products.filter(category_id=category_id)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_az':
        products = products.order_by('name')
    elif sort == 'name_za':
        products = products.order_by('-name')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'products/index.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'search_query': query,
        'sort': sort
    })
