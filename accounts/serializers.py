from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Follow

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
  username = serializers.CharField(source='user.username', read_only=True)
  avatar = serializers.ImageField(required=False, allow_null=True)
  following_ids = serializers.SerializerMethodField()

  class Meta:
    model = Profile
    fields = ["id", "username", "display_name", "avatar", "following_ids"]
    read_only_fields = ["id", "username"]

  def get_following_ids(self, obj):
    return Follow.objects.filter(follower=obj.user).values_list('following_id', flat=True)

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