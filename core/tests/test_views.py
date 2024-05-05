from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Order, Country, Brand, Product, OrderProduct, Reviews, Feedback


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

    # Test ProductAPIView
    def test_product(self):
        url = reverse('core:products-list')
        res = self.client.get(url, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    # Test RegisterView
    def test_register(self):
        url = reverse('core:register')
        data = {'username': 'user2', 'password': 'pass', 'password2': 'pass'}
        res = self.client.post(url, data, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    # Test ProfileView
    def test_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse('core:profile')
        res = self.client.get(url, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    # Test FeedbackView
    def test_feedback(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse('core:feedback')
        data = {'review': 'text'}
        res = self.client.post(url, data, format='json')
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    # Test ReviewsView
    def test_reviews(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse('core:reviews')
        data = {'product': self.product.id, 'text': 'text'}
        res = self.client.post(url, data, format='json')
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    # Test ReviewsView(List)
    def test_reviews_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse('core:reviews_for_product', kwargs={'product_slug': self.product.slug})
        res = self.client.get(url, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    # Test Cart
    def test_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse('core:cart')
        res = self.client.get(url, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    # Test AddProductToCart
    def test_add_product_to_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse('core:cart_add')

        data = {'product': self.product.id}
        res = self.client.post(url, data, format='json')
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    # Test RemoveProductFromCart
    def test_remove_product_from_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse('core:cart_add')
        data = {'product': self.product.id}
        res = self.client.post(url, data, format='json')
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

