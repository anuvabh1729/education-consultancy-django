
from django.db import models
from django.conf import settings
from students.models import StudentProfile
from consultants.models import ConsultantProfile


class ChatRoom(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.id}: {self.student.full_name} ↔ {self.consultant.full_name}"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}"
