from rest_framework import viewsets, permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied

from .models import Review
from .serializers import ReviewSerializer
from orders.models import Order


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            return Review.objects.filter(service__seller=user)
        elif user.is_staff:
            return Review.objects.all()
        return Review.objects.none()

    def perform_create(self, serializer):
        order_id = self.request.data.get('order')
        order = Order.objects.filter(id=order_id).first()

        if not order:
            raise NotFound({"error": "Order not found."})

        if order.buyer != self.request.user:
            raise PermissionDenied({"error": "You are not authorized to review this order."})

        if order.status != 'completed':
            raise PermissionDenied({"error": "You can only review a completed order."})

        # Prevent multiple reviews for same order
        if Review.objects.filter(order=order, buyer=self.request.user).exists():
            raise PermissionDenied({"error": "You have already reviewed this order."})

        serializer.save(buyer=self.request.user, service=order.service, order=order)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_reviews(self, request):
        reviews = Review.objects.filter(buyer=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
