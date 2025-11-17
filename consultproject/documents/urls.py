# documents/urls.py
from django.urls import path
from .views import (
    UploadDocumentView,
    StudentDocumentListView,
    AllDocumentsListView,
    VerifyDocumentView,
)

urlpatterns = [
    path("upload/", UploadDocumentView.as_view()),
    path("mine/", StudentDocumentListView.as_view()),
    path("pending/", AllDocumentsListView.as_view()),
    path("verify/<int:doc_id>/", VerifyDocumentView.as_view()),
]
