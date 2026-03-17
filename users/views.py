from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterViewSet(generics.CreateAPIView):
  queryset = CustomUser.objects.all()
  serializer_class = CustomUserSerializer
  permission_classes = [AllowAny]


class LoginViewSet(TokenObtainPairView):
  permission_classes = [AllowAny]