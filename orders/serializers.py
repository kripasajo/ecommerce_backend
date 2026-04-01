from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductVariantSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product_variant',
            'quantity',
            'price',
            'product_name'
        ]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = [
            'id',
            'total_price',
            'status',
            'items',
            'item_count',
            'created_at'
        ]
        read_only_fields = fields

    def get_item_count(self, obj):
        return obj.items.count()
    