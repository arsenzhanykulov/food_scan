from django.urls import path

from apps.user.external_api.apple_api import AppleLoginAPIView
from apps.user.external_api.google_api import GoogleLoginAPIView

urlpatterns = [
    path("google-login/", GoogleLoginAPIView.as_view(), name="google_login_api"),
    path("apple/", AppleLoginAPIView.as_view(), name="apple-login"),
]
