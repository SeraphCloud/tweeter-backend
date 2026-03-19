from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
  RegisterViewSet, LoginViewSet, ProfileView,
  FollowView, FollowingListView, FollowersListView
)

urlpatterns = [
  path('register/', RegisterViewSet.as_view(), name='user-register'),
  path('login/', LoginViewSet.as_view(), name='user-login'),
  path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
  path('profile/', ProfileView.as_view(), name='user-profile'),
  path('<int:pk>/follow/', FollowView.as_view(), name='user-follow'),
  path('<int:pk>/followers/', FollowersListView.as_view(), name='user-followers'),
  path('<int:pk>/following/', FollowingListView.as_view(), name='user-following'),
]