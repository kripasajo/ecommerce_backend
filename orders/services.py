from django.db import transaction
from rest_framework.exceptions import ValidationError
from decimal import Decimal
import logging

from .models import Order, OrderItem
from products.models import ProductVariant

logger = logging.getLogger(__name__)


def create_order_from_cart(cart, idempotency_key=None):
    if idempotency_key:
        existing_order = Order.objects.filter(
            idempotency_key=idempotency_key
        ).first()

        if existing_order:
            return existing_order
        
    if not cart or not cart.items.exists():
        raise ValidationError("Cart is empty")

    # 👉 ADD EXACTLY HERE

        
    try:
        with transaction.atomic():

            # ✅ Create order
            order = Order.objects.create(
                user=cart.user,
                total_price=Decimal("0.00"),
                status=Order.Status.PENDING,
                idempotency_key=idempotency_key
            )

            total = Decimal("0.00")
            order_items = []

            # ✅ Fetch cart items with related variants
            cart_items = list(
                cart.items.select_related("product_variant")
            )

            # ✅ Extract all variant IDs
            variant_ids = [item.product_variant.id for item in cart_items]
            variant_ids = sorted(set(variant_ids))
            # 🔒 Lock ALL variants in ONE query (IMPORTANT FIX)
            variants = {
                v.id: v
                for v in ProductVariant.objects
                .select_for_update()
                .filter(id__in=variant_ids)
            }

            unique_ids = set(variant_ids) #handles delted products and avoids silent misses
            if len(variants) != len(unique_ids):
                raise ValidationError("Some products are no longer available")
            
            from collections import defaultdict

            requested = defaultdict(int)

            for item in cart_items:
                requested[item.product_variant.id] += item.quantity

            # ✅ validation loop
            # 🔥 NEW VALIDATION LOOP (USE THIS INSTEAD)

            for vid, qty in requested.items():
                variant = variants.get(vid)

                if not variant:
                    raise ValidationError("Product not found")

                if qty <= 0:
                    raise ValidationError("Invalid quantity")

                if variant.stock < qty:
                    raise ValidationError(f"Only {variant.stock} available for {variant}")


            for item in cart_items:
                variant = variants[item.product_variant.id]
                quantity = item.quantity
                price = variant.price

                order_items.append(
                    OrderItem(
                        order=order,
                        product_variant=variant,
                        quantity=quantity,
                        price=price,
                        product_name=str(variant)
                    )
                )

                variant.stock -= quantity

                total += quantity * price

            ProductVariant.objects.bulk_update(
                variants.values(),
                ["stock"]
            )

            # ✅ Bulk insert
            OrderItem.objects.bulk_create(order_items)

            # ✅ Update total
            order.total_price = total
            order.save(update_fields=["total_price"])

            cart.items.all().delete()
            return order

    except ValidationError:
        raise

    except Exception as e:
        logger.error(f"Order creation failed for user {cart.user.id}: {str(e)}")
        raise ValidationError("Order processing failed")           