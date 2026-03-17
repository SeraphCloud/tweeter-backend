from django.urls import path
from .views import RegisterViewSet, LoginViewSet


urlpatterns = [
  path('register/', RegisterViewSet.as_view(), name='user-register'),
  path('login/', LoginViewSet.as_view(), name='user-login'),
  path('register', RegisterViewSet.as_view(), name='user-register-no-slash'),
  path('login', LoginViewSet.as_view(), name='user-login-no-slash'),
]