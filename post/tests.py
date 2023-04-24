from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from knox.models import AuthToken
from .models import Post
from account.models import CustomUser
from django.urls import reverse

class PostAPITestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(email='testuser@gmail.com', password='testpass')
        self.client = APIClient()

        # Authenticate the test user using Knox
        token = AuthToken.objects.create(self.user)[1]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def test_new_post(self):
        # Test creating a new post
        url = reverse('new_post')
        data = {
            'description': 'Test post',
            'post_type': True,
            'state': True
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the post was created in the database
        post = Post.objects.last()
        self.assertEqual(post.description, 'Test post')
        self.assertEqual(post.post_type, True)
        self.assertEqual(post.state, True)

    def test_new_post_missing_data(self):
        # Test creating a new post with missing data
       url = reverse('new_post')
       data={}
       response = self.client.post(url,data)
       self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_post_invalid_data(self):
        # Test creating a new post with invalid data
 
        url = reverse('new_post')
        data= {
            'description': 'Test post',
            'post_type': 'invalid',
            'state': True
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_post_unauthenticated(self):
        # Test creating a new post while unauthenticated
        client = APIClient()
        url = reverse('new_post')
        data= {
            'description': 'Test post',
            'post_type': 'invalid',
            'state': True
        }
        response = client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_posts_user(self):
        # Create a test post
        Post.objects.create(description='Test post', user_info=self.user)

        # Make a GET request to the get_posts_user API view
        url = reverse('get_posts_user')
        response = self.client.get(url, {'user_id': self.user.id})
 
        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['description'], 'Test post')

    def test_get_posts_user_missing_user_id(self):
        # Make a GET request to the get_posts_user API view without a user ID
        url = reverse('get_posts_user')
        response = self.client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response data
        self.assertEqual(response.data['error'], 'Missing or invalid user ID')

    def test_get_posts_user_unauthorized(self):
        # Create a second test user
        other_user = CustomUser.objects.create_user(email='otheruser@gmail.com', password='testpass')

        # Make a GET request to the get_posts_user API view with the other user's ID
        url = reverse('get_posts_user')
        response = self.client.get(url, {'user_id': other_user.id})

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check the response data
        self.assertEqual(response.data['error'], 'Unauthorized')

    def test_get_post(self):
        # Create a test post
        post = Post.objects.create(description='Test post', user_info=self.user)

        # Make a GET request to the post_pk API view
        url = reverse('post_pk', args=[post.id])
        response = self.client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        self.assertEqual(response.data['description'], 'Test post')

    def test_update_post(self):
        # Create a test post
        post = Post.objects.create(description='Test post', user_info=self.user)

        # Make a PUT request to the post_pk API view
        url = reverse('post_pk', args=[post.id])
        data = {'description': 'Updated post'}
        response = self.client.put(url, data)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        self.assertEqual(response.data['description'], 'Updated post')

    def test_delete_post(self):
        # Create a test post
        post = Post.objects.create(description='Test post', user_info=self.user)

        # Make a DELETE request to the post_pk API view
        url = reverse('post_pk', args=[post.id])
        response = self.client.delete(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the post was deleted from the database
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(pk=post.id)

    def test_get_post_not_found(self):
        # Make a GET request to the post_pk API view with an invalid post ID
        url = reverse('post_pk', args=[999])
        response = self.client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_post_unauthorized(self):
        # Create a second test user
        other_user = CustomUser.objects.create_user(email='otheruser@gmail.com', password='testpass')

        # Create a test post for the other user
        post = Post.objects.create(description='Test post', user_info=other_user)

        # Make a GET request to the post_pk API view with the other user's post ID
        url = reverse('post_pk', args=[post.id])
        response = self.client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post_invalid_data(self):
        # Create a test post
        post = Post.objects.create(description='Test post', user_info=self.user)

        # Make a PUT request to the post_pk API view with invalid data
        url = reverse('post_pk', args=[post.id])
        data = {'description': ''}
        response = self.client.put(url, data)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_posts(self):
            # Create some test posts
            Post.objects.create(description='Test post 1', contact_info='1234567890', user_info=self.user)
            Post.objects.create(description='Test post 2', contact_info='0987654321', user_info=self.user)

            # Make a GET request to the search_posts API view with a search query
            url = reverse('search_posts')
            response = self.client.get(url, {'q': 'post'})

            # Check the response status code
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Check the response data
            self.assertEqual(len(response.data), 2)
            self.assertEqual(response.data[0]['description'], 'Test post 1')
            self.assertEqual(response.data[1]['description'], 'Test post 2')

    def test_post_list(self):
        # Create some test posts
        Post.objects.create(description='Test post 1', contact_info='1234567890', user_info=self.user)
        Post.objects.create(description='Test post 2', contact_info='0987654321', user_info=self.user)

        # Make a GET request to the post_list API view
        url = reverse('post_list')
        response = self.client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['description'], 'Test post 1')
        self.assertEqual(response.data[1]['description'], 'Test post 2')

    def test_add_like(self):
        # Create a test post
        post = Post.objects.create(description='Test post', contact_info='1234567890', user_info=self.user)

        # Make a POST request to the add_like API view
        url = reverse('add_like', args=[post.id])
        response = self.client.post(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        self.assertEqual(response.data['likes'], 1)

        # Check that the post was updated in the database
        post.refresh_from_db()
        self.assertEqual(post.likes, 1)

    def test_remove_like(self):
        # Create a test post with 1 like
        post = Post.objects.create(description='Test post', contact_info='1234567890', user_info=self.user, likes=1)

        # Make a POST request to the remove_like API view
        url = reverse('remove_like', args=[post.id])
        response = self.client.post(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        self.assertEqual(response.data['likes'], 0)

        # Check that the post was updated in the database
        post.refresh_from_db()
        self.assertEqual(post.likes, 0)