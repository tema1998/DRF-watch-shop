from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import News, Comment


class NewsTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='user1', password='pass1')
        self.news = News.objects.create(title="title text", text="news text", image="123.jpg", author=user)

    def test_model(self):
        self.assertEqual(self.news.title, "title text")
        self.assertEqual(self.news.text, "news text")
        self.assertEqual(self.news.image, "123.jpg")
        self.assertEqual(self.news.slug, "title-text")
        self.assertEqual(str(self.news), "title text")

    def test_slug_label(self):
        field_label = self.news._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'Slug')

    def test_title_label(self):
        field_label = self.news._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Title')

    def test_title_length(self):
        max_length = self.news._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_text_label(self):
        field_label = self.news._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'News text')

    def test_image_label(self):
        field_label = self.news._meta.get_field('image').verbose_name
        self.assertEquals(field_label, 'Image')

    def test_created_at_label(self):
        field_label = self.news._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Date of creation')

    def test_author_label(self):
        field_label = self.news._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'Author')

    def test_likes_label(self):
        field_label = self.news._meta.get_field('likes').verbose_name
        self.assertEquals(field_label, 'Likes')


class CommentTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='user1', password='pass1')
        news = News.objects.create(title="title text", text="news text", image="123.jpg", author=user)
        self.comment = Comment.objects.create(text="comment text", news=news, user=user)

    def test_model(self):
        self.assertEqual(self.comment.text, "comment text")
        self.assertEqual(str(self.comment), f'{self.comment.created_at} - {self.comment.user}')

    def test_user_label(self):
        field_label = self.comment._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_news_label(self):
        field_label = self.comment._meta.get_field('news').verbose_name
        self.assertEquals(field_label, 'News')

    def test_text_label(self):
        field_label = self.comment._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'Comment text')

    def test_created_at_label(self):
        field_label = self.comment._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Date of creation')

