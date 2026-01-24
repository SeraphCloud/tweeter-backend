from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics

from .models import Profile, Follow
from .serializers import ProfileSerializer, RegisterSerializer
from .permissions import IsOwnerOrReadOnly

class RegisterView(generics.CreateAPIView):
  serializer_class = RegisterSerializer
  permission_classes = [permissions.AllowAny]

class ProfileViewSet(viewsets.ModelViewSet):
  queryset = Profile.objects.select_related('user').all()
  serializer_class = ProfileSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

  def get_queryset(self):
    qs = super().get_queryset()
    username = self.request.query_params.get('username')

    if username:
      qs = qs.filter(user__username=username)
    return qs
  
  @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
  def follow(self, request, pk=None):
    profile = self.get_object()
    user_to_follow = profile.user

    if user_to_follow == request.user:
      return Response({'detail': 'Não é possível seguir a si mesmo.'}, status=status.HTTP_400_BAD_REQUEST)
    
    Follow.objects.get_or_create(
      follower=request.user,
      following=user_to_follow,
    )
    return Response({'detail': 'Agora você está seguindo.'}, status=status.HTTP_201_CREATED)
  
  @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
  def unfollow(self, request, pk=None):
    profile = self.get_object()
    user_to_unfollow = profile.user

    if user_to_unfollow == request.user:
      return Response({'detail': 'Não faz sentido deixar de seguir a si mesmo.'}, status=status.HTTP_400_BAD_REQUEST)
    
    deleted, _ = Follow.objects.filter(
      follower=request.user,
      following=user_to_unfollow,
    ).delete()

    if deleted:
      return Response({'detail': 'Deixou de seguir.'}, status=status.HTTP_200_OK)
    return Response({'detail': 'Você não segue esse usuário.'}, status=status.HTTP_400_BAD_REQUEST)
  
  @action(detail=True, methods=['get'])
  def followers(self, request, pk=None):
    profile = self.get_object()
    qs = Follow.objects.filter(following=profile.user).select_related('follower')
    data = [
      {'username': f.follower.username}
      for f in qs
    ]
    return Response(data)
  
  @action(detail=True, methods=['get'])
  def following(self, request, pk=None):
    profile = self.get_object()
    qs = Follow.objects.filter(follower=profile.user).select_related('following')
    data = [
      {'username': f.following.username}
      for f in qs
    ]
    return Response(data)
  
  @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
  def me(self, request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "GET":
      serializer = self.get_serializer(profile)
      return Response(serializer.data)
    
    # PATCH
    serializer = self.get_serializer(profile, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)