from rest_framework_simplejwt.authentication import (
    JWTAuthentication, InvalidToken, AuthenticationFailed)

from authentications.models import Account


class CustomJWTAuthentication(JWTAuthentication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = Account

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token['user_id']
            is_active = validated_token['is_active']
            user_type = validated_token['user_type']
            email = validated_token['email']
        except KeyError:
            raise InvalidToken(
                'Token contained no recognizable user identification')

        try:
            user = self.user_model(
                user_id=user_id, is_active=is_active, user_type=user_type, email=email)
        except Exception:
            raise AuthenticationFailed('User not found', code='user_not_found')

        if user.is_active != user.IsActiveChoices.ACTIVE.value:
            raise AuthenticationFailed(
                'User is inactive, please contact support', code='user_inactive')

        return user
