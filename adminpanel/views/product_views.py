from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from products.models.product import Product
from products.forms import ProductForm
from adminpanel.services.product_service import delete_product_by_id

def is_superadmin(user):
    return user.is_superuser

@user_passes_test(is_superadmin)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'adminpanel/products.html', {'products': products})

@user_passes_test(is_superadmin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form = ProductForm()
    return render(request, 'adminpanel/add_product.html', {'form': form})

@user_passes_test(is_superadmin)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'adminpanel/edit_product.html', {'form': form})

@user_passes_test(is_superadmin)
def delete_product(request, product_id):
    delete_product_by_id(product_id)
    return redirect('admin_products')
