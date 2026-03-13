from django.db import models
from django.conf import settings

class Post(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  text = models.CharField(max_length=280)
  created_at = models.DateTimeField(auto_now_add=True)
  likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_posts')

  def __str__(self):
    return f'{self.author.username} - {self.text[:20]}'
  
class Comment(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  text = models.TextField(max_length=280)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Comentário de {self.author.username} no post {self.post.id}'
  