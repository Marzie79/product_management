from django_filters import rest_framework as filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentications.models import Account
from products.filters import ProductFilter
from products.models import Product
from products.serializers import ProductSerializer
from products.permissions import IsOwnerOrManager


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrManager]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'created_at__gt',
                openapi.IN_QUERY,
                description='Enter date in yyyy-mm-dd format',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'created_at__lt',
                openapi.IN_QUERY,
                description='Enter date in yyyy-mm-dd format',
                type=openapi.TYPE_STRING,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.user_type != Account.UserTypeChoices.MANAGER.value:
            return super().get_queryset().filter(owner=self.request.user)

        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrManager]
