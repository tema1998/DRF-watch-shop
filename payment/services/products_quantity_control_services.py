from django.db import transaction
from django.db.transaction import atomic

from core.models import OrderProduct, Order


def decrease_quantity_of_products_in_shop(order: Order):
    ordered_products_qs = order.ordered_products.all()
    with transaction.atomic():
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
