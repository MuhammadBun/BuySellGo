from django.shortcuts import render
from post.models import  Photos, Post
from favorite_list.serializer import FavoriteListSerializer 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes 
from account.models import CustomUser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FavoriteList 
from django.core.exceptions import ValidationError
from community.models import Community


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorite_lists(request):
    try:
        user = CustomUser.objects.get(id=request.user.id)
    except (KeyError, CustomUser.DoesNotExist):
        return Response({"error": "Invalid or missing user_id"}, status=status.HTTP_400_BAD_REQUEST)
    
 
    favorite_lists = FavoriteList.objects.filter(user=user)
    favoriteListSerializer = FavoriteListSerializer(favorite_lists, many=True)
    return Response(favoriteListSerializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorite_list_items(request):
    favorite_list_id = request.query_params.get('favorite_list_id')
    if not favorite_list_id:
        return Response({"error": "Missing favorite_list_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        favorite_list = FavoriteList.objects.get(id=favorite_list_id)
    except FavoriteList.DoesNotExist:
        return Response({"error": "Invalid favorite_list_id"}, status=status.HTTP_400_BAD_REQUEST)

    if favorite_list.user != request.user:
        return Response({"error": "You do not have permission to access this FavoriteList"}, status=status.HTTP_403_FORBIDDEN)

    favoriteListSerializer = FavoriteListSerializer(favorite_list)
    return Response(favoriteListSerializer.data, status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_favorite_list(request):
    try:
        user = CustomUser.objects.get(id=request.user.id)
    except (KeyError, CustomUser.DoesNotExist):
        return Response({"error": "Invalid or missing user_id"}, status=status.HTTP_400_BAD_REQUEST)

    title = request.data.get('title')
    if not title:
        return Response({"error": "Missing title"}, status=status.HTTP_400_BAD_REQUEST)

    favorite_list = FavoriteList.objects.create(user=user, title=title)

    post_id = request.data.get('post_id')
    if post_id:
        try:
            post = Post.objects.get(id=post_id)
            favorite_list.favorite_posts.add(post)
        except Post.DoesNotExist:
            return Response({"error": "Invalid post_id"}, status=status.HTTP_400_BAD_REQUEST)

    favorite_user_id = request.data.get('favorite_user_id')
    if favorite_user_id:
        try:
            favorite_user = CustomUser.objects.get(id=favorite_user_id)
            favorite_list.favorite_users.add(favorite_user)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid favorite_user_id"}, status=status.HTTP_400_BAD_REQUEST)

    favorite_community_id = request.data.get('favorite_community_id')
    if favorite_community_id:
        try:
            favorite_community = Community.objects.get(id=favorite_community_id)
            favorite_list.favorite_communities.add(favorite_community)
        except Community.DoesNotExist:
            return Response({"error": "Invalid favorite_community_id"}, status=status.HTTP_400_BAD_REQUEST)
 
    favoriteListSerializer = FavoriteListSerializer(favorite_list)
    return Response(favoriteListSerializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorite_list(request):
    favorite_list_id = request.data.get('favorite_list_id')
    if not favorite_list_id:
        return Response({"error": "Missing favorite_list_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        favorite_list = FavoriteList.objects.get(id=favorite_list_id)
    except FavoriteList.DoesNotExist:
        return Response({"error": "Invalid favorite_list_id"}, status=status.HTTP_400_BAD_REQUEST)

    post_id = request.data.get('post_id')
    if post_id:
        try:
            post = Post.objects.get(id=post_id)
            favorite_list.favorite_posts.add(post)
        except Post.DoesNotExist:
            return Response({"error": "Invalid post_id"}, status=status.HTTP_400_BAD_REQUEST)

    favorite_user_id = request.data.get('favorite_user_id')
    if favorite_user_id:
        try:
            favorite_user = CustomUser.objects.get(id=favorite_user_id)
            favorite_list.favorite_users.add(favorite_user)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid favorite_user_id"}, status=status.HTTP_400_BAD_REQUEST)

    favorite_community_id = request.data.get('favorite_community_id')
    if favorite_community_id:
        try:
            favorite_community = Community.objects.get(id=favorite_community_id)
            favorite_list.favorite_communities.add(favorite_community)
        except Community.DoesNotExist:
            return Response({"error": "Invalid favorite_community_id"}, status=status.HTTP_400_BAD_REQUEST)

    if favorite_list.user != request.user:
        return Response({"error": "You do not have permission to delete this FavoriteList"}, status=status.HTTP_403_FORBIDDEN)

    favoriteListSerializer = FavoriteListSerializer(favorite_list)
    return Response(favoriteListSerializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_favorite_list_title(request):
    favorite_list_id = request.data.get('favorite_list_id')
    if not favorite_list_id:
        return Response({"error": "Missing favorite_list_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        favorite_list = FavoriteList.objects.get(id=favorite_list_id)
    except FavoriteList.DoesNotExist:
        return Response({"error": "Invalid favorite_list_id"}, status=status.HTTP_400_BAD_REQUEST)

    title = request.data.get('title')
    if not title:
        return Response({"error": "Missing title"}, status=status.HTTP_400_BAD_REQUEST)

    if favorite_list.user != request.user:
        return Response({"error": "You do not have permission to delete this FavoriteList"}, status=status.HTTP_403_FORBIDDEN)

    favorite_list.title = title
    favorite_list.save()

    favoriteListSerializer = FavoriteListSerializer(favorite_list)
    return Response(favoriteListSerializer.data, status=status.HTTP_200_OK)
 
 
  
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_favorite_list(request):
    favorite_list_id = request.data.get('favorite_list_id')
    if not favorite_list_id:
        return Response({"error": "Missing favorite_list_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        favorite_list = FavoriteList.objects.get(id=favorite_list_id)
    except FavoriteList.DoesNotExist:
        return Response({"error": "Invalid favorite_list_id"}, status=status.HTTP_400_BAD_REQUEST)

    post_id = request.data.get('post_id')
    if post_id:
        try:
            post = Post.objects.get(id=post_id)
            favorite_list.favorite_posts.remove(post)
        except Post.DoesNotExist:
            return Response({"error": "Invalid post_id"}, status=status.HTTP_400_BAD_REQUEST)

    favorite_user_id = request.data.get('favorite_user_id')
    if favorite_user_id:
        try:
            favorite_user = CustomUser.objects.get(id=favorite_user_id)
            favorite_list.favorite_users.remove(favorite_user)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid favorite_user_id"}, status=status.HTTP_400_BAD_REQUEST)

    favorite_community_id = request.data.get('favorite_community_id')
    if favorite_community_id:
        try:
            favorite_community = Community.objects.get(id=favorite_community_id)
            favorite_list.favorite_communities.remove(favorite_community)
        except Community.DoesNotExist:
            return Response({"error": "Invalid favorite_community_id"}, status=status.HTTP_400_BAD_REQUEST)

    if favorite_list.user != request.user:
        return Response({"error": "You do not have permission to delete this FavoriteList"}, status=status.HTTP_403_FORBIDDEN)

    favoriteListSerializer = FavoriteListSerializer(favorite_list)
    return Response(favoriteListSerializer.data, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_favorite_list(request):
    favorite_list_id = request.data.get('favorite_list_id')
    if not favorite_list_id:
        return Response({"error": "Missing favorite_list_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        favorite_list = FavoriteList.objects.get(id=favorite_list_id)
    except FavoriteList.DoesNotExist:
        return Response({"error": "Invalid favorite_list_id"}, status=status.HTTP_400_BAD_REQUEST)

    if favorite_list.user != request.user:
        return Response({"error": "You do not have permission to delete this FavoriteList"}, status=status.HTTP_403_FORBIDDEN)

    favorite_list.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)