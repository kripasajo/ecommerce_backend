from django.db import transaction
from rest_framework.exceptions import ValidationError
from decimal import Decimal
import logging

from .models import Order, OrderItem
from products.models import ProductVariant

logger = logging.getLogger(__name__)


def create_order_from_cart(cart):

    if not cart or not cart.items.exists():
        raise ValidationError("Cart is empty")

    try:
        with transaction.atomic():

            # ✅ Create order
            order = Order.objects.create(
                user=cart.user,
                total_price=Decimal("0.00"),
                status=Order.Status.PENDING
            )

            total = Decimal("0.00")
            order_items = []

            # ✅ Fetch cart items with related variants
            cart_items = list(
                cart.items.select_related("product_variant")
            )

            # ✅ Extract all variant IDs
            variant_ids = [item.product_variant.id for item in cart_items]

            # 🔒 Lock ALL variants in ONE query (IMPORTANT FIX)
            variants = {
                v.id: v
                for v in ProductVariant.objects
                .select_for_update()
                .filter(id__in=variant_ids)
            }

            # ✅ Process items
            for item in cart_items:
                variant = variants.get(item.product_variant.id)

                if not variant:
                    raise ValidationError("Product not found")
               

                quantity = item.quantity
                price = variant.price

                # ✅ Stock validation
                if variant.stock < quantity:
                    raise ValidationError(f"Insufficient stock for {variant}")

                # ✅ Prepare order item
                order_items.append(
                    OrderItem(
                        order=order,
                        product_variant=variant,
                        quantity=quantity,
                        price=price,
                        product_name=str(variant)
                    )
                )

                # ✅ Reduce stock
                variant.stock -= quantity
                variant.save(update_fields=["stock"])

                total += quantity * price

            # ✅ Bulk insert
            OrderItem.objects.bulk_create(order_items)

            # ✅ Update total
            order.total_price = total
            order.save(update_fields=["total_price"])

            # 🔒 Lock cart items before delete (extra safety)
            cart.items.select_for_update().delete()
            return order

    except Exception as e:
        logger.error(f"Order creation failed for user {cart.user.id}: {str(e)}")
        raise