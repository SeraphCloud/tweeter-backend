from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
  likes_count = serializers.IntegerField(read_only=True)
  is_liked = serializers.SerializerMethodField()
  comments_count = serializers.IntegerField(read_only=True)

  author_username = serializers.CharField(source="author.username", read_only=True)
  author_display_name = serializers.SerializerMethodField()
  author_avatar = serializers.SerializerMethodField()

  class Meta:
    model = Post
    fields = ["id", "author", "author_username", "author_display_name", "author_avatar", "content", "created_at", "likes_count", "comments_count", "is_liked"]
    read_only_fields = ["id", "author", "author_username", "author_display_name", "author_avatar", "created_at", "likes_count", "comments_count", "is_liked"]

  def get_is_liked(self, obj):
    request = self.context.get('request')
    if not request or not request.user.is_authenticated:
      return False
    return obj.likes.filter(user=request.user, post=obj).exists()
  
  def get_author_display_name(self, obj):
      profile = getattr(obj.author, "profile", None)
      if not profile:
          return ""
      return getattr(profile, "display_name", "") or ""

  def get_author_avatar(self, obj):
      profile = getattr(obj.author, "profile", None)
      if not profile:
          return None

      avatar = getattr(profile, "avatar", None)
      if not avatar:
          return None

      request = self.context.get("request")
      url = avatar.url
      return request.build_absolute_uri(url) if request else url
  

class CommentSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Comment
    fields = ["id", "user", "post", "text", "created_at"]
    read_only_fields = ["id", "user", "created_at"]