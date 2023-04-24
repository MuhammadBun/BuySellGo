from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notifications
from django.contrib.contenttypes.models import ContentType
from .serializer import NotificationSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from post.models import Post
from post.serializer import PostSerializer
from account.models import CustomUser
from account.serializer import CustomUserSerializer

from community.models import Community
from community.serializer import CommunitySerializer
from comment.models import Comment
from comment.serializer import CommentsSerializer
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_notification(request):
    try:
        # Get the data from the request
        recipient = request.data.get('recipient')
        actor = request.data.get('actor')
        verb = request.data.get('verb')
        target_model = request.data.get('target')
        target_object_id = request.data.get('target_object_id')
        read_status = request.data.get('read')

        # Check that all required fields are present in the request data
        if not all([recipient, actor, verb, target_model, target_object_id]):
            return Response({'error': 'Missing required field(s)'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new notification instance
        notification = Notifications.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            target=target_model,
            target_object_id=target_object_id,
            read=read_status
        )

        # Serialize the data
        serializer = NotificationSerializer(notification)

        # Return a success response with the serialized data
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist:
        # Return a not found error response if the requested ContentType instance does not exist
        return Response({'error': 'The requested ContentType instance does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        # Return a validation error response if the provided data is invalid
        return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
    except NotFound as e:
        # Return a not found error response if the requested resource is not found
        return Response({'error': e.detail}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Return a generic error response if something else goes wrong
 
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
def get_notification_target(request):
    target = request.data.get('target')
    target_object_id = request.data.get('target_object_id')

    if target and target_object_id:
        # Check if the target is valid
        if target not in ['comment', 'community', 'post', 'CustomUser']:
            return Response({'error': 'Invalid target'}, status=400)

        # Check if the target_object_id is valid and get the object
        try:
            if target == 'comment':
                obj = Comment.objects.get(pk=target_object_id)
                serializer = CommentsSerializer(obj)
            elif target == 'community':
                obj = Community.objects.get(pk=target_object_id)
                serializer = CommunitySerializer(obj)
            elif target == 'post':
                obj = Post.objects.get(pk=target_object_id)
                serializer = PostSerializer(obj)
            elif target == 'CustomUser':
                obj = CustomUser.objects.get(pk=target_object_id)
                serializer = CustomUserSerializer(obj)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid target_object_id'}, status=400)

        # If everything is valid, return a success response with the serialized object
        return Response({'success': True, 'object': serializer.data})
    else:
        return Response({'error': 'Missing target or target_object_id'}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notifications(request):
    try:
        # Get the user from the request
        user = request.user.id

        # Get all notification instances for the user from the database
        notifications = Notifications.objects.filter(recipient=user)

        # Apply filters if provided in the request
        if 'unread' in request.GET:
            notifications = notifications.filter(read=False)
        elif 'read' in request.GET:
            notifications = notifications.filter(read=True)
        
        if 'start_date' in request.GET and 'end_date' in request.GET:
            start_date = request.GET['start_date']
            end_date = request.GET['end_date']
            notifications = notifications.filter(timestamp__range=[start_date, end_date])

        # Serialize the data
        serializer = NotificationSerializer(notifications, many=True)

        # Return a success response with the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValidationError as e:
        # Return a validation error response if the provided data is invalid
        return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
    except NotFound as e:
        # Return a not found error response if the requested resource is not found
        return Response({'error': e.detail}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
 
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return a generic error response if something else goes wrong

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request):
    try:
        # Get the notification id from the request
        notification_id = request.data.get('notification_id')

        # Get the notification instance from the database
        notification = Notifications.objects.get(id=notification_id)

        # Mark the notification as read
        notification.read = True
        notification.save()

        # Serialize the data
        serializer = NotificationSerializer(notification)

        # Return a success response with the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Notifications.DoesNotExist:
        # Return a not found error response if the specified Notifications instance does not exist
        return Response({'error': 'The specified Notifications instance does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        # Return a validation error response if the provided data is invalid
        return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
    except NotFound as e:
        # Return a not found error response if the requested resource is not found
        return Response({'error': e.detail}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Return a generic error response if something else goes wrong
 
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request):
    try:
        # Get the notification id from the request
        notification_id = request.data.get('notification_id')

        # Get the notification instance from the database and delete it
        Notifications.objects.get(id=notification_id).delete()

        # Return a success response with no content
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Notifications.DoesNotExist:
        # Return a not found error response if the specified Notifications instance does not exist
        return Response({'error': 'The specified Notifications instance does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        # Return a validation error response if the provided data is invalid
        return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
    except NotFound as e:
        # Return a not found error response if the requested resource is not found
        return Response({'error': e.detail}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
         # Return a generic error response if something else goes wrong
         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)