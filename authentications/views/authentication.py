from rest_framework.response import Response
from rest_framework import (status, permissions, generics)

from authentications.modules.account import authenticate
from authentications.serializers import AuthenticationSerializer


class AuthenticationView(generics.GenericAPIView):
    """Login an existing account or signup a new account."""
    permission_classes = [permissions.AllowAny]
    serializer_class = AuthenticationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=authenticate(**serializer.validated_data),
                        status=status.HTTP_200_OK)
