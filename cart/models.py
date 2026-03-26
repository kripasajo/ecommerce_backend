from django.db import models
from django.conf import settings
from products.models import ProductVariant
from products.models import BaseModel
from products.models import ActiveManager



class Cart(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts'
    )

    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager() # we can upgrade later

    def __str__(self):
        return f"Cart - {self.user}"
    
    def get_total_price(self):
        return sum(
        item.quantity * item.product_variant.price
        for item in self.items.all()
        )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(is_active=True),
                name='unique_active_cart_per_user'
            )
        ]
        indexes = [
            models.Index(fields=['user']),
        ]

class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    quantity = models.PositiveIntegerField()

    objects = models.Manager()

    def __str__(self):
        return f"{self.product_variant} x {self.quantity}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'product_variant'],
                name='unique_cart_item'
            )
        ]
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['product_variant']),
        ]
