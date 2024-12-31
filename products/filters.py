from django_filters import rest_framework as filters

from products.models import Product


class ProductFilter(filters.FilterSet):
    created_at__gt = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte')
    created_at__lt = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte')
    total_price__lte = filters.NumberFilter(
        field_name='total_price', lookup_expr='lte')
    total_price__gte = filters.NumberFilter(
        field_name='total_price', lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['created_at__gt', 'created_at__lt',
                  'total_price__lte', 'total_price__gte']
