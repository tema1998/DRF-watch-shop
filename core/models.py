from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils.text import slugify


from unidecode import unidecode


class Country(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = RichTextUploadingField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, unique=True)
    description = RichTextUploadingField()
    image = models.ImageField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField(default=0)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    review = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)


class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text