from rest_framework.generics import ListCreateAPIView
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.active_objects.all()   # ✅ uses custom manager
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]   # ✅ ADD THIS TEMPORARILY

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
