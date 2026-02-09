import jwt
from jwt import PyJWKClient
from rest_framework import status
from rest_framework.permissions import AllowAny
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
                    'description': 'Apple ID токен'
                }
            },
            'required': ['token']
        }
    },
    description="Аутентификация через Apple",
    summary="Apple Login"
)
class AppleLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response(
                {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        apple_keys_url = "https://appleid.apple.com/auth/keys"

        try:
            jwks_client = PyJWKClient(apple_keys_url)
            signing_key = jwks_client.get_signing_key_from_jwt(token)

            data = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience="com.erbol.FoodScanAI",
                issuer="https://appleid.apple.com",
            )

            user, created = User.objects.get_or_create(
                sub=data.get("sub"),
                defaults={
                    "email": data.get("email"),
                    "provider": Provider.APPLE,
                    "is_active": True,
                },
            )

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "status": "success",
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_200_OK,
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.InvalidTokenError as e:
            return Response(
                {"error": f"Invalid token: {str(e)}"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
