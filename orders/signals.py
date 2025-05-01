from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from notifications.models import Notification

@receiver(post_save, sender=Order)
def create_notification_for_order_update(sender, instance, **kwargs):
    if instance.status == 'completed':
        message = f"Your order {instance.id} has been completed."
    elif instance.status == 'in_progress':
        message = f"Your order {instance.id} is now in progress."
    else:
        message = f"Your order {instance.id} is still pending."

    Notification.objects.create(
        user=instance.buyer,
        order=instance,
        message=message
    )
    Notification.objects.create(
        user=instance.service.seller,
        order=instance,
        message=message
    )
