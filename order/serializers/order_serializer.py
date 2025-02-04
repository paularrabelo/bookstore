from rest_framework import serializers

from order.models import Order
from product.models import Product
from product.serializers import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False, many=True)
    products_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['product', 'total', 'user', 'products_id']
        extra_kwargs = {'product': {'required': False}}

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total
    
    

    def create(self, validated_data):
        products = validated_data.pop('products_id')
        user = validated_data.pop('user')

        order = Order.objects.create(user=user)
        for product in products:
            order.product.add(product)

        return order