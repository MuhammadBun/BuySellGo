
from .models import Community
from rest_framework import serializers

class CommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = '__all__'
 
 
