from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from knox.models import AuthToken
from .models import FavoriteList 
from account.models import CustomUser
from community.models import Community
from post.models import Post
from rest_framework import status

class FavoriteListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email='test@example.com', password='testpassword')
        self.token = AuthToken.objects.create(self.user)[1]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
 
    def test_new_favorite_list(self):
        url = reverse('new_favorite_list')

        # Test successful creation of a new favorite list
        response = self.client.post(url, {'title': 'Test List'})
 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test List')

        # Test missing title
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing title')

        # Test adding a post to the favorite list
        post = Post.objects.create(description='Test Post', user_info=self.user)
        response = self.client.post(url, {'title': 'Test List', 'post_id': post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
 
        # Test invalid post_id
        response = self.client.post(url, {'title': 'Test List', 'post_id': 999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid post_id')

    def test_add_to_favorite_list(self):
        favorite_list = FavoriteList.objects.create(title='Test List', user=self.user)

        # Test successful addition of a post to the favorite list
        post = Post.objects.create(description='Test Post', user_info=self.user)
        url = reverse('add_to_favorite_list')
        response = self.client.post(url, {'favorite_list_id': favorite_list.id, 'post_id': post.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 

        # Test missing favorite_list_id
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing favorite_list_id')

        # Test invalid favorite_list_id
        response = self.client.post(url, {'favorite_list_id': 999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid favorite_list_id')

        # Test invalid post_id
        response = self.client.post(url, {'favorite_list_id': favorite_list.id, 'post_id': 999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid post_id')

        # Add more tests here for favorite_users and favorite_communities
    def test_update_favorite_list_title(self):
        favorite_list = FavoriteList.objects.create(title='Test List', user=self.user)

        # Test successful update of favorite list title
        url = reverse('update_favorite_list_title')
        response = self.client.put(url, {'favorite_list_id': favorite_list.id, 'title': 'Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

        # Test missing favorite_list_id
        response = self.client.put(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing favorite_list_id')

        # Test invalid favorite_list_id
        response = self.client.put(url, {'favorite_list_id': 999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid favorite_list_id')

        # Test missing title
        response = self.client.put(url, {'favorite_list_id': favorite_list.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing title')

    def test_get_favorite_lists(self):
        favorite_list1 = FavoriteList.objects.create(title='Test List 1', user=self.user)
        favorite_list2 = FavoriteList.objects.create(title='Test List 2', user=self.user)

        # Test successful retrieval of favorite lists
        url = reverse('get_favorite_lists')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Test List 1')
        self.assertEqual(response.data[1]['title'], 'Test List 2')

        # Test retrieval of favorite lists for a different user
        other_user = CustomUser.objects.create(username='otheruser', password='otherpass')
        other_favorite_list = FavoriteList.objects.create(title='Other Test List', user=other_user)
        self.client.force_authenticate(user=other_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Other Test List')

        # Test retrieval of favorite lists when there are no favorite lists
        FavoriteList.objects.all().delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    def test_get_favorite_list_items(self):
        favorite_list = FavoriteList.objects.create(title='Test List', user=self.user)
        post = Post.objects.create(description='Test Post', user_info=self.user)
        favorite_list.favorite_posts.add(post)

        # Test successful retrieval of favorite list items
        url = reverse('get_favorite_list_items')
        response = self.client.get(url, {'favorite_list_id': favorite_list.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test List')
 

        # Test missing favorite_list_id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing favorite_list_id')

        # Test invalid favorite_list_id
        response = self.client.get(url, {'favorite_list_id': 999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid favorite_list_id')

        # Test permission check
        other_user = CustomUser.objects.create(username='otheruser', password='otherpass')
        self.client.force_authenticate(user=other_user)
        response = self.client.get(url, {'favorite_list_id': favorite_list.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], 'You do not have permission to access this FavoriteList')

    def test_remove_from_favorite_list(self):
        favorite_list = FavoriteList.objects.create(title='Test List', user=self.user)
        post = Post.objects.create(description='Test Post', user_info=self.user)
        favorite_list.favorite_posts.add(post)

        # Test successful removal of a post from the favorite list
        url = reverse('remove_from_favorite_list')
        response = self.client.delete(url, {'favorite_list_id': favorite_list.id, 'post_id': post.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 

        # Test missing favorite_list_id
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing favorite_list_id')

        # Test invalid favorite_list_id
        response = self.client.delete(url, {'favorite_list_id': 999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid favorite_list_id')

        # Test invalid post_id
        response = self.client.delete(url, {'favorite_list_id': favorite_list.id, 'post_id': 999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid post_id')

        # Add more tests here for favorite_users and favorite_communities

    def test_delete_favorite_list(self):
        favorite_list = FavoriteList.objects.create(title='Test List', user=self.user)

        # Test successful deletion of a favorite list
        url = reverse('delete_favorite_list')
        response = self.client.delete(url, {'favorite_list_id': favorite_list.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FavoriteList.objects.filter(id=favorite_list.id).exists())

        # Test missing favorite_list_id
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing favorite_list_id')

        # Test invalid favorite_list_id
        response = self.client.delete(url, {'favorite_list_id': 999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid favorite_list_id')

        # Test permission check
        other_user = CustomUser.objects.create(username='otheruser', password='otherpass')
        other_favorite_list = FavoriteList.objects.create(title='Other Test List', user=other_user)
        self.client.force_authenticate(user=other_user)
    def test_delete_favorite_list_permission_check(self):
        favorite_list = FavoriteList.objects.create(title='Test List', user=self.user)

        # Test permission check
        other_user = CustomUser.objects.create(username='otheruser', password='otherpass')
        self.client.force_authenticate(user=other_user)
        url = reverse('delete_favorite_list')
        response = self.client.delete(url, {'favorite_list_id': favorite_list.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], 'You do not have permission to delete this FavoriteList')