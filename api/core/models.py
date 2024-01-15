from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User


class Product(models.Model):
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    slug = models.SlugField()
    description = RichTextUploadingField()
    image = models.ImageField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.model


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    review = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)