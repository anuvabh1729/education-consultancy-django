from rest_framework import serializers
from .models import (
    StudentProfile,
    StudentDocument,
    UniversityApplication,
    ConsultantBooking,
)
from consultants.models import ConsultantProfile, ConsultantSchedule


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = "__all__"
        read_only_fields = ("user",)


class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocument
        fields = "__all__"
        read_only_fields = ("student", "status")


class UniversityApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityApplication
        fields = "__all__"
        read_only_fields = ("student", "status")


class ConsultantBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantBooking
        fields = "__all__"
        read_only_fields = ("student", "status")
