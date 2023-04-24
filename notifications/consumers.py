# chat/consumers.py
import json
from account.models import CustomUser
from community.models import Community
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notifications
from rest_framework_jwt.utils import jwt_decode_handler
from asgiref.sync import sync_to_async
from rest_framework.response import Response
from dotenv import load_dotenv
import os

class NotificationUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = str(self.scope["url_route"]["kwargs"]["room_name"])
        if self.scope['user']==self.room_name:
            self.room_group_name = self.room_name
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()
            raise ValueError(f"Un Authenticated")
   
        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        notification_data = text_data_json['notification']
        recipient = notification_data['recipient']
        actor = notification_data['actor']
        verb = notification_data['verb']
        target = notification_data['target']
        target_object_id = notification_data['target_object_id']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_notifications",
                "notification": {
                    "recipient": recipient,
                    "actor": actor,
                    "verb": verb,
                    "target": target,
                    "target_object_id": target_object_id
                }
            }
        )
        await self.save_notification_to_database(notification_data)

    async def send_notifications(self, event):
        notification_data = event['notification']
        recipient = notification_data['recipient']
        actor = notification_data['actor']
        verb = notification_data['verb']
        target = notification_data['target']
        target_object_id = notification_data['target_object_id']

        await self.send(text_data=json.dumps({
            "notification": {
                "recipient": recipient,
                "actor": actor,
                "verb": verb,
                "target": target,
                "target_object_id": target_object_id
            }
        }))

    @database_sync_to_async
    def save_notification_to_database(self, notification_data):
        recipient = notification_data['recipient']
        actor = notification_data['actor']
        verb = notification_data['verb']
        target = notification_data['target']
        target_object_id = notification_data['target_object_id']

        Notifications.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            target=target,
            target_object_id=target_object_id
        )

 
class NotificationCommunityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["community_name"]

        try:
            community = await sync_to_async(Community.objects.get)(id=self.room_name)
        except Community.DoesNotExist:
            self.close()
            raise ValueError(f"The Community : {self.room_name} does not exist")

        if not await sync_to_async(community.members.filter(id=self.scope['user']).exists)():
            self.close()
            raise ValueError(f"The user : {self.scope['user']} is not a member in the {self.room_name}")
        
        await self.accept()
        self.room_group_name = f"groub_notifications_{self.room_name}"
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        notification_data = text_data_json['notification']
        recipient = notification_data['recipient']
        actor = notification_data['actor']
        verb = notification_data['verb']
        target = notification_data['target']
        target_object_id = notification_data['target_object_id']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_notifications",
                "notification": {
                    "recipient": recipient,
                    "actor": actor,
                    "verb": verb,
                    "target": target,
                    "target_object_id": target_object_id
                }
            }
        )
        await self.save_notification_to_database(notification_data)

    async def send_notifications(self, event):
        notification_data = event['notification']
        recipient = notification_data['recipient']
        actor = notification_data['actor']
        verb = notification_data['verb']
        target = notification_data['target']
        target_object_id = notification_data['target_object_id']

        await self.send(text_data=json.dumps({
            "notification": {
                "recipient": recipient,
                "actor": actor,
                "verb": verb,
                "target": target,
                "target_object_id": target_object_id
            }
        }))

    @database_sync_to_async
    def save_notification_to_database(self, notification_data):
        recipient = notification_data['recipient']
        actor = notification_data['actor']
        verb = notification_data['verb']
        target = notification_data['target']
        target_object_id = notification_data['target_object_id']

        Notifications.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            target=target,
            target_object_id=target_object_id
        )

class NotificationAdminConsumer(AsyncWebsocketConsumer):
    load_dotenv()  # load environment variables from .env file
# SECURITY WARNING: keep the secret key used in production secret!
 
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["admin_notifiy"]
        ADMIN_CHANNEL = os.environ.get('ADMIN_CHANNEL')

        if ADMIN_CHANNEL == self.room_name :
            await self.accept()
            self.room_group_name = "admin_notifications_%s" % self.room_name
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        else:
            await self.close()
            raise ValueError(f"Un Authenticated")

        


   

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        notification_data = text_data_json['notification']
        recipient = notification_data['recipient']
        actor = notification_data['actor']
        verb = notification_data['verb']
        target = notification_data['target']
        target_object_id = notification_data['target_object_id']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_notifications",
                "notification": {
                    "recipient": recipient,
                    "actor": actor,
                    "verb": verb,
                    "target": target,
                    "target_object_id": target_object_id
                }
            }
        )
        await self.save_notification_to_database(notification_data)

    async def send_notifications(self, event):
        notification_data = event['notification']
        recipient = notification_data['recipient']
        actor = notification_data['actor']
        verb = notification_data['verb']
        target = notification_data['target']
        target_object_id = notification_data['target_object_id']

        await self.send(text_data=json.dumps({
            "notification": {
                "recipient": recipient,
                "actor": actor,
                "verb": verb,
                "target": target,
                "target_object_id": target_object_id
            }
        }))

    @database_sync_to_async
    def save_notification_to_database(self, notification_data):
        recipient = notification_data['recipient']
        actor = notification_data['actor']
        verb = notification_data['verb']
        target = notification_data['target']
        target_object_id = notification_data['target_object_id']

        Notifications.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            target=target,
            target_object_id=target_object_id
        )