from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from .validators import validate_file_size

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_time = models.PositiveIntegerField(help_text="Delivery time in days")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')
