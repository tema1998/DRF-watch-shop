from django.db import transaction
from django.db.transaction import atomic

from core.models import OrderProduct, Order


def decrease_quantity_of_products_in_shop(order: Order):
    """
    Service to decrease quantity of products in shop
    by the amount of paid products.
    """

    ordered_products_qs = order.ordered_products.all()
    for product_in_cart in ordered_products_qs:
        product_in_shop = product_in_cart.product
        if product_in_shop.is_available:
            if product_in_shop.quantity >= product_in_cart.quantity:
                product_in_shop.quantity = product_in_shop.quantity - product_in_cart.quantity
                product_in_shop.save()
            elif product_in_shop.quantity == 0:
                product_in_cart.delete()
            else:
                product_in_cart.quantity = product_in_shop.quantity
                product_in_cart.save()
                product_in_shop.quantity = 0
                product_in_shop.save()
        else:
            product_in_cart.delete()


def cancel_decrease_quantity_of_products_in_shop(order: Order):
    """
    Service to cancel decreasing of quantity of products in the shop
    due to order payment creation.
    """

    ordered_products_qs = order.ordered_products.all()
    for product_in_cart in ordered_products_qs:
        product_in_shop = product_in_cart.product
        product_in_shop.quantity += product_in_cart.quantity
        product_in_shop.save()
        if product_in_shop.quantity > 0 and not product_in_shop.is_available:
            product_in_shop.is_available = True
            product_in_shop.save()
