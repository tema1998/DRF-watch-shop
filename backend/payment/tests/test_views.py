from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase

from core.models import Order, Country, Brand, Product, OrderProduct, Reviews, Feedback, PaymentProcess


class TestCoreAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass1')
        token_response = self.client.post(reverse('token'), data={'username': 'user1', 'password': 'pass1'}, format='json')
        self.access_token = token_response.data['access']
        self.order = Order.objects.create(user=self.user)
        self.country = Country.objects.create(name="test country")
        self.brand = Brand.objects.create(name="test brand", country=self.country, description='test description')
        self.product = Product.objects.create(
            brand=self.brand,
            model="watch watch 1",
            description='desc',
            price=100,
            is_available=True,
            image='1.png',
            quantity=2,
            author=self.user,
            discount=5,
        )
        self.order_product = OrderProduct.objects.create(product=self.product, quantity=1, user=self.user, order=self.order)
        self.review = Reviews.objects.create(product=self.product, user=self.user, text='text')
        self.feedback = Feedback.objects.create(user=self.user, image="1.jpg", review='text')

    # Test CreatePaymentView
    def test_create_payment(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse('payment:create_payment')
        data = {'username': 'user2', 'password': 'pass', 'password2': 'pass'}
        res = self.client.post(url, data, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    # Test CreatePaymentView
    def test_cancel_payment(self):
        self.payment = PaymentProcess.objects.create(payment_id='123', payment_url='url')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse('payment:create_payment')
        res = self.client.post(url, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
