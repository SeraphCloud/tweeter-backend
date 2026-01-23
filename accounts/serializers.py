from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Follow

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
  username = serializers.CharField(source='user.username', read_only=True)
  avatar = serializers.ImageField(required=False, allow_null=True)

  class Meta:
    model = Profile
    fields = ["id", "username", "display_name", "avatar"]
    read_only_fields = ["id", "username"]