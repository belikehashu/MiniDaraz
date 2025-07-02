from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from orders.models import Order
from django import forms
from products.models import Product, Category
from products.forms import ProductForm, CategoryForm
from django.contrib import messages


def is_superadmin(user):
    return user.is_superuser

@user_passes_test(is_superadmin)
def dashboard(request):
    return render(request, 'adminpanel/dashboard.html')

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
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_products')

@user_passes_test(is_superadmin)
def all_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/orders.html', {'orders': orders})

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

@user_passes_test(is_superadmin)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order status updated.")
            return redirect('admin_orders')
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'adminpanel/update_order_status.html', {'form': form, 'order': order})

@user_passes_test(is_superadmin)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'adminpanel/categories.html', {'categories': categories})

# Add or Edit Category
@user_passes_test(is_superadmin)
def add_edit_category(request, category_id=None):
    category = get_object_or_404(Category, id=category_id) if category_id else None
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'adminpanel/add_edit_category.html', {'form': form})

# Delete Category (and its related products)
@user_passes_test(is_superadmin)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('admin_categories')
