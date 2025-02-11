from django.contrib.auth.models import User
from django.test import TestCase

from core.models import Country, Product, Brand, PaymentProcess, Order, OrderProduct, Feedback, Reviews


class CountryTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="test country")

    def test_model(self):
        self.assertEqual(self.country.name, "test country")
        self.assertEqual(str(self.country), "test country")

    def test_name_label(self):
        field_label = self.country._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Country')

    def test_name_length(self):
        max_length = self.country._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)


class BrandTest(TestCase):
    def setUp(self):
        country = Country.objects.create(name="test country")
        self.brand = Brand.objects.create(name="test brand", country=country, description='test description')

    def test_model(self):
        self.assertEqual(self.brand.name, "test brand")
        self.assertEqual(self.brand.description, "test description")
        self.assertEqual(str(self.brand), "test brand")

    def test_name_label(self):
        field_label = self.brand._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Brand')

    def test_name_length(self):
        max_length = self.brand._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_country_label(self):
        field_label = self.brand._meta.get_field('country').verbose_name
        self.assertEquals(field_label, 'Country')

    def test_description_label(self):
        field_label = self.brand._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Description')


class ProductTest(TestCase):
    def setUp(self):
        country = Country.objects.create(name="test country")
        brand = Brand.objects.create(name="test brand", country=country, description='test description')
        user = User.objects.create(username='user1', password='pass1')
        self.product = Product.objects.create(
            brand = brand,
            model="watch watch 1",
            description='desc',
            price=100,
            is_available=True,
            image = '1.png',
            quantity=2,
            author = user,
            discount=5,
        )

    def test_model(self):
        self.assertEqual(self.product.model, "watch watch 1")
        self.assertEqual(self.product.price, 100)
        self.assertEqual(str(self.product), "watch watch 1")
        self.assertEqual(self.product.slug, "watch-watch-1")
        self.assertEqual(self.product.description, "desc")
        self.assertEqual(self.product.is_available, True)
        self.assertEqual(self.product.quantity, 2)
        self.assertEqual(self.product.discount, 5)
        self.assertEqual(self.product.price_with_discount, 95)
        self.product.quantity = 0
        self.product.save()
        self.assertFalse(self.product.is_available)

    def test_brand_label(self):
        field_label = self.product._meta.get_field('brand').verbose_name
        self.assertEquals(field_label, 'Brand')

    def test_model_label(self):
        field_label = self.product._meta.get_field('model').verbose_name
        self.assertEquals(field_label, 'Model')

    def test_model_length(self):
        max_length = self.product._meta.get_field('model').max_length
        self.assertEquals(max_length, 200)

    def test_slug_label(self):
        field_label = self.product._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'Slug')

    def test_description_label(self):
        field_label = self.product._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Description')

    def test_image_label(self):
        field_label = self.product._meta.get_field('image').verbose_name
        self.assertEquals(field_label, 'Image')

    def test_created_at_label(self):
        field_label = self.product._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Date of creation')

    def test_author_label(self):
        field_label = self.product._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'Author')

    def test_price_label(self):
        field_label = self.product._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'Price, $')

    def test_is_available_label(self):
        field_label = self.product._meta.get_field('is_available').verbose_name
        self.assertEquals(field_label, 'Availability')

    def test_quantity_label(self):
        field_label = self.product._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'Quantity')

    def test_discount_label(self):
        field_label = self.product._meta.get_field('discount').verbose_name
        self.assertEquals(field_label, 'Discount, %')


class PaymentProcessTest(TestCase):
    def setUp(self):
        self.payment_process = PaymentProcess.objects.create(payment_id="234", payment_url='payment_url')

    def test_model(self):
        self.assertEqual(self.payment_process.payment_id, "234")
        self.assertEqual(self.payment_process.payment_url, "payment_url")
        self.assertEqual(str(self.payment_process), f"Payment #{self.payment_process.payment_id}")
        self.assertEqual(self.payment_process.status, False)

    def test_payment_id_label(self):
        field_label = self.payment_process._meta.get_field('payment_id').verbose_name
        self.assertEquals(field_label, 'ID of created payment')

    def test_payment_id_length(self):
        max_length = self.payment_process._meta.get_field('payment_id').max_length
        self.assertEquals(max_length, 255)

    def test_payment_url_label(self):
        field_label = self.payment_process._meta.get_field('payment_url').verbose_name
        self.assertEquals(field_label, 'URL of created payment')

    def test_payment_url_length(self):
        max_length = self.payment_process._meta.get_field('payment_url').max_length
        self.assertEquals(max_length, 255)


class OrderTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='user1', password='pass1')
        payment_process = PaymentProcess.objects.create(payment_id="234", payment_url='payment_url')
        self.order = Order.objects.create(user=user, payment_process=payment_process)
        country = Country.objects.create(name="test country")
        brand = Brand.objects.create(name="test brand", country=country, description='test description')
        product = Product.objects.create(
            brand=brand,
            model="watch watch 1",
            description='desc',
            price=100,
            is_available=True,
            image='1.png',
            quantity=2,
            author=user,
            discount=5,
        )
        OrderProduct.objects.create(product=product, quantity=2, user=user, order=self.order)

    def test_model(self):
        self.assertEqual(self.order.is_ordered, False)
        self.assertEqual(str(self.order), f"Order #{self.order.id}")
        self.assertEqual(self.order.order_price, 190)

    def test_user_label(self):
        field_label = self.order._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_is_ordered_label(self):
        field_label = self.order._meta.get_field('is_ordered').verbose_name
        self.assertEquals(field_label, 'Is ordered')

    def test_payment_process_label(self):
        field_label = self.order._meta.get_field('payment_process').verbose_name
        self.assertEquals(field_label, 'Payment')

    def test_created_at_label(self):
        field_label = self.order._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Date of creation')


class OrderProductTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='user1', password='pass1')
        payment_process = PaymentProcess.objects.create(payment_id="234", payment_url='payment_url')
        order = Order.objects.create(user=user, payment_process=payment_process)
        country = Country.objects.create(name="test country")
        brand = Brand.objects.create(name="test brand", country=country, description='test description')
        product = Product.objects.create(
            brand=brand,
            model="watch watch 1",
            description='desc',
            price=100,
            is_available=True,
            image='1.png',
            quantity=2,
            author=user,
            discount=5,
        )
        self.order_product = OrderProduct.objects.create(product=product, quantity=2, user=user, order=order)

    def test_model(self):
        self.assertEqual(self.order_product.quantity, 2)
        self.assertEqual(str(self.order_product), f"{self.order_product.user}'s ordered product")
        self.assertEqual(self.order_product.total_price, 190)

    def test_product_label(self):
        field_label = self.order_product._meta.get_field('product').verbose_name
        self.assertEquals(field_label, 'Product')

    def test_quantity_label(self):
        field_label = self.order_product._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'Quantity')

    def test_user_label(self):
        field_label = self.order_product._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_order_label(self):
        field_label = self.order_product._meta.get_field('order').verbose_name
        self.assertEquals(field_label, 'Order')


class FeedbackTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='user1', password='pass1')
        self.feedback = Feedback.objects.create(user=user, image="1.jpg", review='text')

    def test_model(self):
        self.assertEqual(self.feedback.image, "1.jpg")
        self.assertEqual(self.feedback.review, "text")
        self.assertEqual(str(self.feedback), f"{self.feedback.user}'s feedback ID={self.feedback.pk}")

    def test_user_label(self):
        field_label = self.feedback._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_image_label(self):
        field_label = self.feedback._meta.get_field('image').verbose_name
        self.assertEquals(field_label, 'Image')

    def test_review_label(self):
        field_label = self.feedback._meta.get_field('review').verbose_name
        self.assertEquals(field_label, 'Review')

    def test_review_length(self):
        max_length = self.feedback._meta.get_field('review').max_length
        self.assertEquals(max_length, 1000)

    def test_created_at_label(self):
        field_label = self.feedback._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Date of creation')


class ReviewsTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='user1', password='pass1')
        country = Country.objects.create(name="test country")
        brand = Brand.objects.create(name="test brand", country=country, description='test description')
        product = Product.objects.create(
            brand=brand,
            model="watch watch 1",
            description='desc',
            price=100,
            is_available=True,
            image='1.png',
            quantity=2,
            author=user,
            discount=5,
        )
        self.review = Reviews.objects.create(product=product, user=user, text='text')

    def test_model(self):
        self.assertEqual(self.review.text, "text")
        self.assertEqual(str(self.review), f"{self.review.user}'s review ID={self.review.pk}")

    def test_product_label(self):
        field_label = self.review._meta.get_field('product').verbose_name
        self.assertEquals(field_label, 'Product')

    def test_user_label(self):
        field_label = self.review._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_text_label(self):
        field_label = self.review._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'Review text')

    def test_created_at_label(self):
        field_label = self.review._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Date of creation')
