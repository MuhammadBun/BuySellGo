from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from knox.models import AuthToken
from .models import Chat, CustomUser

class ChatAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sender = CustomUser.objects.create(email='sender@example.com', password='password')
        self.receiver = CustomUser.objects.create(email='receiver@example.com', password='password')
        self.token = AuthToken.objects.create(self.sender)[1]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_new_chat(self):
        url = reverse('new_chat')
        data = {'receiver_id': self.receiver.id, 'content': 'Hello!'}
        response = self.client.post(url, data)
        print(response, '-------------response-------------')
        print(response.data, '-------------response data-------------')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['sender'], self.sender.id)
        self.assertEqual(response.data['receiver'], self.receiver.id)
        self.assertEqual(response.data['message'], 'Hello!')

    def test_new_chat_missing_data(self):
        url = reverse('new_chat')
        data = {}
        response = self.client.post(url, data)
        print(response, '-------------response-------------')
        print(response.data, '-------------response data-------------')
        self.assertEqual(response.status_code, 400)

    def test_get_chats(self):
        Chat.objects.create(sender=self.sender, receiver=self.receiver, message='Hello!')
        Chat.objects.create(sender=self.receiver, receiver=self.sender, message='Hi!')
        url = reverse('get_chats')
        response = self.client.get(url)
        print(response, '-------------response-------------')
        print(response.data, '-------------response data-------------')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_mark_as_read(self):
        chat = Chat.objects.create(sender=self.sender, receiver=self.receiver, message='Hello!')
        self.client.force_authenticate(user=self.receiver)
        url = reverse('mark_as_read')
        data = {'chat_id': chat.id}
        response = self.client.post(url, data)
        print(response, '-------------response-------------')
        print(response.data, '-------------response data-------------')
        self.assertEqual(response.status_code, 200)
        chat.refresh_from_db()
        self.assertTrue(chat.is_read)

    def test_mark_as_read_invalid_chat(self):
        url = reverse('mark_as_read')
        data = {'chat_id': 999}
        response = self.client.post(url, data)
        print(response, '-------------response-------------')
        print(response.data, '-------------response data-------------')
        self.assertEqual(response.status_code, 400)

    def test_mark_as_read_invalid_user(self):
        chat = Chat.objects.create(sender=self.sender, receiver=self.receiver, message='Hello!')
        url = reverse('mark_as_read')
        data = {'chat_id': chat.id}
        response = self.client.post(url,data)