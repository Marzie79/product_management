from rest_framework.response import Response
from rest_framework import (status, permissions, generics)

from authentications.modules.account import refresh
from authentications.serializers import RefreshTokenSerializer


class RefreshTokenView(generics.GenericAPIView):
    """Update refresh and access token of an account."""
    permission_classes = [permissions.AllowAny]
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=refresh(
            serializer.validated_data['refresh_token']),
            status=status.HTTP_200_OK)
