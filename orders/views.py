from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import DatabaseError
from rest_framework.exceptions import ValidationError as DRFValidationError

import logging

from cart.services import get_or_create_cart
from .services import create_order_from_cart
from .serializers import OrderSerializer
from .models import Order

logger = logging.getLogger(__name__)


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)

        # ✅ Validate cart
        if not cart.items.exists():
            return Response(
                {
                    "success": False,
                    "message": "Cart is empty"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = create_order_from_cart(cart)

        # ✅ Business logic errors
        except (DjangoValidationError, DRFValidationError) as e:
            logger.warning(f"Order validation failed for user {request.user.id}: {str(e)}")
            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Database errors
        except DatabaseError as e:
            logger.error(f"Database error for user {request.user.id}: {str(e)}")
            return Response(
                {
                    "success": False,
                    "message": "Something went wrong. Please try again."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # ✅ Unexpected errors
        except Exception as e:
            logger.critical(f"Unexpected error for user {request.user.id}: {str(e)}")
            return Response(
                {
                    "success": False,
                    "message": "Unexpected error occurred"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = OrderSerializer(order)

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = (
            Order.objects
            .filter(user=request.user)
            .select_related('user')
            .prefetch_related('items__product_variant')
            .order_by('-created_at')
        )

        serializer = OrderSerializer(orders, many=True)

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = (
                Order.objects
                .select_related('user')
                .prefetch_related('items__product_variant')
                .get(id=order_id, user=request.user)
            )

        except Order.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Order not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(order)

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )