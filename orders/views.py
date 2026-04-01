from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from cart.services import get_or_create_cart
from .services import create_order_from_cart
from .serializers import OrderSerializer
from .models import Order


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)

        # ✅ VALIDATION 1: Cart must not be empty
        if not cart.items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Create order
        order = create_order_from_cart(cart)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related(
            'items__product_variant'
        )

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.prefetch_related(
                'items__product_variant'
            ).get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=404
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
