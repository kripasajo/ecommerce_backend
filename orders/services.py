from .models import Order, OrderItem

def create_order_from_cart(cart):
    # create order
    order = Order.objects.create(
        user=cart.user,
        total_price=0
    )

    total = 0

    # loop through cart items
    for item in cart.items.all():
        variant = item.product_variant
        quantity = item.quantity
        price = variant.price

        # create order item
        OrderItem.objects.create(
            order=order,
            product_variant=variant,
            quantity=quantity,
            price=price,
            product_name=str(variant)
        )

        # calculate total
        total += quantity * price

    # update order total
    order.total_price = total
    order.save()

    # clear cart
    cart.items.all().delete()

    return order