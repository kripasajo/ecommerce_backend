from rest_framework import serializers
from .models import Cart, CartItem
from products.models import ProductVariant
from products.serializers import ProductVariantSerializer

class CartItemSerializer(serializers.ModelSerializer):

    product_variant = ProductVariantSerializer(read_only=True) #for read
    product_variant_id = serializers.PrimaryKeyRelatedField( #for write
        queryset=ProductVariant.objects.all(),
        source='product_variant',
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product_variant','product_variant_id', 'quantity']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value

    def validate(self, data):
        variant = data.get('product_variant')
        quantity = data.get('quantity')

        if variant and quantity:
            if quantity > variant.stock:
                raise serializers.ValidationError({
                     "quantity": f"Only {variant.stock} items available in stock"
                })

        return data

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(
            item.quantity * item.product_variant.price
            for item in obj.items.all()
        )