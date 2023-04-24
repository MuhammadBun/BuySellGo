from .models import  Photos, Post
from .serializer import PostSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes 
from account.models import CustomUser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_like(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if post.likes > 0:
        post.likes -= 1
        post.save()
    return Response({'likes': post.likes})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_like(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    post.likes += 1
    post.save()
    return Response({'likes': post.likes})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
 
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_pk(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check if the user is the creator of the post
    if request.user != post.user_info:
        return Response(status=status.HTTP_403_FORBIDDEN)

    # GET
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # PUT
    elif request.method == 'PUT':
        # Check if the user has the "change_post" permission
        if not request.user.has_perm('post.change_post'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    elif request.method == 'DELETE':
        # Check if the user has the "delete_post" permission
        if not request.user.has_perm('post.delete_post'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_post(request):
    try:
        # Get the authenticated user from the request
        user = request.user

        # Create a new post instance
        post = Post(
            description=request.data.get('description'),
            contact_info=request.data.get('contact_info'),
            post_type=request.data.get('post_type'),
            state=request.data.get('state'),
            user_info=user,
            likes=request.data.get('likes', 0)
        )

        # Validate the post instance
        post_serializer = PostSerializer(post, data=request.data)
        if not post_serializer.is_valid():
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save the post instance
        post_serializer.save()

        # Create and save photo instances from the request data
        for photo_data in request.FILES.getlist('photos'):
            photo = Photos(post=post, image=photo_data)
            photo.save()

        # Return a success response
        return Response(status=status.HTTP_201_CREATED)
    except Exception as e:
        # Return a 500 Internal Server Error response with the error message
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts_user(request):
    # Get the user ID from the request data
    user_id = request.query_params.get('user_id')

    # Check if the user ID is valid
    if not user_id:
        return Response({'error': 'Missing or invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the authenticated user is authorized to access the data
    if request.user.id != int(user_id):
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    # Get the posts for the specified user
    posts = Post.objects.filter(user_info=request.user)
    
    # Serialize the data
    serializer = PostSerializer(posts, many=True)

    # Return a success response with the serialized data
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_posts(request):
    try:
        # Get the search query from the request
        query = request.query_params.get('q', '')
        # Split the query into individual words
        words = query.split()

        # Create a Q object to represent the search conditions
        search_conditions = Q()
        for word in words:
            search_conditions |= Q(description__icontains=word) | Q(contact_info__icontains=word) | Q(user_info__username__icontains=word)

 

        # Get all post instances from the database that match the search conditions
        posts = Post.objects.filter(search_conditions).distinct()
 

        # Serialize the data
        serializer = PostSerializer(posts, many=True)

        # Return a success response with the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        # Return an error response if something goes wrong
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
