from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.external_api.apple_api import AppleLoginAPIView
from apps.user.external_api.google_api import GoogleLoginAPIView

urlpatterns = [
    path("google-login/", GoogleLoginAPIView.as_view(), name="google_login_api"),
    path("apple/", AppleLoginAPIView.as_view(), name="apple-login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
