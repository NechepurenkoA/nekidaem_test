from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api/", include("blogs.urls")),
    # path("api/", include("posts.urls")),
]
