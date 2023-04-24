# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# from notifications.models import Notifications
# from chat.models import Chat
# def send_notification_to_user(user_id, message,  type_message,created_at):
#     # Get the channel layer
#     channel_layer = get_channel_layer()

#     # Send the message to the user's personal channel
#     async_to_sync(channel_layer.group_send)(
#         user_id,
#         {
#                     "message": message,
#                     "type_message": type_message,
#                     "created_at": created_at,
#         }
#     )

# @receiver(post_save, sender=Chat)
# def on_message_save(sender, instance, created, **kwargs):
#     if created:
#         # Send a notification to the user's personal channel
#         user_id = str(instance.receiver.id)
#         message = f'You have a new message from {instance.sender.username}'
#         type_message='user-{user_id}-message'
#         created_at=instance.created_at
#         created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
#         send_notification_to_user(user_id, message,type_message,created_at)
#         Notifications.objects.create(
#                 message=message,
#                 user=instance.user,
#                 notification_type='reply'
#             ) 