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
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Price, $")
    discount = models.IntegerField(default=0, verbose_name="Discount, %")

    def __str__(self):
        return self.model

    def save(self, *args, **kwargs):
        """
        Add slug to model if it was not filled.
        """
        if not self.slug:
            self.slug = slugify(unidecode(str(self.model)))
        super().save(*args, **kwargs)


class Feedback(models.Model):
    """
    Model for storing feedback.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    image = models.ImageField(blank=True, verbose_name="Image")
    review = models.CharField(max_length=1000, verbose_name="Review")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date of creation")


class Reviews(models.Model):
    """
    Model for storing reviews to watches.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text