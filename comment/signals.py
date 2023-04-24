# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# from .models import Comment
# from notifications.models import Notifications
 
# @receiver(post_save, sender=Comment)
# def on_comment_save(sender, instance, created, **kwargs):
#     print('this is in Comment receiver ---------- ')
#     if created:
#         # Send a notification to the user's personal channel
#         user_id = str(instance.user.id)
#         message = f'Your comment have been created : {instance.post.description}'
#         type_message='user-{user_id}-comment'

#         created_at=instance.created_at
#         created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
