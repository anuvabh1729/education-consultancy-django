from django.contrib import admin
from .models import (
    StudentProfile,
    StudentDocument,
    UniversityApplication,
)

admin.site.register(StudentProfile)
admin.site.register(StudentDocument)
admin.site.register(UniversityApplication)
