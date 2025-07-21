from django.shortcuts import render, redirect, get_object_or_404
from brandpanel.models import Brand, Branch, Owner
from brandpanel.forms import BranchForm

def branch_create_view(request):
    owner = Owner.objects.get(user=request.user)
    brand = Brand.objects.get(owner=owner)

    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.brand = brand
            branch.save()
            return redirect('brand:dashboard')
    else:
        form = BranchForm()

    return render(request, 'brandpanel/branch_form.html', {'form': form})

def branch_update_view(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    form = BranchForm(request.POST or None, instance=branch)

    if form.is_valid():
        form.save()
        return redirect('brand:dashboard')

    return render(request, 'brandpanel/branch_form.html', {'form': form})

def branch_delete_view(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    branch.delete()
    return redirect('brand:dashboard')
