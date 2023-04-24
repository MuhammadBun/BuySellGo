from .serializer import CommunitySerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes 
from account.models import CustomUser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Community
from post.models import Post
from post.serializer import PostSerializer
from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_communities(request):
    try:
        # Get all community instances from the database
        communities = Community.objects.all()

        # Serialize the data
        serializer = CommunitySerializer(communities, many=True)

        # Return a success response with the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        # Return an error response if something goes wrong
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_community(request, pk):
    try:
        # Get the community instance from the database using the pk
        community = Community.objects.get(pk=pk)

        # Serialize the data
        serializer = CommunitySerializer(community)

        # Return a success response with the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Community.DoesNotExist:
        # Return a 404 not found response if the community does not exist
        return Response({'error': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Return an error response if something goes wrong
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_community(request):
    try:
        user = request.user
        user = CustomUser.objects.get(id=user.id) 
        name = request.data.get('name')
        admin =  user
 
        description = request.data.get('description')
        if not description:
            return Response({'error': 'A Community description cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        if (not name) :
            return Response({'error': 'A Community name cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)
        if Community.objects.filter(name=name).exists():
            return Response({'error': 'A Community with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            community = Community.objects.create(admin=admin , description=description, name=name)
            community.members.add(admin)

        serializer = CommunitySerializer(community)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_member_to_community(request):
    try:
        # Get the user and community IDs from the request data
        community_id = request.data.get('community_id')
        # Get the user and community instances from the database
        community = Community.objects.get(id=community_id)

 
        # Check if the user is already a member of the community
        if community.members.filter(id=request.user.id).exists():
            return Response({'error': 'User is already a member of the community.'}, status=status.HTTP_400_BAD_REQUEST)
        community.members.add(request.user)
        # Return a success response
        return Response({'success': 'User added as a member of the community.'}, status=status.HTTP_200_OK)
    except Exception as e:
        # Return an error response if something goes wrong
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post_for_community(request):
    try:
        # Get the post data from the request
        description = request.data.get('description')
        contact_info = request.data.get('contact_info')
        user_info = request.user
        post_type = request.data.get('post_type')
        state = request.data.get('state')
        community_id = request.data.get('community_id')

        # Get the user and community instances from the database
        user = request.user
        community = Community.objects.get(id=community_id)

        # Check if the user is a member of the community
        if user not in community.members.all():
            return Response({'error': 'Only members of the community can publish posts.'}, status=status.HTTP_403_FORBIDDEN)

        # Create a new Post instance
        post = Post.objects.create(
            description=description,
            contact_info=contact_info,
            user_info=user_info,
            post_type=post_type,
            state=state,
 
        )
        community.posts.add(post)

        serializer = PostSerializer(post, data=request.data)
        
        # Call is_valid before accessing serialized data
        if serializer.is_valid():
            # Return a success response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Return an error response if something goes wrong
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post_for_community(request,community_id,post_id):

    try:
        # Get the post instance from the database
        post = Post.objects.get(id=post_id)
        community = Community.objects.get(id=community_id)

        # Check if the current user is the admin of the community
        if request.user != community.admin:
            return Response({'error': 'Only the admin of the community can delete posts.'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the post is in the community
        if post not in community.posts.all():
            return Response({'error': 'The post is not in this community.'}, status=status.HTTP_400_BAD_REQUEST)
          # Delete the post
        post.delete()

        # Return a success response
        return Response({'success': 'Post deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        # Return an error response if something goes wrong
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_member(request, community_id, user_id):
    try:
        # Get the community and user instances from the database
        community = Community.objects.get(id=community_id)
        user = CustomUser.objects.get(id=user_id)

        # Check if the current user is the admin of the community
        if request.user != community.admin:
            return Response({'error': 'Only the admin of the community can remove members.'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the user being removed is the admin of the community
        if user == community.admin:
            return Response({'error': 'The admin of the community cannot be removed.'}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the user from the community's members
        community.members.remove(user)

        # Return a success response
        return Response({'success': 'Member removed from the community.'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        # Return an error response if something goes wrong
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_community(request, community_id):
    try:
        # Get the community instance from the database
        community = Community.objects.get(id=community_id)

        # Check if the current user is the admin of the community
        if request.user != community.admin:
            return Response({'error': 'Only the admin of the community can delete it.'}, status=status.HTTP_403_FORBIDDEN)
        # Delete all posts associated with the community
        community.posts.all().delete()

        # Remove all members from the community
        community.members.clear()

        # Delete the community
        community.delete()

        # Return a success response
        return Response({'success': 'Community deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        # Return an error response if something goes wrong
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_community(request, pk):
    try:
        # Get the community instance from the database using the pk
        community = Community.objects.get(pk=pk)

        # Check if the current user is the admin of the community
        if request.user != community.admin:
            return Response({'error': 'Only the admin of the community can update it.'}, status=status.HTTP_403_FORBIDDEN)

        # Update the community instance with the data from the request
        serializer = CommunitySerializer(community, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Community.DoesNotExist:
        # Return a 404 not found response if the community does not exist
        return Response({'error': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Return an error response if something goes wrong
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_communities(request):
    try:
        # Get the search query from the request
        query = request.query_params.get('q', '')
 

        # Split the query into individual words
        words = query.split()

        # Create a Q object to represent the search conditions
        search_conditions = Q()
        for word in words:
            search_conditions |= Q(name__icontains=word) | Q(description__icontains=word) | Q(posts__description__icontains=word)
     
        # Get all community instances from the database that match the search conditions
        communities = Community.objects.filter(search_conditions).distinct()
 

        # Serialize the data
        serializer = CommunitySerializer(communities, many=True)

        # Return a success response with the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        # Return an error response if something goes wrong
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 