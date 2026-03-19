from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = CustomUser
    fields = ('id', 'username', 'email', 'password', 'foto_perfil', 'following')

  def create(self, validated_data):
    password = validated_data.pop('password')
    user = CustomUser(**validated_data)
    user.set_password(password)
    user.save()
    return user