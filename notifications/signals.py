from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from orders.models import Order

@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, **kwargs):
 
    Notification.objects.create(
        user=instance.service.seller,
        order=instance,
        message=f"Your order (ID: {instance.id}) has been updated to {instance.status}."
    )
    

    Notification.objects.create(
        user=instance.buyer,
        order=instance,
        message=f"Your order (ID: {instance.id}) is now {instance.status}."
    )
