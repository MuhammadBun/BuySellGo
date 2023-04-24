from rest_framework import serializers
from .models import Post 
from .models import Photos

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user_info','photos',)
 
