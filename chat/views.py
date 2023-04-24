from .serializer import ChatMessageSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from chat.models import Chat
from account.models import CustomUser
from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chats(request):
    user = request.user
    chats = Chat.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')
    serializer = ChatMessageSerializer(chats, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request):
    chat_id = request.data.get('chat_id')
    try:
        chat = Chat.objects.get(id=chat_id, receiver=request.user)
        chat.is_read = True
        chat.save()
        return Response({'success': 'Message marked as read.'})
    except Chat.DoesNotExist:
        return Response({'error': 'Invalid chat or user.'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_chat(request):
    receiver_id = request.data.get('receiver_id')
    content = request.data.get('content')
    if not receiver_id or not content:
        return Response({'error': 'Missing data.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        sender_user = request.user     
        receiver_user = CustomUser.objects.get(id=receiver_id)
        chat = Chat.objects.create(sender=sender_user, receiver=receiver_user, message=content)
        serializer = ChatMessageSerializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid receiver.'}, status=status.HTTP_400_BAD_REQUEST)
 