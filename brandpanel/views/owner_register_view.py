from django.shortcuts import render, redirect
from django.contrib import messages
from users.models.user import User
from brandpanel.forms import OwnerRegisterForm
from brandpanel.models import Owner, Brand

def owner_register_view(request):
    if request.method == 'POST':
        form = OwnerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            owner = Owner.objects.create(user=user, phone=form.cleaned_data['phone'])
            Brand.objects.create(owner=owner, name=form.cleaned_data['brand_name'])

            messages.success(request, "Owner registered successfully. Please login.")
            return redirect('login')
    else:
        form = OwnerRegisterForm()
    
    return render(request, 'brandpanel/owner_register.html', {'form': form})
