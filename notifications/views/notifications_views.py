from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from notifications.services.notification_service import get_user_notifications
from notifications.services.notification_service import get_unread_count
from notifications.services.notification_service import mark_all_as_read

@login_required
def notifications_view(request):
    notifications = get_user_notifications(request.user)
    mark_all_as_read(request.user)
    return render(request, 'notifications/notifications.html', {'notifications': notifications})

@login_required
def unread_notification_count_api(request):
    count = get_unread_count(request.user)
    return JsonResponse({'count': count})

@login_required
def mark_all_read_api(request):
    mark_all_as_read(request.user)
    return JsonResponse({'success': True})
