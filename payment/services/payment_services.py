from yookassa import Payment, Configuration
import uuid

from core.models import Order

Configuration.account_id = '378591'
Configuration.secret_key = 'test_3LvWNqOjroU0MFy57p03e01ECXGsyAKhWn1vB9lsxYU'


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

    confirmation_url = payment.confirmation.confirmation_url
    return confirmation_url


def payment_acceptance(response):
    # try:
    #     table = BalanceChange.objects.get(
    #         id=response['object']['metadata']['table_id'],
    #     )
    # except ObjectDoesNotExist:
    #     payment_id = response['object']['id']
    #     rollbar.report_message(
    #         f"Can't get table for payment id {payment_id}",
    #         'warning',
    #     )
    #     return False

    if response['event'] == 'payment.succeeded':
        print('SUCCEED')
    elif response['event'] == 'payment.canceled':
        print('CANCEL')
    elif response['event'] == 'payment.waiting_for_capture':
        print('waiting_for_capture')
    return True
