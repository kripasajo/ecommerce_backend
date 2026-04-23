from django.db import models


class Inventory(models.Model):
    product_variant = models.OneToOneField(
        "products.ProductVariant",
        on_delete=models.CASCADE,
        related_name="inventory"
    )

    # Total stock available in warehouse
    stock = models.PositiveIntegerField(default=0)

    # Reserved during checkout (not yet confirmed)
    reserved_stock = models.PositiveIntegerField(default=0)

    # Optional: safety buffer (prevent overselling edge cases)
    safety_stock = models.PositiveIntegerField(default=0)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["product_variant"]),
        ]

    def available_stock(self):
        return self.stock - self.reserved_stock - self.safety_stock

    def __str__(self):
        return f"Inventory({self.product_variant})"