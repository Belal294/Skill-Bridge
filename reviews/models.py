from django.db import models
from users.models import CustomUser
from services.models import Service
from orders.models import Order

class Review(models.Model):
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)  
    rating = models.PositiveIntegerField(default=1)  
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.buyer.username} - {self.rating} Stars"
