from django.urls import path
from . import views

app_name = 'consultants'

urlpatterns = [
    path('', views.consultant_list, name='consultant_list'),
    path('<int:pk>/', views.consultant_detail, name='consultant_detail'),
    path('success/', views.booking_success, name='booking_success'),
    path('booking/<int:pk>/delete/', views.delete_booking, name='booking_delete'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
