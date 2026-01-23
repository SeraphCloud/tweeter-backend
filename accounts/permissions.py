from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
  """
  Só permite edição se o profile pertencer ao usuário logado.
  """

  def has_object(self, request, view, obj):
    # Leituras são liberadas
    if request.method in permissions.SAFE_METHODS:
      return True
    # Escritas liberadas se o dono do profile for o user
    owner = getattr(obj, "author", None) or getattr(obj, "user", None)
    return owner == request.user