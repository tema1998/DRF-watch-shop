from django.contrib.auth.models import User
from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.utils.text import slugify
from unidecode import unidecode


class News(models.Model):
    """
    Model for storing news.
    """
    slug = models.SlugField(blank=True, unique=True, verbose_name="Slug")
    title = models.CharField(max_length=200, verbose_name="Title")
    text = RichTextUploadingField(verbose_name="News text")
    image = models.ImageField(verbose_name="Image")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date of creation")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")
    likes = models.ManyToManyField(User, blank=True, related_name="news_like", verbose_name='Likes')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Add slug to model if it was not filled.
        """
        if not self.slug:
            self.slug = slugify(unidecode(str(self.title)))
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Model for storing comments to news.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user', verbose_name='User')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comment_news', verbose_name='News')
    text = models.TextField(verbose_name='Comment text')
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date of creation")

    def __str__(self):
        return f'{self.created_at} - {self.user}'
