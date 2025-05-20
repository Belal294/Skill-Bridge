from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

# 🔹 Views Import
from users.views import (
    RegisterView, VerifyEmailView, LoginView,
    BuyerDashboard, SellerDashboard, UserViewSet, freelancer_dashboard
)
from services.views import ServiceViewSet, CategoryViewSet, ServiceImageViewSet
from orders.views import (
    OrderViewSet, payment_success, create_checkout_session,
    get_order_by_id, HasOrderedProduct
)
from notifications.views import NotificationViewSet
from dashboard.views import AdminDashboardView
from reviews.views import ReviewViewSet

from notes.views import NoteViewSet

# 🔹 Default Router
router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('services', ServiceViewSet, basename='services')
router.register('categories', CategoryViewSet, basename='categories')
router.register('orders', OrderViewSet, basename='orders')
router.register('notifications', NotificationViewSet, basename='notifications')
router.register('reviews', ReviewViewSet, basename='reviews') 
router.register("notes", NoteViewSet, basename="notes")

# 🔹 Nested Router for services/{id}/images and services/{id}/reviews
services_router = NestedDefaultRouter(router, 'services', lookup='service')
services_router.register('images', ServiceImageViewSet, basename='service-images')
services_router.register('reviews', ReviewViewSet, basename='service-reviews')


# 🔹 URL Patterns
urlpatterns = [
    # ✅ DRF routers
    path('', include(router.urls)),
    path('', include(services_router.urls)),

    # ✅ Authentication & User
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),

    # ✅ Dashboards
    path('buyer-dashboard/', BuyerDashboard.as_view(), name='buyer-dashboard'),
    path('seller-dashboard/', SellerDashboard.as_view(), name='seller-dashboard'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('freelancer-dashboard/', freelancer_dashboard, name='freelancer-dashboard'),

    # ✅ Order-specific & Stripe
    path('orders/<int:pk>/update-status/', OrderViewSet.as_view({'patch': 'update_status'}), name='update-status'),
    path('orders/by-id/<int:order_id>/', get_order_by_id, name='get-order-by-id'),
    path('orders/has-ordered/<int:service_id>/', HasOrderedProduct.as_view(), name='has-ordered'),
    path('create-checkout-session/', create_checkout_session, name='create-checkout'),
    path('payment-success/', payment_success, name='payment-success'),

    # path('auth/users/reset_password/', CustomPasswordResetView.as_view(), name='password_reset'),


    # ✅ Djoser Auth
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
