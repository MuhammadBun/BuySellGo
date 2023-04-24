from django.db import models
from post.models import Post
from account.models import CustomUser
class Community(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    members = models.ManyToManyField(CustomUser, related_name='communities')
    posts = models.ManyToManyField(Post, related_name='communities')
    admin = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='admin_communities')
    
def __str__(self):
    return f"Name: {self.name}, Description: {self.description}, Members: {self.members.count()}, Posts: {self.posts.count()}, Admin: {self.admin}"





