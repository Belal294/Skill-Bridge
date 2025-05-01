from django.db import models
from django.contrib.auth import get_user_model
from services.models import Service
import uuid

User = get_user_model()

class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'), 
    ]

    buyer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    status = models.CharField(
        max_length=20, 
        choices=ORDER_STATUS, 
        default='pending'
    )
    order_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.uuid} | {self.buyer.username} → {self.service.title} [{self.status}]"

    class Meta:
        ordering = ['-order_date']
        verbose_name = "Order"
        verbose_name_plural = "Orders"
