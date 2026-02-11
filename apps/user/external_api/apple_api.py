import jwt
from jwt import PyJWKClient
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from apps.user.models import Provider, User
import requests

from .apple_services import verify_apple_id_token


class AppleLoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {"token": {"type": "string"}},
                "required": ["token"],
            }
        },
        summary="Apple Login",
    )
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is required"}, status=400)

        payload = verify_apple_id_token(token)

        if not payload:
            return Response(
                {"error": "Invalid or expired Apple token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user, created = User.objects.get_or_create(
            sub=payload.get("sub"),
            defaults={
                "email": payload.get("email"),
                "provider": Provider.APPLE,
                "is_active": True,
            },
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            "status": "success",
            "is_new_user": created,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        }, status=status.HTTP_200_OK)
