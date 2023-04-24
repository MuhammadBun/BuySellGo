from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from knox.models import AuthToken
from .models import Community 
from account.models import CustomUser
from post.models import Post
class CommunityAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )

        # Create a non-admin test user
        self.non_admin_user = CustomUser.objects.create_user(
            email='nonadmintestuser@example.com',
            password='testpassword'
        )

        # Create a test community
        self.community = Community.objects.create(
            name='Test Community',
            description='This is a test community',
            admin=self.user
        )

        # Authenticate the test user
        token = AuthToken.objects.create(self.user)[1]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def test_get_communities(self):
        # Get the URL for the get_communities view
        url = reverse('get_communities')

        # Make a GET request to the URL
        response = self.client.get(url)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data contains the test community
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Community')
        self.assertEqual(response.data[0]['description'], 'This is a test community')

    def test_get_community(self):
        # Get the URL for the get_community view with the pk of the test community
        url = reverse('get_community', args=[self.community.pk])

        # Make a GET request to the URL
        response = self.client.get(url)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data contains the test community
        self.assertEqual(response.data['name'], 'Test Community')
        self.assertEqual(response.data['description'], 'This is a test community')

    def test_get_community_not_found(self):
        # Get the URL for the get_community view with an invalid pk
        url = reverse('get_community', args=[999])

        # Make a GET request to the URL
        response = self.client.get(url)

        # Assert that the response status code is 404 NOT FOUND
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)   
    def test_new_community(self):
        # Get the URL for the new_community view
        url = reverse('new_community')

        # Create a test community data
        data = {
            'name': 'New Test Community',
            'description': 'This is a new test community'
        }

        # Make a POST request to the URL with the test community data
        response = self.client.post(url, data)

        # Assert that the response status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the response data contains the new community
        self.assertEqual(response.data['name'], 'New Test Community')
        self.assertEqual(response.data['description'], 'This is a new test community')

    def test_new_community_empty_name(self):
        # Get the URL for the new_community view
        url = reverse('new_community')

        # Create a test community data with an empty name
        data = {
            'name': '',
            'description': 'This is a new test community'
        }

        # Make a POST request to the URL with the test community data
        response = self.client.post(url, data)

        # Assert that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_community_empty_description(self):
        # Get the URL for the new_community view
        url = reverse('new_community')

        # Create a test community data with an empty description
        data = {
            'name': 'New Test Community',
            'description': ''
        }

        # Make a POST request to the URL with the test community data
        response = self.client.post(url, data)

        # Assert that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_community_duplicate_name(self):
        # Get the URL for the new_community view
        url = reverse('new_community')

        # Create a test community data with a duplicate name
        data = {
            'name': 'Test Community',
            'description': 'This is a new test community'
        }

        # Make a POST request to the URL with the test community data
        response = self.client.post(url, data)

        # Assert that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_join_member_to_community(self):
        # Get the URL for the join_member_to_community view
        url = reverse('join_member_to_community')

        # Create a test data dictionary with the community ID
        data = {
            'community_id': self.community.id
        }

        # Make a POST request to the URL with the test data
        response = self.client.post(url, data)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_join_member_to_community_already_member(self):
        # Add the test user as a member of the test community
        self.community.members.add(self.user)

        # Get the URL for the join_member_to_community view
        url = reverse('join_member_to_community')

        # Create a test data dictionary with the community ID
        data = {
            'community_id': self.community.id
        }

        # Make a POST request to the URL with the test data
        response = self.client.post(url, data)

        # Assert that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post(self):
        # Add the test user as a member of the test community
        self.community.members.add(self.user)

        # Get the URL for the create_post view
        url = reverse('create_post')

        # Create a test post data dictionary
        data = {
            'description': 'Test Post',
            'contact_info': 'test@example.com',
            'post_type': True,
            'state': True,
            'community_id': self.community.id
        }

        # Make a POST request to the URL with the test post data
        response = self.client.post(url, data)

        # Assert that the response status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_not_member(self):
        # Get the URL for the create_post view
        url = reverse('create_post')

        # Create a test post data dictionary
        data = {
            'description': 'Test Post',
            'contact_info': 'test@example.com',
            'post_type': True,
            'state': True,
            'community_id': self.community.id
        }

        # Make a POST request to the URL with the test post data
        response = self.client.post(url, data)

        # Assert that the response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post(self):
        # Create a test post in the test community
        post = Post.objects.create(
            description='Test Post',
            contact_info='test@example.com',
            user_info=self.user,
            post_type=True,
            state=True,
        )
        self.community.posts.add(post)

        # Set the test user as the admin of the test community
        self.community.admin = self.user
        self.community.save()

        # Get the URL for the delete_post view with the community and post IDs
        url = reverse('delete_post', args=[self.community.id, post.id])

        # Make a DELETE request to the URL
        response = self.client.delete(url)

        # Assert that the response status code is 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_not_admin(self):
        # Create a test post in the test community
        post = Post.objects.create(
            description='Test Post',
            contact_info='test@example.com',
            user_info=self.user,
            post_type=True,
            state=True,
        )
        self.community.posts.add(post)

        # Authenticate the non-admin test user
        token = AuthToken.objects.create(self.non_admin_user)[1]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Get the URL for the delete_post view with the community and post IDs
        url = reverse('delete_post', args=[self.community.id, post.id])

        # Make a DELETE request to the URL
        response = self.client.delete(url)

        # Assert that the response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_not_in_community(self):
        # Create a test post not in the test community
        post = Post.objects.create(
            description='Test Post',
            contact_info='test@example.com',
            user_info=self.user,
            post_type=True,
            state=True,
        )

        # Set the test user as the admin of the test community
        self.community.admin = self.user
        self.community.save()

        # Get the URL for the delete_post view with the community and post IDs
        url = reverse('delete_post', args=[self.community.id, post.id])

        # Make a DELETE request to the URL
        response = self.client.delete(url)

        # Assert that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)    


    def test_remove_member(self):
        # Create a test user to be removed
        user_to_remove = CustomUser.objects.create_user(
            email='testuser2@example.com',
            password='testpassword'
        )

        # Add the test user to be removed as a member of the test community
        self.community.members.add(user_to_remove)

        # Set the test user as the admin of the test community
        self.community.admin = self.user
        self.community.save()

        # Get the URL for the remove_member view with the community and user IDs
        url = reverse('remove_member', args=[self.community.id, user_to_remove.id])

        # Make a DELETE request to the URL
        response = self.client.delete(url)

        # Assert that the response status code is 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_remove_member_not_admin(self):
        # Create a test user to be removed
        user_to_remove = CustomUser.objects.create_user(
            email='testuser2@example.com',
            password='testpassword'
        )

        # Add the test user to be removed as a member of the test community
        self.community.members.add(user_to_remove)

        # Authenticate the non-admin test user
        token = AuthToken.objects.create(self.non_admin_user)[1]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Get the URL for the remove_member view with the community and user IDs
        url = reverse('remove_member', args=[self.community.id, user_to_remove.id])

        # Make a DELETE request to the URL
        response = self.client.delete(url)

        # Assert that the response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_update_community_not_admin(self):
        # Get the URL for the update_community view with the community ID
        url = reverse('update_community', args=[self.community.id])

        # Create a test update data dictionary
        data = {
            'name': 'Updated Test Community',
            'description': 'This is an updated test community'
        }
        token = AuthToken.objects.create(self.non_admin_user)[1]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Make a PUT request to the URL with the test update data
        response = self.client.put(url, data)

        # Assert that the response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_remove_member_admin(self):
        # Set the test user as the admin of the test community
        self.community.admin = self.user
        self.community.save()

        # Get the URL for the remove_member view with the community and user IDs
        url = reverse('remove_member', args=[self.community.id, self.user.id])

        # Make a DELETE request to the URL
        response = self.client.delete(url)

        # Assert that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_community(self):
        # Set the test user as the admin of the test community
        self.community.admin = self.user
        self.community.save()

        # Get the URL for the delete_community view with the community ID
        url = reverse('delete_community', args=[self.community.id])

        # Make a DELETE request to the URL
        response = self.client.delete(url)

        # Assert that the response status code is 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_community_not_admin(self):
        # Authenticate the non-admin test user
        token = AuthToken.objects.create(self.non_admin_user)[1]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Construct the URL for the request using the reverse function
        url = reverse('delete_community', args=[self.community.id])

        # Attempt to delete the community as a non-admin user
        response = self.client.delete(url)

        # Check that the response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_community(self):
        # Set the test user as the admin of the test community
        self.community.admin = self.user
        self.community.save()

        # Get the URL for the update_community view with the community ID
        url = reverse('update_community', args=[self.community.id])

        # Create a test update data dictionary
        data = {
            'name': 'Updated Test Community',
            'description': 'This is an updated test community'
        }

        # Make a PUT request to the URL with the test update data
        response = self.client.put(url, data)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_search_communities_no_results(self):
        # Get the URL for the search_communities view
        url = reverse('search_communities')

        # Add a query parameter to the URL
        url += '?q=NoResults'

        # Make a GET request to the URL
        response = self.client.get(url)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data is an empty list
        self.assertEqual(len(response.data), 0)

    def test_search_communities_multiple_results(self):
        # Create additional test communities
        Community.objects.create(
            name='Test Community 2',
            description='This is another test community',
            admin=self.user
        )
        Community.objects.create(
            name='Test Community 3',
            description='This is yet another test community',
            admin=self.user
        )

        # Get the URL for the search_communities view
        url = reverse('search_communities')

        # Add a query parameter to the URL
        url += '?q=Test'

        # Make a GET request to the URL
        response = self.client.get(url)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data contains all test communities
        self.assertEqual(len(response.data), 3)