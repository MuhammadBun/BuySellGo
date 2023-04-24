# Create your models here.
from django.db import models
from account.models import CustomUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notifications(models.Model):
    recipient =  models.PositiveIntegerField()
    actor = models.PositiveIntegerField()
    verb = models.CharField(max_length=255,null=True)
    target = models.CharField(max_length=255,null=False)
    target_object_id = models.PositiveIntegerField()
 
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):  
        return f'{self.actor} {self.verb} {self.target}'
