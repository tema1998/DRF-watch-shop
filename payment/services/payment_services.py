from yookassa import Payment, Configuration
import uuid

Configuration.account_id = '378591'
Configuration.secret_key = 'test_3LvWNqOjroU0MFy57p03e01ECXGsyAKhWn1vB9lsxYU'


def create_payment():
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
          "value": "2.00",
          "currency": "RUB"
        },
        "payment_method_data": {
          "type": "bank_card"
        },
        "confirmation": {
          "type": "redirect",
          "return_url": "https://www.example.com/return_url"
        },
        "description": "Заказ №72"
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
