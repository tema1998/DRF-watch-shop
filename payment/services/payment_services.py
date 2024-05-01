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



