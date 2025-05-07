from rest_framework import serializers
from .models import Review
from users.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'buyer', 'service', 'rating', 'comment', 'created_at']
        read_only_fields = ['buyer', 'service']
