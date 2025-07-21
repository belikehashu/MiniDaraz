from django.urls import path
from notifications.views.notifications_views import notifications_view
from notifications.views.notifications_views import unread_notification_count_api
from notifications.views.notifications_views import mark_all_read_api

urlpatterns = [
    path('', notifications_view, name='notifications'),
    path('unread-count/', unread_notification_count_api, name='unread_notification_count'),
    path('mark-read/', mark_all_read_api, name='mark_all_read_api'),
]
