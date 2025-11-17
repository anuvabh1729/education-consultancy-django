
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.permissions import IsStudent, IsConsultant
from students.models import StudentProfile
from consultants.models import ConsultantProfile
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
import openai


class CreateChatRoomView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        student = StudentProfile.objects.get(user=request.user)
        consultant = ConsultantProfile.objects.get(id=request.data.get("consultant_id"))

        room, created = ChatRoom.objects.get_or_create(
            student=student, consultant=consultant
        )

        return Response(ChatRoomSerializer(room).data)


class ListMessagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, room_id):
        messages = Message.objects.filter(room_id=room_id).order_by("timestamp")
        return Response(MessageSerializer(messages, many=True).data)


class AIChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        question = request.data.get("message")

        openai.api_key = getattr(settings, "OPENAI_API_KEY", None)

        if not openai.api_key:
            return Response({"error": "OpenAI key missing"}, status=500)

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}],
        )

        answer = response.choices[0].message["content"]
        return Response({"reply": answer})
