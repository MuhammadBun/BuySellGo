 
from .serializer import CommentsSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes 
 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Comment 
from post.models import Post
from account.models import CustomUser
# get your views here.
@api_view(['GET'])
def get_comments(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post, is_deleted=False, parent=None)
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Post.DoesNotExist:
        return Response({'error': 'Invalid post.'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_comment(request):
    try:
        user = request.user
        post_id = request.data.get('post_id')
        post = Post.objects.get(id=post_id)
        content = request.data.get('content')
        photo = request.FILES.get('photo')
        parent_id = request.data.get('parent_id')
        parent = None

        if parent_id:
            parent = Comment.objects.get(id=parent_id)

        if not content:
            return Response({'error': 'Comment content cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(user=user, post=post, content=content, photo=photo, parent=parent)

        serializer = CommentsSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Post.DoesNotExist:
        return Response({'error': 'Invalid post.'}, status=status.HTTP_400_BAD_REQUEST)

    except Comment.DoesNotExist:
        return Response({'error': 'Invalid parent comment.'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    try:
        user = request.user
        comment = Comment.objects.get(id=comment_id)

        if comment.user != user:
            return Response({'error': 'You are not authorized to update this comment.'}, status=status.HTTP_403_FORBIDDEN)

        content = request.data.get('content')
        photo = request.FILES.get('photo')

        if content:
            comment.content = content
            comment.is_edited = True

        if photo:
            comment.photo = photo
            comment.is_edited = True

        comment.save()

        serializer = CommentsSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Comment.DoesNotExist:
        return Response({'error': 'Invalid comment.'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    try:
        user = request.user
        comment = Comment.objects.get(id=comment_id)

        if comment.user != user:
            return Response({'error': 'You are not authorized to delete this comment.'}, status=status.HTTP_403_FORBIDDEN)

        comment.is_deleted = True
        comment.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    except Comment.DoesNotExist:
        return Response({'error': 'Invalid comment.'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_user_comments(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        comments = Comment.objects.filter(user=user, is_deleted=False)
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid user.'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)