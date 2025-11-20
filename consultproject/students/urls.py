from django.urls import path
from .views import (
    StudentProfileView,
    UploadDocumentView,
    UniversityApplicationView,
    BookConsultantView,
    # student_profile,
    student_dashboard,
    student_basic_info,

)

#updated by hash
from . import views

urlpatterns = [
    
    path("basic-info/", student_basic_info, name="student_basic_info"),
    path("dashboard/", student_dashboard, name="student_dashboard"),
    path("profile/", views.student_profile, name="student_profile"),
    path("edit-profile/", views.edit_student_profile, name="edit_student_profile"),
    path("upload-documents/", views.upload_documents, name="upload_documents"),
    path("universities/", views.explore_universities, name="explore_universities"),
    path("universities/<int:uni_id>/programs/", views.programs_page, name="programs_page"),
    path("consultants/", views.consultant_list, name="consultant_list"),
    path("book-session/<int:consultant_id>/", views.book_session, name="book_session"),
    path("my-sessions/", views.my_sessions, name="my_sessions"),


    
]
