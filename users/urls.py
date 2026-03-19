from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterViewSet, LoginViewSet

urlpatterns = [
  path('register/', RegisterViewSet.as_view(), name='user-register'),
  path('login/', LoginViewSet.as_view(), name='user-login'),
  path('token/refresh', TokenRefreshView.as_view(), name='token-refresh')
]