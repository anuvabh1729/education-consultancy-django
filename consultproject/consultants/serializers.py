from rest_framework import serializers
from .models import ConsultantProfile, ConsultantSchedule


class ConsultantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantProfile
        fields = "__all__"
        read_only_fields = ("user", "email")


class ConsultantScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantSchedule
        fields = "__all__"
        read_only_fields = ("consultant", "is_available")
