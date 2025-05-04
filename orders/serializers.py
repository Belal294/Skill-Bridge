from rest_framework import serializers
from .models import Order
from services.models import Service
from services.serializers import ServiceSerializer

class OrderSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source='service', write_only=True
    )
    is_paid = serializers.BooleanField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'buyer',
            'service',
            'service_id',
            'status',
            'is_paid',        
            'created_at',
            'updated_at',
            'order_date'
        ]
        read_only_fields = ['id', 'buyer', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['buyer'] = self.context['request'].user
        return super().create(validated_data)


class CheckoutSessionSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    service_id = serializers.IntegerField()
