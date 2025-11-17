from django.urls import path
from . import views
# DRF API views (imported from views)
from .views import (
    ConsultantProfileView,
    AddScheduleView,
    ConsultantScheduleListView,
)

app_name = 'consultants'

urlpatterns = [
    # Web pages
    path('', views.consultant_list, name='consultant_list'),
    path('<int:pk>/', views.consultant_detail, name='consultant_detail'),
    path('success/', views.booking_success, name='booking_success'),
    path('booking/<int:pk>/delete/', views.delete_booking, name='booking_delete'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),

    # API endpoints (prefix these if you want an 'api/' namespace)
    path('api/profile/', ConsultantProfileView.as_view(), name='api_profile'),
    path('api/schedule/add/', AddScheduleView.as_view(), name='api_schedule_add'),
    path('api/schedule/<int:consultant_id>/', ConsultantScheduleListView.as_view(), name='api_schedule_list'),
]
