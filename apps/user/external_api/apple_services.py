import jwt
from jwt import PyJWKClient
import ssl
import certifi


ssl_context = ssl.create_default_context(cafile=certifi.where())

apple_jwks_client = PyJWKClient(
    "https://appleid.apple.com/auth/keys",
    cache_jwk_set=True,
    lifespan=86400,
    ssl_context=ssl_context
)


def verify_apple_id_token(token):
    try:
        signing_key = apple_jwks_client.get_signing_key_from_jwt(token)

        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience="com.erbol.FoodScanAI",
            issuer="https://appleid.apple.com",
        )
        return data
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception) as e:
        print(f"Apple verification error: {e}")
        return None