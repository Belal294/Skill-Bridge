from rest_framework import serializers
from .models import Order
from services.models import Service

class OrderSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'buyer', 'service', 'status', 'created_at', 'updated_at', 'order_date']
        read_only_fields = ['id', 'buyer', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['buyer'] = self.context['request'].user
        return super().create(validated_data)

    # Optional: prevent duplicate orders by the same user for the same service
    # def validate(self, attrs):
    #     buyer = self.context['request'].user
    #     service = attrs.get('service')
    #     if Order.objects.filter(buyer=buyer, service=service).exists():
    #         raise serializers.ValidationError("You have already ordered this service.")
    #     return attrs


class CheckoutSessionSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    product_id = serializers.IntegerField()  # Rename to 'service_id' if needed
