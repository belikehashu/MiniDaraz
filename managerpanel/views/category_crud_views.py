from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from products.models.category import Category
from managerpanel.forms import CategoryForm
from managerpanel.models import Manager
from brandpanel.models.owner import Owner
from brandpanel.models.brand import Brand
from brandpanel.models.branch import Branch
from managerpanel.decorators import is_owner_or_manager_required

@is_owner_or_manager_required
def category_list_view(request):
    user = request.user
    branch_id = request.GET.get('branch')
    branch = None
    categories = []

    try:
        manager = Manager.objects.get(user=user)
        if branch_id:
            try:
                branch = manager.branches.get(id=branch_id)
            except Branch.DoesNotExist:
                branch = None  # invalid branch
            categories = Category.objects.filter(branch=branch) if branch else Category.objects.filter(branch__in=manager.branches.all())
        else:
            categories = Category.objects.filter(branch__in=manager.branches.all())

    except Manager.DoesNotExist:
        try:
            owner = Owner.objects.get(user=user)
            if branch_id:
                try:
                    branch = Branch.objects.get(id=branch_id, brand=owner.brand)
                except Branch.DoesNotExist:
                    branch = None
                categories = Category.objects.filter(branch=branch) if branch else Category.objects.filter(branch__brand=owner.brand)
            else:
                categories = Category.objects.filter(branch__brand=owner.brand)
        except Owner.DoesNotExist:
            return redirect('login')  # only if both manager & owner not found

    return render(request, 'managerpanel/category_list.html', {
        'categories': categories,
        'branch': branch
    })


@is_owner_or_manager_required
def category_create_view(request):
    user = request.user
    branch_id = request.POST.get('branch') or request.GET.get('branch')
    branch = None

    try:
        manager = Manager.objects.get(user=user)
        if branch_id:
            branch = manager.branches.get(id=branch_id)
    except Manager.DoesNotExist:
        try:
            owner = Owner.objects.get(user=user)
            if branch_id:
                branch = Branch.objects.get(id=branch_id, brand=owner.brand)
        except:
            branch = None

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid() and branch:
            category = form.save(commit=False)
            category.branch = branch
            category.save()
            return redirect(f"{reverse('manager:category_list')}?branch={branch.id}")
    else:
        form = CategoryForm()

    return render(request, 'managerpanel/category_form.html', {
        'form': form,
        'branch_id': branch.id if branch else ''
    })

@is_owner_or_manager_required
def category_update_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    branch = category.branch
    user = request.user

    try:
        if Manager.objects.filter(user=user, branches=branch).exists() or \
           (Owner.objects.filter(user=user).exists() and branch.brand == Owner.objects.get(user=user).brand):
            form = CategoryForm(request.POST or None, instance=category)
            if form.is_valid():
                form.save()
                return redirect(f"{reverse('manager:category_list')}?branch={branch.id}")
        else:
            return redirect('login')
    except:
        return redirect('login')

    return render(request, 'managerpanel/category_form.html', {
        'form': form,
        'branch_id': branch.id
    })

@is_owner_or_manager_required
def category_delete_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    branch = category.branch
    user = request.user

    try:
        if Manager.objects.filter(user=user, branches=branch).exists() or \
           (Owner.objects.filter(user=user).exists() and branch.brand == Owner.objects.get(user=user).brand):
            category.delete()
            return redirect(f"{reverse('manager:category_list')}?branch={branch.id}")
        else:
            return redirect('login')
    except:
        return redirect('login')
