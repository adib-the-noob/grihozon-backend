from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView


def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    # Add custom claims to the token
    refresh["user_role"] = user.user_role
    refresh["phone_number"] = user.phone_number
    refresh["is_verified"] = user.is_verified

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user_role": user.user_role,
        "phone_number": user.phone_number,
        "is_verified": user.is_verified,
    }


def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)

    # Add custom claims to the token
    refresh["user_role"] = user.user_role
    refresh["phone_number"] = user.phone_number
    refresh["is_verified"] = user.is_verified

    return str(refresh)


def get_access_token(user):
    refresh = RefreshToken.for_user(user)

    # Add custom claims to the token
    refresh["user_role"] = user.user_role
    refresh["phone_number"] = user.phone_number
    refresh["is_verified"] = user.is_verified

    return str(refresh.access_token)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["user_role"] = user.user_role
        token["phone_number"] = user.phone_number
        token["is_verified"] = user.is_verified

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user_role"] = self.user.user_role
        data["phone_number"] = self.user.phone_number
        data["is_verified"] = self.user.is_verified

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
