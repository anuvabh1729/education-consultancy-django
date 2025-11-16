from django.contrib import admin
from .models import (
    StudentProfile,
    StudentDocument,
    UniversityApplication,
    ConsultantBooking,
)

admin.site.register(StudentProfile)
admin.site.register(StudentDocument)
admin.site.register(UniversityApplication)
admin.site.register(ConsultantBooking)
