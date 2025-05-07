from rest_framework import serializers
from .models import Service, Category, ServiceImage
from users.serializers import UserSerializer, User


class CategorySerializer(serializers.ModelSerializer):
    service_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name','description', 'service_count']

class ServiceImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ServiceImage
        fields = ['id', 'image']

# class ServiceSerializer(serializers.ModelSerializer):
#     images = ServiceImageSerializer(many=True, read_only=True)

#     class Meta:
#         model = Service
#         fields = ['id', 'title', 'description', 'price', 'category', 'delivery_time', 'created_at', 'images']
#         # fields = '__all__'


class SellerShortSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class ServiceSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)
    seller = SellerShortSerializer(read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'price', 'category', 'delivery_time', 'created_at', 'images', 'seller']
