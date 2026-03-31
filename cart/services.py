from .models import Cart, CartItem

def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(
        user=user,
        is_active=True
    )
    return cart
def add_to_cart(cart, variant, quantity):
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_variant=variant,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return cart_item