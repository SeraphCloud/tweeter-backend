from django.db.models import Count, Q
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Follow
from accounts.permissions import IsOwnerOrReadOnly
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer

# View de Posts
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
      qs = super().get_queryset()
      return qs.annotate(
        likes_count=Count("likes", distinct=True),
        comments_count=Count("comments", distinct=True),
      ).order_by("-created_at")

    def perform_create(self, serializer):
      serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
       user = request.user

       # Usuários que o user logado segue
       following_ids = Follow.objects.filter(
          follower=user
       ).values_list('following_id', flat=True)

       queryset = self.get_queryset().filter(Q(author_id__in=following_ids) | Q(author=user))

       serializer = self.get_serializer(queryset, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
  
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def all_posts(self, request):
      """
      Retorna todos os posts públicos para a página de Explore.
      Inclui informação sobre se o usuário logado está seguindo o autor.
      """
      queryset = self.get_queryset()
      serializer = self.get_serializer(queryset, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
       post = self.get_object()
       like, created = Like.objects.get_or_create(user=request.user, post=post)

       if created:
          return Response({'detail': 'Liked'}, status=status.HTTP_201_CREATED)
       return Response({'detail': 'Already Liked'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def dislike(self, request, pk=None):
       post = self.get_object()
       deleted, _ = Like.objects.filter(user=request.user, post=post).delete()

       if deleted:
          return Response({'detail': 'Disliked'}, status=status.HTTP_200_OK)
       return Response({'detail': 'Not liked yet'}, status=status.HTTP_400_BAD_REQUEST)

# View de Comments
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
      qs = super().get_queryset()
      post_id = self.request.query_params.get('post')
      
      if post_id is not None:
        qs = qs.filter(post_id=post_id)
      return qs
    
    def perform_create(self, serializer):
      serializer.save(user=self.request.user)