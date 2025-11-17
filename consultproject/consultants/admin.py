from django.contrib import admin
from .models import ConsultantProfile, ConsultantSchedule, Booking

@admin.register(ConsultantProfile)
class ConsultantProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'specialization', 'verified', 'created_at')
    search_fields = ('full_name', 'user__username', 'user__email')
    list_filter = ('specialization', 'verified')

@admin.register(ConsultantSchedule)
class ConsultantScheduleAdmin(admin.ModelAdmin):
    list_display = ('consultant', 'day', 'start_time', 'end_time', 'is_available')
    list_filter = ('day', 'is_available')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('consultant', 'client_name', 'start_datetime', 'end_datetime', 'duration_minutes', 'confirmed')
    list_filter = ('consultant', 'confirmed')
    search_fields = ('client_name', 'client_email', 'consultant__full_name')
