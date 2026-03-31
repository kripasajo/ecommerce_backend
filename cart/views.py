from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .services import get_or_create_cart, add_to_cart
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


# ✅ GET CART
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)

        cart = Cart.objects.prefetch_related(
            'items__product_variant'
        ).get(id=cart.id)

        serializer = CartSerializer(cart)
        return Response(serializer.data)


# ✅ ADD TO CART
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)

        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            variant = serializer.validated_data['product_variant']
            quantity = serializer.validated_data['quantity']

            add_to_cart(cart, variant, quantity)

            return Response({"message": "Item added"}, status=201)

        return Response(serializer.errors, status=400)


# ✅ UPDATE ITEM (SECURE)
class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')

        cart = get_or_create_cart(request.user)   # 🔥 important

        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)  # 🔥 FIX
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

        if quantity <= 0:
            return Response({"error": "Invalid quantity"}, status=400)

        cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Updated"})


# ✅ REMOVE ITEM (SECURE)
class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        item_id = request.data.get('item_id')

        cart = get_or_create_cart(request.user)   # 🔥 important

        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)  # 🔥 FIX
            cart_item.delete()
            return Response({"message": "Removed"})
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)