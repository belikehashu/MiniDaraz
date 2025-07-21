from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from brandpanel.models import Owner, Brand, Branch
from managerpanel.models.manager import Manager

def is_owner(user):
    return user.is_authenticated and user.role == 'owner'

@login_required(login_url='brand:seller_login')
@user_passes_test(is_owner, login_url='brand:seller_login')
def owner_dashboard_view(request):
    owner = Owner.objects.get(user=request.user)
    brand = Brand.objects.get(owner=owner)
    branches = Branch.objects.filter(brand=brand)
    managers = Manager.objects.filter(user__role='manager', branches__brand=brand).distinct()

    return render(request, 'brandpanel/dashboard.html', {
        'owner': owner,
        'brand': brand,
        'branches': branches,
        'managers': managers,
    })
