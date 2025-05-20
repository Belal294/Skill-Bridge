from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='text')

    class Meta:
        model = Note
        fields = ['id', 'content', 'priority', 'created_at', 'user']
        read_only_fields = ['user', 'created_at']
