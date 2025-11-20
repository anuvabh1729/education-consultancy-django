from django.contrib import admin
from .models import ConsultantProfile, ConsultantSchedule


@admin.register(ConsultantProfile)
class ConsultantProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "specialization", "experience_years")


@admin.register(ConsultantSchedule)
class ConsultantScheduleAdmin(admin.ModelAdmin):
    list_display = ("consultant", "date", "time", "is_booked")
