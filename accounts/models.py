from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  display_name = models.CharField(max_length=50, blank=True)
  avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

  def __str__(self):
    return self.display_name or self.user.username
  
class Follow(models.Model):
  follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
  following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['follower','following'],
        name='unique_follow',
      )
    ]

  def __str__(self):
    return f'{self.follower} follows {self.following}'

