
from rest_framework import serializers
from .models import ChatRoom, Message


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = ("id", "room", "sender", "sender_name", "text", "timestamp")
