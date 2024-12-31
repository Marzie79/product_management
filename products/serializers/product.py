from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity', 'owner',
                  'total_price', 'created_at', 'updated_at']
