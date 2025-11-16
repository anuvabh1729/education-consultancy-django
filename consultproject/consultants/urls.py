from django.urls import path
from .views import (
    ConsultantProfileView,
    AddScheduleView,
    ConsultantScheduleListView,
)

urlpatterns = [
    path("profile/", ConsultantProfileView.as_view()),
    path("schedule/add/", AddScheduleView.as_view()),
    path("schedule/<int:consultant_id>/", ConsultantScheduleListView.as_view()),
]
