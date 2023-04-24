from rest_framework import serializers
from .models import Chat

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat 
        fields = ('id', 'message', 'sender','receiver', 'timestamp')
