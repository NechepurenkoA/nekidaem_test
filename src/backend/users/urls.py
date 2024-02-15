from django.conf import settings
from django.urls import path
from rest_framework.authtoken import views

urlpatterns = [
    path(f"{settings.API_V1_PREFIX}/obtain-token/", views.obtain_auth_token),
]
