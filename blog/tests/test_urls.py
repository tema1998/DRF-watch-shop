from django.test import SimpleTestCase
from django.urls import reverse, resolve

from blog import views


class UrlsTest(SimpleTestCase):

    def test_news_list(self):
        path = reverse('blog:news-list')
        self.assertEquals(resolve(path).func.cls, views.NewsViewSet)

    def test_like(self):
        path = reverse('blog:like', kwargs={'pk': 1})
        self.assertEquals(resolve(path).func.view_class, views.LikeNews)

    def test_comments_list(self):
        path = reverse('blog:comments', kwargs={'pk': 1})
        self.assertEquals(resolve(path).func.view_class, views.CommentsList)

    def test_comments_create(self):
        path = reverse('blog:comments-create')
        self.assertEquals(resolve(path).func.view_class, views.CommentCreate)

    def test_comments_update_delete(self):
        path = reverse('blog:comments-update-delete', kwargs={'pk': 1})
        self.assertEquals(resolve(path).func.view_class, views.CommentUpdateDelete)
