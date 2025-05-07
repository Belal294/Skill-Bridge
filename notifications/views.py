from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.exceptions import PermissionDenied
from orders.models import Order
from rest_framework.response import Response


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()

       
        if self.request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to view notifications.")

    
        return Notification.objects.filter(user=self.request.user).select_related('user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(is_read=True)
