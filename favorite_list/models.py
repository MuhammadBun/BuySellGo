from django.db import models
from account.models import CustomUser
from post.models import Post
from community.models import Community
class FavoriteList(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    favorite_posts = models.ManyToManyField(Post)
    favorite_users = models.ManyToManyField(CustomUser, related_name='favorited_by')
    favorite_communities = models.ManyToManyField(Community)
    def __str__(self):
        return self.title
 