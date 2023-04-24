from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post, Comment
from knox.models import AuthToken

CustomUser = get_user_model()

class CommentAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.token = AuthToken.objects.create(self.user)[1]
        self.post = Post.objects.create(description='Test Description', contact_info='Test Contact Info', user_info=self.user)
        self.comment = Comment.objects.create(content='Test Comment', post=self.post, user=self.user)
    def test_new_comment(self):
        url = reverse('new_comment')
        data = {'post_id': self.post.id, 'content': 'Test Comment'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        print(response)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], data['content'])
        self.assertEqual(response.data['post'], data['post_id'])
        self.assertEqual(response.data['user'], self.user.id)

    def test_update_comment(self):
        url = reverse('update_comment', args=[self.comment.id])
        data = {'content': 'Updated Comment'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        print(response)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], data['content'])
        self.assertTrue(response.data['is_edited'])

    def test_delete_comment(self):
        url = reverse('delete_comment', args=[self.comment.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        print(response)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        comment = Comment.objects.get(id=self.comment.id)
        self.assertTrue(comment.is_deleted)

    def test_get_comments(self):
        url = reverse('get_comments', args=[self.post.id])
        response = self.client.get(url)
        print(response)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.comment.id)

    def test_get_user_comments(self):
        url = reverse('get_user_comments', args=[self.user.id])
        response = self.client.get(url)
        print(response)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.comment.id) 