from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
  likes_count = serializers.IntegerField(read_only=True)
  is_liked = serializers.SerializerMethodField()
  comments_count = serializers.IntegerField(read_only=True)

  class Meta:
    model = Post
    fields = ["id", "author", "content", "created_at", "likes_count", "comments_count"]
    read_only_fields = ["id", "author", "created_at", "likes_count", "comments_count"]
    
  def get_is_liked(self, obj):
    user = self.context['request'].user
    if not user.is_authenticated:
      return False
    return obj.likes.filter(user=user).exists()
    

class CommentSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Comment
    fields = ["id", "user", "post", "text", "created_at"]
    read_only_fields = ["id", "user", "created_at"]