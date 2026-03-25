from rest_framework.generics import ListCreateAPIView
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import AllowAny


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.active_objects.all()   # ✅ uses custom manager
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]   # ✅ ADD THIS TEMPORARILY

