from django.test import SimpleTestCase
from django.urls import reverse, resolve

from core import views


class UrlsTest(SimpleTestCase):

    def test_products_list(self):
        path = reverse('core:products-list')
        self.assertEquals(resolve(path).func.cls, views.ProductViewSet)

    def test_register(self):
        path = reverse('core:register')
        self.assertEquals(resolve(path).func.view_class, views.RegisterView)

    def test_profile(self):
        path = reverse('core:profile')
        self.assertEquals(resolve(path).func.view_class, views.ProfileView)

    def test_feedback(self):
        path = reverse('core:feedback')
        self.assertEquals(resolve(path).func.view_class, views.FeedbackView)

    def test_reviews(self):
        path = reverse('core:reviews')
        self.assertEquals(resolve(path).func.view_class, views.ReviewsView)

    def test_reviews_for_product(self):
        path = reverse('core:reviews_for_product', kwargs={"product_slug": "test-slug"})
        self.assertEquals(resolve(path).func.view_class, views.ReviewsView)

    def test_cart(self):
        path = reverse('core:cart')
        self.assertEquals(resolve(path).func.view_class, views.Cart)

    def test_cart_add(self):
        path = reverse('core:cart_add')
        self.assertEquals(resolve(path).func.view_class, views.AddProductToCart)

    def test_cart_remove(self):
        path = reverse('core:cart_remove')
        self.assertEquals(resolve(path).func.view_class, views.RemoveProductFromCart)