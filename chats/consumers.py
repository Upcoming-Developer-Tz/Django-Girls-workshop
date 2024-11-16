import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Parse the incoming JSON data
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send the message back to the WebSocket
        await self.send(text_data=json.dumps({"message": message}))
