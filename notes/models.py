
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    text = models.TextField()
    priority = models.CharField(max_length=20, choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low")], default="High")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note({self.user.username})"
