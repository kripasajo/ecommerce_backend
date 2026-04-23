from django.db import models
from django.conf import settings
from products.models import ProductVariant, BaseModel

class Order(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    idempotency_key = models.CharField(
    max_length=255,
    unique=True,
    null=True,
    blank=True
    )

    def __str__(self):
        return f"Order {self.id} - {self.user}"

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
        ]

class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()
    product_name = models.CharField(max_length=255)    
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_variant} x {self.quantity}"

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product_variant']),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product_variant'],
                name='unique_order_item'
            )
        ]