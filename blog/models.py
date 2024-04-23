from django.contrib.auth.models import User
from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.utils.text import slugify
from unidecode import unidecode


class News(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    text = RichTextUploadingField()
    image = models.ImageField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Add slug to model if it was not filled.
        """
        if not self.slug:
            self.slug = slugify(unidecode(str(self.title)))
        super().save(*args, **kwargs)
