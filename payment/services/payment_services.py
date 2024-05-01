import os

from django.core.exceptions import ObjectDoesNotExist
from yookassa import Payment, Configuration
import uuid

from core.models import Order, PaymentProcess

Configuration.account_id = os.getenv('YOOKASSA_ACCOUNT_ID', '378591')
Configuration.secret_key = os.getenv('YOOKASSA_SECRET_KEY', 'test_3LvWNqOjroU0MFy57p03e01ECXGsyAKhWn1vB9lsxYU')


def create_payment(serialized_data):
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
        payment_process = PaymentProcess.objects.create(payment_id=payment.id, payment_url=payment.confirmation.confirmation_url)
        order.payment_process = payment_process
        order.save()
        return payment_process.payment_url


def payment_acceptance(response):
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
        payment_process.delete()
    return True
