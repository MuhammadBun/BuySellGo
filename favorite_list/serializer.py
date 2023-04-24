from rest_framework import serializers
from .models import FavoriteList
 
 
class FavoriteListSerializer(serializers.ModelSerializer):
 

    class Meta:
        model = FavoriteList
        fields = ['id', 'user_id', 'title']
