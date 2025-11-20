from django.urls import path
from .views import (
    RegisterStudentView,
    RegisterConsultantView,
    LoginView,
    GoogleLoginView,
    UserProfileView,
    login_view,
    signup_view,
    welcome_view,
    services_view,
    about_view,
    contact_view,
    feedback_view,
    logout_view,


)

urlpatterns = [
    # path("register/student/", RegisterStudentView.as_view()),
    # path("register/consultant/", RegisterConsultantView.as_view()),
    # path('', login_view, name='home'),
    path('', welcome_view, name='home'),

    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("welcome/", welcome_view, name="welcome"),
    path('services/', services_view, name='services'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('feedback/', feedback_view, name='feedback'),
    path("logout/", logout_view, name="logout"),


    # path("login/google/", GoogleLoginView.as_view()),
    # path("me/", UserProfileView.as_view()),
]
