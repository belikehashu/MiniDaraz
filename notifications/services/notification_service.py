from notifications.models import Notification

def create_notification(user, message, product=None):
    Notification.objects.create(user=user, message=message, product=product)

def get_user_notifications(user):
    return Notification.objects.filter(user=user)

def get_unread_count(user):
    return Notification.objects.filter(user=user, is_read=False).count()

def mark_all_as_read(user):
    Notification.objects.filter(user=user, is_read=False).update(is_read=True)
