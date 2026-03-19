from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.db import models


class CustomUser(AbstractUser):
  foto_perfil = CloudinaryField('imagem', blank=True, null=True)
  following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followers')

  def __str__(self):
    return self.username
  