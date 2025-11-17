
from django.urls import path
from .views import CreateChatRoomView, ListMessagesView, AIChatView

urlpatterns = [
    path("room/create/", CreateChatRoomView.as_view()),
    path("messages/<int:room_id>/", ListMessagesView.as_view()),
    path("ai/", AIChatView.as_view()),
]
