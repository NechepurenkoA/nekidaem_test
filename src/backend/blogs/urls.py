from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from blogs.api_views import BlogViewSet, PostViewSet

router = DefaultRouter()
router.register(r"news", PostViewSet, basename="posts")
router.register(r"blogs", BlogViewSet, basename="follow_blog")

urlpatterns = [
    path(f"{settings.API_V1_PREFIX}/", include(router.urls)),
]
