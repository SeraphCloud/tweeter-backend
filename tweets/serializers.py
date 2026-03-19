from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
  author_username = serializers.ReadOnlyField(source='author.username')

  class Meta:
    model = Comment
    fields = ('id', 'author', 'author_username', 'post', 'text', 'created_at')
    read_only_fields = ['author', 'post']

class PostSerializer(serializers.ModelSerializer):
  author_username = serializers.ReadOnlyField(source='author.username')
  comments = CommentSerializer(many=True, read_only=True)
  likes_count = serializers.SerializerMethodField()
  liked_by_me: bool = serializers.SerializerMethodField() # type: ignore

  class Meta:
    model = Post
    fields = (
      'id', 'author', 'author_username', 'text', 'created_at',
      'likes_count', 'liked_by_me', 'comments'
    )
    read_only_fields = ['author']

  def get_likes_count(self, obj):
    return obj.likes.count()

  def get_liked_by_me(self, obj):
    request = self.context.get('request')
    
    if request and request.user.is_authenticated:
      return obj.likes.filter(pk=request.user.pk).exists()
    return False
