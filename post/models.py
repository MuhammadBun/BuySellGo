from django.db import models
from account.models import CustomUser
 
class Post(models.Model):
    description = models.CharField(max_length=128,default='',null=False)
    contact_info = models.CharField(max_length=20, null=True)
    user_info = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    post_type = models.BooleanField(default=True) # 1=> buyer , 0=>seller
    date_posted = models.DateTimeField(auto_now_add=True) # the date and time when the post was created
    state = models.BooleanField(default=True) # a boolean field indicating the state of the post
    likes = models.IntegerField(default=0) # the number of likes for the post
class Photos(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos') # a foreign key to the Post model indicating the post the photo belongs to
    image = models.ImageField(upload_to='post_photos/') # a field for the photo, which is an image file
    