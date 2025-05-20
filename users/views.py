from rest_framework import status, generics, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from .serializers import CustomUserSerializer, LoginSerializer, CustomPasswordResetSerializer
from orders.serializers import OrderSerializer
from orders.models import Order
from reviews.models import Review
from services.models import Service
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework.decorators import api_view

User = get_user_model()


# Manage all users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]


#  Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


# Login View with JWT
class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"error": "Invalid Credentials"}, status=400)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                }
            })

        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


# Email Verification
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get('token')
        if not token:
            return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            access_token = AccessToken(token)
            user = get_object_or_404(User, id=access_token['user_id'])
            user.is_verified = True
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        except (ExpiredSignatureError, InvalidTokenError):
            return Response({"error": "Invalid or expired token"}, status=400)


# Buyer Dashboard 
class BuyerDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.select_related('service').filter(buyer=request.user).values(
            'service__title', 'status', 'order_date'
        )
        reviews = Review.objects.select_related('service').filter(buyer=request.user).values(
            'service__title', 'rating', 'comment', 'created_at'
        )

        return Response({
            'order_history': list(orders),
            'reviews': list(reviews),
        })


# Seller Dashboard
class SellerDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        services = Service.objects.select_related('category').filter(seller=request.user).values(
            'title', 'price', 'category__name'
        )
        orders = Order.objects.select_related('buyer').filter(service__seller=request.user).values(
            'buyer__email', 'status', 'order_date'
        )
        reviews = Review.objects.select_related('buyer').filter(service__seller=request.user).values(
            'buyer__email', 'rating', 'comment', 'created_at'
        )

        return Response({
            'posted_services': list(services),
            'order_history': list(orders),
            'reviews': list(reviews),
        })





@api_view(['GET'])
def freelancer_dashboard(request):
    data = {
        "task_bids_won": 22,
        "jobs_applied": 195,
        "profile_views": [120, 135, 150, 145, 160, 170, 180],
        "timeline_labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    }
    return Response(data)


# class CustomPasswordResetView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = CustomPasswordResetSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data['email']
#         User = serializer.Meta.model if hasattr(serializer.Meta, 'model') else None

#         users = User.objects.filter(email=email) if User else None
#         if not users or users.count() == 0:
#             return Response({"email": ["User with this email does not exist."]}, status=status.HTTP_400_BAD_REQUEST)

#         for user in users:
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             token = default_token_generator.make_token(user)
#             reset_url = f"http://yourfrontend.com/reset-password-confirm/{uid}/{token}/"

#             # Send reset email
#             send_mail(
#                 subject="Password Reset",
#                 message=f"Click the link to reset your password: {reset_url}",
#                 from_email="no-reply@yourdomain.com",
#                 recipient_list=[email],
#                 fail_silently=False,
#             )

#         return Response({"detail": "Password reset e-mail has been sent."}, status=status.HTTP_200_OK)