from django.contrib import admin
from .models import Follow, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'display_name')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
  list_display = ('follower', 'following', 'created_at')