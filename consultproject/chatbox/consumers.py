
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .models import ChatRoom, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group = f"chat_{self.room_id}"

        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    @database_sync_to_async
    def save_message(self, room_id, user_id, text):
        room = ChatRoom.objects.get(id=room_id)
        user = User.objects.get(id=user_id)
        msg = Message.objects.create(room=room, sender=user, text=text)
        return msg

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data["message"]
        user_id = data["sender_id"]

        msg = await self.save_message(self.room_id, user_id, text)

        await self.channel_layer.group_send(
            self.room_group,
            {
                "type": "chat_message",
                "message": msg.text,
                "sender": msg.sender.username,
                "timestamp": str(msg.timestamp),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
