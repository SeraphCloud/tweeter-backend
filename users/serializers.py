from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=True)
  followers_count = serializers.SerializerMethodField()
  following_count = serializers.SerializerMethodField()

  class Meta:
    model = CustomUser
    fields = ('id', 'username', 'email', 'password', 'foto_perfil', 'followers_count', 'following_count')

  def get_followers_count(self, obj):
    return obj.followers.count()

  def get_following_count(self, obj):
    return obj.following.count()

  def create(self, validated_data):
    password = validated_data.pop('password')
    user = CustomUser(**validated_data)
    user.set_password(password)
    user.save()
    return user

  def update(self, instance, validated_data):
    password = validated_data.pop('password', None)

    for attr, value in validated_data.items():
      setattr(instance, attr, value)

    if password:
      instance.set_password(password)
    instance.save()

    return instance