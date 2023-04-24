from django.contrib.auth import get_user_model
from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Notifications
 
from django.contrib.contenttypes.models import ContentType
from post.models import Post
from account.models import CustomUser
class NotificationAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='testpass')
        self.token = AuthToken.objects.create(self.user)[1]

        # Set the authentication credentials for the client
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_create_notification(self):
        # Define the URL and data for the create_notification API endpoint

    
        url = reverse('create_notification')
        data = {
            'recipient': self.user.id,
            'actor': self.user.id,
            'verb': 'test verb',
            'target': "post",
            'target_object_id': 1,
            'read': False
        }

        # Send a POST request to the create_notification API endpoint
        response = self.client.post(url, data)
        print(response,"=======================================")
        # Check that the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the response data contains the expected values
        self.assertEqual(response.data['recipient'], data['recipient'])
        self.assertEqual(response.data['actor'], data['actor'])
        self.assertEqual(response.data['verb'], data['verb'])
        self.assertEqual(response.data['target'], data['target'])
        self.assertEqual(response.data['target_object_id'], data['target_object_id'])
        self.assertEqual(response.data['read'], data['read'])

    def test_list_notifications(self):
        # Define the URL for the list_notifications API endpoint
        url = reverse('list_notifications')

        # Send a GET request to the list_notifications API endpoint
        response = self.client.get(url)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_as_read(self):
        # Create a test notification
       
 
        notification = Notifications.objects.create(
            recipient=self.user.id,
            actor=self.user.id,
            verb='test verb',
            target="post",
            target_object_id=1,
            read=False
        )

        # Define the URL and data for the mark_as_read API endpoint
        url = reverse('mark_as_read')
        data = {
            'notification_id': notification.id
        }

        # Send a POST request to the mark_as_read API endpoint
        response = self.client.post(url, data)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_notification(self):
         # Create a test notification
 
 
         notification = Notifications.objects.create(
             recipient=self.user.id,
             actor=self.user.id,
             verb='test verb',
             target="post",
             target_object_id=1,
             read=False
         )

         # Define the URL and data for the delete_notification API endpoint
         url = reverse('delete_notification')
         data = {
             'notification_id': notification.id
         }

         # Send a DELETE request to the delete_notification API endpoint
         response = self.client.delete(url, data)

         # Check that the response status code is 204 No Content
         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_notification_missing_data(self):
        # Define the URL and data for the create_notification API endpoint
        url = reverse('create_notification')
        data = {}

        # Send a POST request to the create_notification API endpoint
        response = self.client.post(url, data)

        # Check that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_mark_as_read_invalid_id(self):
        # Define the URL and data for the mark_as_read API endpoint
        url = reverse('mark_as_read')
        data = {
            'notification_id': 999
        }

        # Send a POST request to the mark_as_read API endpoint
        response = self.client.post(url, data)

        # Check that the response status code is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_notification_invalid_id(self):
        # Define the URL and data for the delete_notification API endpoint
        url = reverse('delete_notification')
        data = {
            'notification_id': 999
        }

        # Send a DELETE request to the delete_notification API endpoint
        response = self.client.delete(url, data)

        # Check that the response status code is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)