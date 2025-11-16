from django.urls import path
from .views import (
    RegisterStudentView,
    RegisterConsultantView,
    LoginView,
    GoogleLoginView,
    UserProfileView,
)

urlpatterns = [
    path("register/student/", RegisterStudentView.as_view()),
    path("register/consultant/", RegisterConsultantView.as_view()),
    path("login/", LoginView.as_view()),
    path("login/google/", GoogleLoginView.as_view()),
    path("me/", UserProfileView.as_view()),
]
