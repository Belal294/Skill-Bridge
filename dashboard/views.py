from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from orders.models import Order
from orders.serializers import OrderSerializer

class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.select_related('buyer', 'service__seller', 'service__category')  # optimization
        serializer = OrderSerializer(orders, many=True)
        return Response({
            "total_orders": orders.count(),
            "orders": serializer.data
        })
