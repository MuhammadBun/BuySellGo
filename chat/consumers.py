# # chat/consumers.py
# import json

# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import Chat
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#             current_user_id = self.scope['user'].id if self.scope['user'].id else int(self.scope['query_string'])
#             other_user_id = self.scope['url_route']['kwargs']['id']
#             self.room_name = (
#                 f'{current_user_id}_{other_user_id}'
#                 if int(current_user_id) > int(other_user_id)
#                 else f'{other_user_id}_{current_user_id}'
#             )
#             self.room_group_name = f'chat_{self.room_name}'
#             await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#             await self.accept()
#             # await self.send(text_data=self.room_group_name)

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         # Call the printMessage method
#          # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )
 
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event["message"]
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"message": message}))
#         await database_sync_to_async(Chat.objects.create)(
#             room_name=self.scope["url_route"]["kwargs"]["room_name"],
#             message=message
#         )
