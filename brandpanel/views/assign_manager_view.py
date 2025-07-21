from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from brandpanel.models import Branch
from managerpanel.models import Manager
from brandpanel.forms import AssignManagerForm

def assign_manager_view(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    
    if request.method == 'POST':
        form = AssignManagerForm(request.POST, branch=branch)
        if form.is_valid():
            manager = form.cleaned_data['manager']
            branch.managers.add(manager)
            return redirect('brand:dashboard')
    else:
        form = AssignManagerForm(branch=branch)


    return render(request, 'brandpanel/assign_manager.html', {
        'form': form,
        'branch': branch
    })

@login_required
def remove_manager_view(request, branch_id, manager_id):
    branch = get_object_or_404(Branch, id=branch_id)
    manager = get_object_or_404(Manager, id=manager_id)
    
    if request.method == 'POST':
        branch.managers.remove(manager)
    
    return redirect('brand:dashboard')