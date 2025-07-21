from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from managerpanel.models import Manager

@login_required
def manager_dashboard_view(request):
    try:
        manager = Manager.objects.get(user=request.user)
    except Manager.DoesNotExist:
        return redirect('managerpanel:login')

    branches = manager.branches.all()
    return render(request, 'managerpanel/dashboard.html', {
        'manager': manager,
        'branches': branches,
    })
