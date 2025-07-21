def user_role_context(request):
    role = None
    if request.user.is_authenticated:
        if hasattr(request.user, 'owner'):
            role = 'owner'
        elif hasattr(request.user, 'manager'):
            role = 'manager'
        else:
            role = 'user'
    return {'user_role': role}
