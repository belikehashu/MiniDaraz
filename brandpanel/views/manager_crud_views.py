from django.shortcuts import render, redirect
from users.models.user import User
from brandpanel.models import Owner, Brand
from managerpanel.models import Manager
from brandpanel.forms import ManagerCreateForm

def manager_create_view(request):
    owner = Owner.objects.get(user=request.user)
    brand = Brand.objects.get(owner=owner)

    if request.method == 'POST':
        form = ManagerCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            manager = Manager.objects.create(user=user, phone=form.cleaned_data['phone'])
            
            # ✅ Optional: temporarily link to at least one branch
            first_branch = brand.branches.first()
            if first_branch:
                manager.branches.add(first_branch)

            return redirect('brand:dashboard')
    else:
        form = ManagerCreateForm()

    return render(request, 'brandpanel/manager_form.html', {'form': form})
