from django.urls import path
from .views import (
    StudentProfileView,
    UploadDocumentView,
    UniversityApplicationView,
    BookConsultantView,
)

urlpatterns = [
    path("profile/", StudentProfileView.as_view()),
    path("documents/upload/", UploadDocumentView.as_view()),
    path("applications/", UniversityApplicationView.as_view()),
    path("bookings/book/", BookConsultantView.as_view()),
]
