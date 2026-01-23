from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
  author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
  content = models.TextField(max_length=280)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.author} - {self.content[:30]}'

class Like(models.Model):
  user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
  post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'post'],
        name='unique_like'
      )
    ]

  def __str__(self):
    return f'{self.user} likes {self.post}'

class Comment(models.Model):
  user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
  post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
  text = models.TextField(max_length=500)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.user} on {self.post}: {self.text[:30]}'