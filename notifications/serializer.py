from rest_framework import serializers
from .models import Notifications

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ('id', 'recipient', 'actor', 'verb', 'target', 'target_object_id', 'read', 'timestamp')