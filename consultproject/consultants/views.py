from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.permissions import IsConsultant
from .models import ConsultantProfile, ConsultantSchedule
from .serializers import ConsultantProfileSerializer, ConsultantScheduleSerializer


class ConsultantProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsConsultant]

    def get(self, request):
        profile, _ = ConsultantProfile.objects.get_or_create(
            user=request.user,
            defaults={"email": request.user.email or ""}
        )
        return Response(ConsultantProfileSerializer(profile).data)

    def post(self, request):
        profile, _ = ConsultantProfile.objects.get_or_create(
            user=request.user,
            defaults={"email": request.user.email or ""}
        )
        serializer = ConsultantProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Consultant profile updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddScheduleView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsConsultant]

    def post(self, request):
        profile = ConsultantProfile.objects.get(user=request.user)
        serializer = ConsultantScheduleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(consultant=profile)
            return Response({"message": "Schedule added", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsultantScheduleListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, consultant_id):
        schedules = ConsultantSchedule.objects.filter(
            consultant_id=consultant_id,
            is_available=True
        )
        return Response(ConsultantScheduleSerializer(schedules, many=True).data)
