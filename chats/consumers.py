# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.utils import timezone

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["url_route"]["kwargs"]["username"]
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

#         await self.channel_layer.group_add(
#             self.room_name, self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_name, self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         now = timezone.now()

#         await self.channel_layer.group_send(
#             self.room_name,
#             {
#                 "type": "chat_message",
#                 "message": message,
#                 "user": self.user,
#                 "datetime": now.isoformat(),
#             },
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps(event))



import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        username = self.scope['query_string'].decode().split('=')[1]
        now = timezone.now()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'datetime': now.isoformat(),  # Add ISO formatted timestamp
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket client with datetime
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'datetime': event['datetime'],  # Include datetime in response
        }))
