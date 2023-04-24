from django.db import models
from post.models import Post
from account.models import CustomUser
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='comment_photos/', null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
