from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from products.models import Product, Category
from orders.models import Order
from django import forms
from django.contrib import messages
from products.forms import ProductForm

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
