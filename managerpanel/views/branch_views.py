from django.shortcuts import render, get_object_or_404, redirect
from managerpanel.models import Manager
from brandpanel.models.owner import Owner
from brandpanel.models.branch import Branch
from brandpanel.models.brand import Brand
from products.models.product import Product
from managerpanel.decorators import is_owner_or_manager_required

@is_owner_or_manager_required
def branch_detail_view(request, branch_id):
    user = request.user
    branch = get_object_or_404(Branch, id=branch_id)
    products = []

    try:
        # Try if user is a manager
        manager = Manager.objects.get(user=user)
        if branch in manager.branches.all():
            products = Product.objects.filter(branch=branch)
        else:
            return redirect('manager:dashboard')  # unauthorized
    except Manager.DoesNotExist:
        # Try if user is an owner
        try:
            owner = Owner.objects.get(user=user)
            if branch.brand == owner.brand:
                products = Product.objects.filter(branch=branch)
            else:
                return redirect('brand:seller_dashboard')  # unauthorized
        except Owner.DoesNotExist:
            return redirect('login')

    return render(request, 'managerpanel/branch_detail.html', {
        'branch': branch,
        'products': products,
    })
