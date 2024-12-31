from rest_framework import serializers


class AuthenticationSerializer(serializers.Serializer):
    """Validate authentication data."""
    email = serializers.EmailField()
    password = serializers.CharField()
