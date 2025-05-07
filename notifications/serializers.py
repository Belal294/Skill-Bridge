from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(source='order.id', read_only=True)
    order_status = serializers.CharField(source="order.status", read_only=True)
    class Meta:
        model = Notification
        fields = ['id', 'user', 'order', 'message', 'is_read', 'created_at', 'order_status']