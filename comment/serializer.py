from rest_framework import serializers
from .models import Comment 
 

class CommentsSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'post', 'content', 'created_at', 'updated_at', 'photo', 'user', 'is_edited', 'is_deleted', 'parent', 'replies')

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent=obj, is_deleted=False)
        serializer = CommentsSerializer(replies, many=True, context=self.context)
        return serializer.data