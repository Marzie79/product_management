from rest_framework_simplejwt.tokens import RefreshToken

from authentications.models import Account


def test_create_token(user_id, user_type):
    """Generate a token for all tests."""
    user = Account(id=user_id,
                   is_active=True,
                   user_type=user_type,
                   email='test@gmail.com')
    fixture_token = RefreshToken.for_user(user)
    return str(fixture_token.access_token)
