from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework import status
from knox.models import AuthToken

class CreateUserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create-user')
        self.valid_data = {
            'email': 'test@example.com',
            'password': 'Test1234Ahemdgood',
            'username': 'testuser',
            'bio': 'Test bio',
            'contact_info': 'Test contact info',
            'image': '',
        }
        self.invalid_data = {
            'email': 'test@example.com',
            'password': 'test',
            'username': '',
            'bio': '',
            'contact_info': '',
            'image': '',
        }

    def test_create_user_success(self):
        response = self.client.post(self.url, self.valid_data)
        print(response.status_code)
        print(response.data,'-------------Valid')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email=self.valid_data['email']).exists())

    def test_create_user_failure(self):
        response = self.client.post(self.url, self.invalid_data)
        print(response.status_code)
        print(response.data,'-------------Invalid')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
class SearchUsersTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = CustomUser.objects.create(username='testuser1', email='test1@example.com', bio='test bio 1')
        self.user2 = CustomUser.objects.create(username='testuser2', email='test2@example.com', bio='test bio 2')

    def test_search_users(self):
        # Test search by username
        url = reverse('search_users') + '?q=testuser1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['users']), 1)
        self.assertEqual(response.data['users'][0]['username'], 'testuser1')

        # Test search by email
        url = reverse('search_users') + '?q=test2@example.com'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['users']), 1)
        self.assertEqual(response.data['users'][0]['email'], 'test2@example.com')
        print(response.status_code,'For Email')
        print(response.data,'For Email')
        # Test search by bio
        url = reverse('search_users') + '?q=bio'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['users']), 2)
        print(response.status_code,'For bio')
        print(response.data,'For bio')
    def test_search_users_missing_query(self):
        # Test missing search query
        url = reverse('search_users')
        response = self.client.get(url)
        print(response.status_code,'For missing search query')
        print(response.data,'For missing search query')       
        self.assertEqual(response.status_code, 400)
        print(response.status_code)
        print(response.data) 

class RateUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = CustomUser.objects.create(username='testuser1', email='test1@example.com')
        self.user2 = CustomUser.objects.create(username='testuser2', email='test2@example.com')
        self.token = AuthToken.objects.create(self.user1)[1]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_rate_user(self):
        # Test valid rating
        url = reverse('rate_user', args=[self.user2.pk])
        data = {'rating': 5}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['average_rating'], 5.0)

        # Test invalid rating value
        data = {'rating': 'invalid'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

        # Test rating out of range
        data = {'rating': 6}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_rate_user_missing_rating(self):
        # Test missing rating value
        url = reverse('rate_user', args=[self.user2.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)

    def test_rate_user_not_found(self):
        # Test user not found
        url = reverse('rate_user', args=[999])
        data = {'rating': 5}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)

