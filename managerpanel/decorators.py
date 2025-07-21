# managerpanel/decorators.py
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from managerpanel.models.manager import Manager
from brandpanel.models.owner import Owner

def is_owner_or_manager_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        user = request.user
        is_manager = Manager.objects.filter(user=user).exists()
        is_owner = Owner.objects.filter(user=user).exists()
        if is_manager or is_owner:
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper
