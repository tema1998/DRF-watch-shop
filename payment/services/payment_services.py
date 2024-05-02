import os

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from yookassa import Payment, Configuration
import uuid

from core.models import Order, PaymentProcess
from payment.services.products_quantity_control_services import decrease_quantity_of_products_in_shop, \
    cancel_decrease_quantity_of_products_in_shop

Configuration.account_id = os.getenv('YOOKASSA_ACCOUNT_ID', '378591')
Configuration.secret_key = os.getenv('YOOKASSA_SECRET_KEY', 'test_3LvWNqOjroU0MFy57p03e01ECXGsyAKhWn1vB9lsxYU')


def create_payment(serialized_data):
    """
    Service creates payment(Yookassa) object,
    decrease quantity of products in the shop(temporary).
    Returns payment url.
    """

    user = serialized_data['user']
    order = Order.objects.get(
            user=user,
            is_ordered=False,
        )
    return_url = serialized_data.get('return_url')
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
          "value": order.order_price,
          "currency": "RUB"
        },
        "payment_method_data": {
          "type": "bank_card"
        },
        "confirmation": {
          "type": "redirect",
          "return_url": return_url
        },
        'metadata': {
            'order_id': order.id,
            'user_id': user.id,
        },
        'capture': True,
        'refundable': False,
        'description': 'Order #' + str(order.id),
    }, idempotence_key)

    if order.payment_process:
        return order.payment_process.payment_url
    else:
        with transaction.atomic():
            decrease_quantity_of_products_in_shop(order)
            payment_process = PaymentProcess.objects.create(payment_id=payment.id, payment_url=payment.confirmation.confirmation_url)
            order.payment_process = payment_process
            order.save()
            payment_url = payment_process.payment_url
        if payment_url:
            return payment_url
        else:
            return None


def cancel_payment(serialized_data):
    """
    Service cancel payment(Yookassa),
    returns quantity of products in the shop.
    Returns bool.
    """
    user = serialized_data['user']
    order = Order.objects.get(
            user=user,
            is_ordered=False,
        )
    if order.payment_process:
        with transaction.atomic():
            cancel_decrease_quantity_of_products_in_shop(order)
            payment_process = order.payment_process
            payment_process.delete()
            return True
    else:
        return False


def payment_accept_or_cancel(response):
    """
    Service accept or cancel payment(Yookassa),
    returns quantity of products in the shop.
    Returns bool.
    """
    try:
        payment_process = PaymentProcess.objects.get(payment_id=response['object']['id'])
        order = Order.objects.get(
            id=response['object']['metadata']['order_id'],
            user=response['object']['metadata']['user_id'],
            payment_process=payment_process
        )
    except ObjectDoesNotExist:
        print(f"Payment error of order #{response['object']['metadata']['order_id']}")
        return False

    if response['event'] == 'payment.succeeded':
        order.is_ordered = True
        order.save()
        payment_process.status = True
        payment_process.save()

    elif response['event'] == 'payment.canceled':
        with transaction.atomic():
            cancel_decrease_quantity_of_products_in_shop(order)
            payment_process = order.payment_process
            payment_process.delete()
    return True
