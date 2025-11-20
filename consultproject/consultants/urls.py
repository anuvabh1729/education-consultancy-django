from django.urls import path
from . import views
# DRF API views (imported from views)
from .views import (
    ConsultantProfileView,
    AddScheduleView,
    ConsultantScheduleListView,
)
from . import views

app_name = 'consultants'

urlpatterns = [

    # Web pages
    path('', views.consultant_list, name='consultant_list'),
    path('<int:pk>/', views.consultant_detail, name='consultant_detail'),

    # API endpoints (prefix these if you want an 'api/' namespace)
    path('api/profile/', ConsultantProfileView.as_view(), name='api_profile'),
    path('api/schedule/add/', AddScheduleView.as_view(), name='api_schedule_add'),
    path('api/schedule/<int:consultant_id>/', ConsultantScheduleListView.as_view(), name='api_schedule_list'),

    path("home/", views.ConsultantProfile, name="consultant_home"),

    path("profile/", ConsultantProfileView.as_view()),
    path("schedule/add/", AddScheduleView.as_view()),
    path("schedule/<int:consultant_id>/", ConsultantScheduleListView.as_view()),

]
