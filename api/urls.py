from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

# 🔹 Views Import
from users.views import (
    RegisterView, VerifyEmailView, LoginView,
    BuyerDashboard, SellerDashboard, UserViewSet
)
from services.views import ServiceViewSet, CategoryViewSet, ServiceImageViewSet
from orders.views import (
    OrderViewSet, payment_cancel, payment_fail, payment_success, create_checkout_session, get_order_by_uuid
)
from notifications.views import NotificationViewSet
from dashboard.views import AdminDashboardView
from reviews.views import ReviewViewSet

# 🔹 Default Router
router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('services', ServiceViewSet, basename='services')
router.register('categories', CategoryViewSet, basename='category')
router.register('orders', OrderViewSet, basename='order')
router.register('notifications', NotificationViewSet, basename='notification')
router.register('reviews', ReviewViewSet, basename='review')

# 🔹 Nested Router for Service Images
services_router = NestedDefaultRouter(router, 'services', lookup='service')
services_router.register('images', ServiceImageViewSet, basename='service-images')

# 🔹 URL Patterns
urlpatterns = [
    # API routes from routers
    path('', include(router.urls)),
    path('', include(services_router.urls)),

    # Auth & User routes
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),

    # Dashboards
    path('buyer-dashboard/', BuyerDashboard.as_view(), name='buyer_dashboard'),
    path('seller-dashboard/', SellerDashboard.as_view(), name='seller_dashboard'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),

    # Order-specific route
    path('orders/<int:pk>/update-status/', OrderViewSet.as_view({'patch': 'update_status'}), name='update-status'),

    # Djoser Authentication
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # Payment URLs
    # path('payment/initiate/', initiate_payment, name="payment-initiate"),
    path('payment/success/', payment_success, name="payment-success"),
    path('payment/cancel/', payment_cancel, name="payment-cancel"),
    path('payment/fail/', payment_fail, name="payment-fail"),
    path('create-checkout-session/', create_checkout_session, name='create-checkout'),
    path('orders/by-uuid/<uuid:uuid>/', get_order_by_uuid),



]
