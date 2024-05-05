from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import News, Comment


class TestCoreAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass1')
        token_response = self.client.post(reverse('token'), data={'username': 'user1', 'password': 'pass1'}, format='json')
        self.access_token = token_response.data['access']
        self.news = News.objects.create(title="title text", text="news text", image="123.jpg", author=self.user)
        self.comment = Comment.objects.create(text="comment text", news=self.news, user=self.user)

    # Test NewsViewSet
    def test_news(self):
        url = reverse('blog:news-list')
        res = self.client.get(url, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    # Test LikeNews
    def test_like_news(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse('blog:like', kwargs={'pk': self.news.pk})
        res = self.client.post(url, format='json')
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    # Test CommentsList
    def test_comments_list(self):
        url = reverse('blog:comments', kwargs={'pk': self.news.pk})
        res = self.client.get(url, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    # Test CommentsCreate
    def test_comments_create(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse('blog:comments-create')
        data = {'news_id': self.news.pk, 'text': 'text'}
        res = self.client.post(url, data, format='json')
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    # Test CommentsUpdateDelete(update)
    def test_comments_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse('blog:comments-update-delete', kwargs={'pk': self.news.pk})
        data = {'text': 'new text'}
        res = self.client.put(url, data, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    # Test CommentsUpdateDelete(delete)
    def test_comments_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse('blog:comments-update-delete', kwargs={'pk': self.news.pk})
        res = self.client.delete(url, format='json')
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)