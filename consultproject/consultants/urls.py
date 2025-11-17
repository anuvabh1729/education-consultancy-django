from django.urls import path
<<<<<<< HEAD
from . import views

app_name = 'consultants'

urlpatterns = [
    path('', views.consultant_list, name='consultant_list'),
    path('<int:pk>/', views.consultant_detail, name='consultant_detail'),
    path('success/', views.booking_success, name='booking_success'),
    path('booking/<int:pk>/delete/', views.delete_booking, name='booking_delete'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
=======
from .views import (
    ConsultantProfileView,
    AddScheduleView,
    ConsultantScheduleListView,
)

urlpatterns = [
    path("profile/", ConsultantProfileView.as_view()),
    path("schedule/add/", AddScheduleView.as_view()),
    path("schedule/<int:consultant_id>/", ConsultantScheduleListView.as_view()),
>>>>>>> 9b05168f821fc26b82794dfcdc5c5ca30c3d8f75
]
