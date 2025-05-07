from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied

from .models import Review
from .serializers import ReviewSerializer
from orders.models import Order
from services.models import Service

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        service_pk = self.kwargs.get('service_pk')
        if not service_pk:
            return Review.objects.none()
        return (
            Review.objects
            .filter(service_id=service_pk)
            .select_related('buyer', 'service', 'order')
            .order_by('-created_at')
        )

    def perform_create(self, serializer):
        service_pk = self.kwargs.get('service_pk')
        user = self.request.user

        order = (
            Order.objects
            .filter(service_id=service_pk, buyer=user, status='completed')
            .order_by('-created_at')
            .first()
        )

        if not order:
            raise PermissionDenied({"error": "You must complete the order before reviewing."})

        if Review.objects.filter(order=order, buyer=user).exists():
            raise PermissionDenied({"error": "You have already reviewed this order."})

        serializer.save(buyer=user, service=order.service, order=order)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def reviewed(self, request):
        user = request.user
        reviewed_services = Service.objects.filter(reviews__buyer=user).distinct()
        service_data = [
            {
                "id": service.id,
                "title": service.title,
            }
            for service in reviewed_services
        ]
        return Response(service_data)

    @action(detail=False, methods=['get'], url_path='my_review', permission_classes=[IsAuthenticated])
    def my_review(self, request, *args, **kwargs):
        user = request.user
        service_pk = self.kwargs.get('service_pk') 

        if not service_pk:
            raise NotFound({"error": "No service specified."})

        try:
            review = Review.objects.get(service_id=service_pk, buyer=user)
        except Review.DoesNotExist:
            raise NotFound({"error": "You have not reviewed this service."})

        serializer = self.get_serializer(review)
        return Response(serializer.data)

