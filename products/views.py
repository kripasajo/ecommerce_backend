from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product,Category, ProductVariant
from .serializers import ProductSerializer, CategorySerializer , ProductVariantSerializer


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.active_objects.all()   # ✅ uses custom manager
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]   # ✅ ADD THIS TEMPORARILY

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

#added category api
class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.active_objects.all()   # ✅ use manager
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]   # ✅ ADD THIS TEMPORARILY

class ProductVariantListCreateView(ListCreateAPIView):
    queryset = ProductVariant.active_objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['product', 'size', 'color']
    search_fields = ['sku']
    ordering_fields = ['price', 'stock', 'created_at']