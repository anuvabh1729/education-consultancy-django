from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone

from .models import ConsultantProfile, ConsultantSchedule




def consultant_list(request):
    consultants = ConsultantProfile.objects.filter(verified=True)
    return render(request, 'consultants/consultant_list.html', {'consultants': consultants})


def consultant_detail(request, pk):
    consultant = get_object_or_404(ConsultantProfile, pk=pk)
    return render(request, "consultants/consultant_detail.html", {
        "consultant": consultant
    })

try:
    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework import status, permissions
    from accounts.permissions import IsConsultant
    from .serializers import ConsultantProfileSerializer, ConsultantScheduleSerializer
except Exception:
    # If DRF or serializers/permissions are missing, we still want the main site to work.
    APIView = object  # placeholder so name exists; API endpoints will fail if used.
    Response = None
    status = None
    permissions = None
    IsConsultant = None
    ConsultantProfileSerializer = None
    ConsultantScheduleSerializer = None


class ConsultantProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsConsultant]

    def get(self, request):
        profile, _ = ConsultantProfile.objects.get_or_create(
            user=request.user,
            defaults={"email": getattr(request.user, 'email', "")}
        )
        return Response(ConsultantProfileSerializer(profile).data)

    def post(self, request):
        profile, _ = ConsultantProfile.objects.get_or_create(
            user=request.user,
            defaults={"email": getattr(request.user, 'email', "")}
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
