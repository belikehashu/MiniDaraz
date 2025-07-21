from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models.product import Product
from managerpanel.forms import ProductForm
from managerpanel.models import Manager
from brandpanel.models import Branch
from brandpanel.models.owner import Owner
from brandpanel.models.brand import Brand
from managerpanel.decorators import is_owner_or_manager_required


@is_owner_or_manager_required
def product_list_view(request):
    user = request.user
    branch_id = request.GET.get('branch')
    products = []
    branch = None

    try:
        manager = Manager.objects.get(user=user)
        if branch_id:
            products = Product.objects.filter(branch_id=branch_id, branch__in=manager.branches.all())
            branch = get_object_or_404(Branch, id=branch_id)
        else:
            products = Product.objects.filter(branch__in=manager.branches.all())
    except Manager.DoesNotExist:
        try:
            owner = Owner.objects.get(user=user)
            if branch_id:
                branch = get_object_or_404(Branch, id=branch_id, brand__owner=owner)
                products = Product.objects.filter(branch=branch)
            else:
                products = Product.objects.filter(branch__brand__owner=owner)
        except:
            pass

    return render(request, 'managerpanel/product_list.html', {
        'products': products,
        'branch': branch,
    })


@is_owner_or_manager_required
def product_create_view(request):
    user = request.user
    branch_id = request.GET.get('branch')
    branch = None

    try:
        manager = Manager.objects.get(user=user)
        if branch_id:
            branch = manager.branches.get(id=branch_id)
    except Manager.DoesNotExist:
        try:
            owner = Owner.objects.get(user=user)
            if branch_id:
                branch = Branch.objects.get(id=branch_id, brand__owner=owner)
        except:
            pass

    if not branch:
        return redirect('manager:product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, branch=branch)
        if form.is_valid():
            product = form.save(commit=False)
            product.branch = branch
            product.save()
            messages.success(request, "Product added successfully.")
            return redirect(f"{reverse('manager:product_list')}?branch={branch.id}")
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = ProductForm(branch=branch)

    return render(request, 'managerpanel/product_form.html', {
        'form': form,
        'branch_id': branch.id
    })


@is_owner_or_manager_required
def product_update_view(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    branch = product.branch
    branch_id = branch.id if branch else None

    is_manager = Manager.objects.filter(user=user, branches=branch).exists()
    is_owner = Owner.objects.filter(user=user).exists() and branch.brand.owner.user == user

    if not (is_manager or is_owner):
        return redirect('login')

    form = ProductForm(request.POST or None, request.FILES or None, instance=product, branch=branch)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Product updated successfully.")
        return redirect(f"{reverse('manager:product_list')}?branch={branch_id}")

    return render(request, 'managerpanel/product_form.html', {
        'form': form,
        'branch_id': branch_id
    })


@is_owner_or_manager_required
def product_delete_view(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    branch = product.branch
    branch_id = branch.id if branch else None

    is_manager = Manager.objects.filter(user=user, branches=branch).exists()
    is_owner = Owner.objects.filter(user=user).exists() and branch.brand.owner.user == user

    if not (is_manager or is_owner):
        return redirect('login')

    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect(f"{reverse('manager:product_list')}?branch={branch_id}")
