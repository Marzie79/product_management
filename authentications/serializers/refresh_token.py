from rest_framework import serializers


class RefreshTokenSerializer(serializers.Serializer):
    """Validate refresh token data."""
    refresh_token = serializers.CharField()
