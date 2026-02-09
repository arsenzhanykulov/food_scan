import requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema


from apps.user.models import Provider, User

@extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'token': {
                    'type': 'string',
                    'description': 'Google access токен'
                }
            },
            'required': ['token']
        }
    },
    description="Аутентификация через Apple",
    summary="Google Login")
class GoogleLoginAPIView(APIView):
    def post(self, request):
        access_token = request.data.get("token")
        if not access_token:
            return Response(
                {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        google_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        response = requests.get(
            google_url, headers={"Authorization": f"Bearer {access_token}"}
        )

        if response.status_code != 200:
            return Response(
                {"error": "Invalid Google Token"}, status=status.HTTP_400_BAD_REQUEST
            )

        user_data = response.json()
        sub = user_data.get("sub")

        user, created = User.objects.get_or_create(
            sub=sub,
            defaults={
                "email": user_data.get("email"),
                "provider": Provider.GOOGLE,
                "is_active": True,
            },
        )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Success",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_200_OK,
        )
