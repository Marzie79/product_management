from rest_framework.response import Response
from rest_framework import (status, generics)

from authentications.modules.account import logout
from authentications.serializers import RefreshTokenSerializer


class LogoutView(generics.GenericAPIView):
    """Logout an account with blocking her current token."""
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logout(serializer.validated_data['refresh_token'])

        return Response(status=status.HTTP_200_OK)
