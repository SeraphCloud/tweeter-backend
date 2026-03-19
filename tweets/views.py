from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
  serializer_class = PostSerializer
  
  def get_queryset(self):
    user = self.request.user
    following_ids = user.following.values_list('id', flat=True)
    return Post.objects.filter( # type: ignore
      author__in=list(following_ids) + [user.id]
    ).order_by('-created_at')

  def perform_create(self, serializer):
    serializer.save(author=self.request.user)

  @action(detail=True, methods=['post'])
  def like(self, request, pk=None):
    post = self.get_object()

    if post.likes.filter(pk=request.user.pk).exists():
      post.likes.remove(request.user)
      return Response({'status': 'unliked'})
    else:
      post.likes.add(request.user)
      return Response({'status': 'liked'})

  @action(detail=True, methods=['post'])
  def comment(self, request, pk=None):
    post = self.get_object()
    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save(author=request.user, post=post)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)