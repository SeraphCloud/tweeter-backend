from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'tweets', PostViewSet, basename='post')

urlpatterns = router.urls