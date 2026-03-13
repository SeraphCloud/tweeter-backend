from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
  foto_perfil = CloudinaryField('imagem', blank=True, null=True)

  def __str__(self):
    return self.username
  