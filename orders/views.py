from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.conf import settings
from .models import Order
from .serializers import OrderSerializer, CheckoutSessionSerializer
from services.models import Service
from drf_yasg.utils import swagger_auto_schema
import stripe

# Stripe configuration
stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(buyer=user)

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

    @swagger_auto_schema(
        methods=['PATCH'],
        operation_summary="Update order status (for sellers only)",
        operation_description="Allows sellers to update the status of their own services' orders.",
        request_body=OrderSerializer
    )
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        order = self.get_object()
        user = request.user
        new_status = request.data.get('status')

        if not new_status:
            return Response({"error": "Status field is required."}, status=status.HTTP_400_BAD_REQUEST)

        if new_status not in ['pending', 'in_progress', 'completed', 'canceled']:
            return Response({"error": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)

        if order.service.seller != user:
            return Response({"error": "You are not authorized to update this order."}, status=status.HTTP_403_FORBIDDEN)

        if order.status == new_status:
            return Response({"error": "Order is already in the requested status."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        return Response({"message": "Order status updated successfully."}, status=status.HTTP_200_OK)





@swagger_auto_schema(
    method='post',
    operation_summary="Create Stripe Checkout Session",
    request_body=CheckoutSessionSerializer
)

@api_view(['POST'])
def create_checkout_session(request):
    order_uuid = request.data.get("order_uuid")
    service_id = request.data.get("service_id")
    
    print('order_uuid:', order_uuid)

    print('service_id:', service_id)

    try: 
        service = Service.objects.get(id=int(service_id))
    except (Service.DoesNotExist, ValueError, TypeError):
        return Response({"error": "Service not found."}, status=404)

    try:
        order = Order.objects.get(id=int(order_uuid))
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=404)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": service.title,
                    },
                    "unit_amount": int(service.price * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{settings.FRONTEND_URL}/payment/status/?order_uuid={order.uuid}&alert=success",
            cancel_url=f"{settings.FRONTEND_URL}/payment/status/?order_uuid={order.uuid}&alert=cancel",
            metadata={"order_uuid": str(order.uuid)},
        )
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    return Response({"checkout_url": session.url})



@api_view(['POST'])
def payment_success(request):
    order_uuid = request.data.get('order_uuid')

    if not order_uuid:
        return Response({'error': 'Order UUID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(uuid=order_uuid)
        order.status = "in_progress"
        order.is_paid = True
        order.save()
        return Response({'message': 'Payment marked as successful'}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Log the error for debugging purposes
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error updating order {order_uuid}: {e}")
        return Response({'error': 'Failed to update order status due to a server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def get_order_by_uuid(request, uuid):
    try:
        order = Order.objects.get(uuid=uuid)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order)
    return Response(serializer.data)
