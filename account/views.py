from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializer import CreateUserSerializer, UpdateUserSerializer, LoginSerializer , UserSerializer ,CustomUserSerializer
from knox import views as knox_views
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from post.models import Post
from post.serializer import PostSerializer
from community.models import Community
from community.serializer import CommunitySerializer
from django.db.models import Q
 
from django.utils.http import   urlsafe_base64_decode
from django.utils.encoding import  force_str  
from .utils import generate_token
from django.shortcuts import render, redirect
from django.urls import reverse
 

 
 

def login_user(request):
    return render(request, 'login.html')

class CreateUserAPI(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class UpdateUserAPI(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer


class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def search_users(request):
    query = request.query_params.get('q')
    if query:
        # Search for CustomUser objects
        users = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(bio__icontains=query)
        )
        user_serializer = CustomUserSerializer(users, many=True)
    
        # Return the search results
        return Response({
            'users': user_serializer.data,
        })
    else:
        return Response({'error': 'Missing search query'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_user(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    rating = request.data.get('rating')
    if rating is not None:
        try:
            rating = int(rating)
        except ValueError:
            return Response({'error': 'Invalid rating value'}, status=status.HTTP_400_BAD_REQUEST)

        if 1 <= rating <= 5:
            user.rating_count += 1
            user.rating_sum += rating
            user.save()
            average_rating = user.rating_sum / user.rating_count
            return Response({'average_rating': average_rating})
        else:
            return Response({'error': 'Rating must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Missing rating value'}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['GET'])
def search(request):
    query = request.query_params.get('q')
    if query:
        # Search for CustomUser objects
        users = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(bio__icontains=query)
        )
        user_serializer = CustomUserSerializer(users, many=True)

        # Search for Post objects
        posts = Post.objects.filter(
            Q(description__icontains=query)
        )
        post_serializer = PostSerializer(posts, many=True)

        # Search for Community objects
        communities = Community.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        community_serializer = CommunitySerializer(communities, many=True)

        # Return the search results
        return Response({
            'users': user_serializer.data,
            'posts': post_serializer.data,
            'communities': community_serializer.data,
        })
    else:
        return Response({'error': 'Missing search query'}, status=status.HTTP_400_BAD_REQUEST)