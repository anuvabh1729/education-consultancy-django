from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.permissions import IsStudent
from .models import (
    StudentProfile,
    StudentDocument,
    UniversityApplication,
    ConsultantBooking,
)
from consultants.models import ConsultantProfile, ConsultantSchedule
from .serializers import (
    StudentProfileSerializer,
    StudentDocumentSerializer,
    UniversityApplicationSerializer,
    ConsultantBookingSerializer,
)


class StudentProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        return Response(StudentProfileSerializer(profile).data)

    def post(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Profile updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadDocumentView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        student = StudentProfile.objects.get(user=request.user)
        serializer = StudentDocumentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(student=student)
            return Response({"message": "Document uploaded", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UniversityApplicationView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        student = StudentProfile.objects.get(user=request.user)
        serializer = UniversityApplicationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(student=student)
            return Response({"message": "Application submitted", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        student = StudentProfile.objects.get(user=request.user)
        apps = UniversityApplication.objects.filter(student=student)
        return Response(UniversityApplicationSerializer(apps, many=True).data)


class BookConsultantView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        student = StudentProfile.objects.get(user=request.user)
        consultant_id = request.data.get("consultant_id")
        schedule_id = request.data.get("schedule_id")

        consultant = ConsultantProfile.objects.get(id=consultant_id)
        schedule = ConsultantSchedule.objects.get(id=schedule_id)

        if not schedule.is_available:
            return Response({"error": "Schedule not available"}, status=400)

        booking = ConsultantBooking.objects.create(
            student=student,
            consultant=consultant,
            schedule=schedule
        )
        schedule.is_available = False
        schedule.save()

        return Response({
            "message": "Consultant booked successfully",
            "booking": ConsultantBookingSerializer(booking).data,
        })
