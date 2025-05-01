from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Service, Category, ServiceImage
from .serializers import ServiceSerializer, CategorySerializer, ServiceImageSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdminOrReadOnly
from django.shortcuts import get_object_or_404
from django.db.models import Count

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.select_related('category', 'seller').prefetch_related('images').all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category']
    ordering_fields = ['price']
    search_fields = ['title', 'description']
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(service_count = Count('service')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ServiceImageViewSet(ModelViewSet):
    serializer_class = ServiceImageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ServiceImage.objects.select_related('service').filter(service_id=self.kwargs.get('service_pk'))

    def perform_create(self, serializer):
        service = get_object_or_404(Service, id=self.kwargs.get('service_pk'))
        serializer.save(service=service)
