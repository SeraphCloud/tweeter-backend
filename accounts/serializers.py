from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Profile, Follow

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
  username = serializers.CharField(source='user.username', read_only=True)
  avatar = serializers.ImageField(required=False, allow_null=True)
  avatar_url = serializers.SerializerMethodField()
  following_ids = serializers.SerializerMethodField()
  followers_count = serializers.SerializerMethodField()
  following_count = serializers.SerializerMethodField()

  class Meta:
    model = Profile
    fields = ["id", "username", "display_name", "avatar", "avatar_url",
              "following_ids", "followers_count", "following_count"]
    read_only_fields = ["id", "username", "avatar_url", "following_ids",
                       "followers_count", "following_count"]

  def get_avatar_url(self, obj):
    """Retorna a URL completa do avatar para exibição no frontend"""
    if not obj.avatar:
      return None
    request = self.context.get('request')
    if request:
      return request.build_absolute_uri(obj.avatar.url)
    return obj.avatar.url
  
  def get_following_ids(self, obj):
    return list(Follow.objects.filter(follower=obj.user).values_list('following_id', flat=True))
  
  def get_followers_count(self, obj):
    return Follow.objects.filter(following=obj.user).count()
  
  def get_following_count(self, obj):
    return Follow.objects.filter(follower=obj.user).count()

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ['id','username', 'email', 'password']
    read_only_fields = ['id']

  def create(self, validated_data):
    return User.objects.create_user(
      username=validated_data['username'],
      email=validated_data.get('email', ''),
      password=validated_data['password'],
    )