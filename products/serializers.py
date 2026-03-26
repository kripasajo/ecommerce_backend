from rest_framework import serializers
from .models import Product, Category, ProductVariant


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['is_deleted'] #exclude the is_deleted field from the serializer because we don't want to return it in the response. This field is used internally to filter out deleted products and categories, but it is not relevant to the API clients. By excluding it from the serializer, we can keep our API responses clean and focused on the relevant data.
        
        


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['is_deleted'] #exclude the is_deleted field from the serializer because we don't want to return it in the response. This field is used internally to filter out deleted products and categories, but it is not relevant to the API clients. By excluding it from the serializer, we can keep our API responses clean and focused on the relevant data.
        

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        exclude = ['is_deleted']   # internal field hidden
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value