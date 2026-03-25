from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['is_deleted'] #exclude the is_deleted field from the serializer because we don't want to return it in the response. This field is used internally to filter out deleted products and categories, but it is not relevant to the API clients. By excluding it from the serializer, we can keep our API responses clean and focused on the relevant data.
        fields = '__all__'