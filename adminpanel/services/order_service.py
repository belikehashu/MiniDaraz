from notifications.services.notification_service import create_notification

def notify_order_status_update(order):
    create_notification(order.user, f"Your order #{order.id} has been {order.status}.")
