from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils.text import slugify


from unidecode import unidecode


class Country(models.Model):
    """
    Model for storing manufacturer country.
    """

    name = models.CharField(max_length=200, verbose_name="Country")

    def __str__(self):
        return self.name


class Brand(models.Model):
    """
    Model for storing brand.
    """

    name = models.CharField(max_length=200, verbose_name="Brand")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Country")
    description = RichTextUploadingField(blank=True, verbose_name="Description")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Model for storing product.
    """

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Brand")
    model = models.CharField(max_length=200, verbose_name="Model")
    slug = models.SlugField(blank=True, unique=True, verbose_name="Slug")
    description = RichTextUploadingField(verbose_name="Description")
    image = models.ImageField(verbose_name="Image")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date of creation")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Price, rub")
    is_available = models.BooleanField(default=True, verbose_name="Availability")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    discount = models.IntegerField(default=0, verbose_name="Discount, %")

    def __str__(self):
        return self.model

    @property
    def price_with_discount(self):
        price_with_discount = self.price * (100-self.discount)/100
        return price_with_discount

    def save(self, *args, **kwargs):
        """
        Add slug to model if it was not filled.
        Check availability: if quantity<1 then is_available=False.
        """
        if not self.slug:
            self.slug = slugify(unidecode(str(self.model)))
        if self.quantity == 0:
            self.is_available = False

        super().save(*args, **kwargs)


class PaymentProcess(models.Model):
    payment_id = models.CharField(max_length=255, verbose_name="ID of created payment")
    payment_url = models.CharField(max_length=255, verbose_name="URL of created payment")
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date of creation")

    def __str__(self):
        return f"Payment #{self.payment_id}"


class Order(models.Model):
    """
    Model for the orders of user.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    is_ordered = models.BooleanField(default=False, verbose_name="Is ordered")
    payment_process = models.ForeignKey(PaymentProcess, null=True, on_delete=models.SET_NULL, related_name="order",
                                        verbose_name='Payment', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date of creation")

    def __str__(self):
        return f"Order #{self.id}"

    @property
    def order_price(self):
        order_price = 0
        for order in self.ordered_products.all():
            order_price += order.total_price
        return order_price


class OrderProduct(models.Model):
    """
    Model for items of order.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="ordered_products", verbose_name="Order")

    @property
    def total_price(self):
        return self.product.price_with_discount * self.quantity

    def __str__(self):
        return f"{self.user}'s ordered product"


class Feedback(models.Model):
    """
    Model for storing feedback to site.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    image = models.ImageField(blank=True, verbose_name="Image")
    review = models.CharField(max_length=1000, verbose_name="Review")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date of creation")

    def __str__(self):
        return f"{self.user}'s feedback ID={self.pk}"


class Reviews(models.Model):
    """
    Model for storing reviews to products.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Product")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="User")
    text = models.TextField(verbose_name="Review text")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date of creation")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user}'s review ID={self.pk}"
