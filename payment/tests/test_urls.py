from django.test import SimpleTestCase
from django.urls import reverse, resolve

from payment import views


class UrlsTest(SimpleTestCase):

    def test_payment_create(self):
        path = reverse('payment:create_payment')
        self.assertEquals(resolve(path).func.cls, views.CreatePaymentView)

    def test_payment_cancel(self):
        path = reverse('payment:cancel_payment')
        self.assertEquals(resolve(path).func.cls, views.CancelPaymentView)

    def test_payment_accept(self):
        path = reverse('payment:accept_payment')
        self.assertEquals(resolve(path).func.cls, views.AcceptPaymentView)