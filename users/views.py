from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import CustomUserSerializer


class RegisterViewSet(generics.CreateAPIView):
  queryset = CustomUser.objects.all()
  serializer_class = CustomUserSerializer
  permission_classes = [AllowAny]


class LoginViewSet(TokenObtainPairView):
  permission_classes = [AllowAny]

class ProfileView(generics.RetrieveUpdateAPIView):
  serializer_class = CustomUserSerializer
  parser_classes = [MultiPartParser, FormParser]

  def get_object(self):
    return self.request.user

  def update(self, request, *args, **kwargs):
    kwargs['partial'] = True
    return super().update(request, *args, **kwargs)

class FollowView(APIView):
  def post(self, request, pk):
    target = get_object_or_404(CustomUser, pk=pk)

    if target == request.user:
      return Response(
        {'error': 'Você não pode seguir a si mesmo.'},
        status=status.HTTP_400_BAD_REQUEST
      )

    if request.user.following.filter(pk=target.pk).exists():
      request.user.following.remove(target)
      return Response({'status': 'unfollow'}, status=status.HTTP_200_OK)
    else:
      request.user.following.add(target)
      return Response({'status': 'follow'}, status=status.HTTP_200_OK)

class FollowersListView(generics.ListAPIView):
  serializer_class = CustomUserSerializer

  def get_queryset(self):
    user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
    return user.followers.all()

class FollowingListView(generics.ListAPIView):
  serializer_class = CustomUserSerializer

  def get_queryset(self):
    user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
    return user.following.all()

class UserSearchView(generics.ListAPIView):
  serializer_class = CustomUserSerializer

  def get_queryset(self):
    query = self.request.query_params.get('q','')
    return CustomUser.objects.filter(username__icontains=query)