from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone

from .models import ConsultantProfile, Booking, ConsultantSchedule
from .forms import BookingForm



def consultant_list(request):
    consultants = ConsultantProfile.objects.filter(verified=True)
    return render(request, 'consultants/consultant_list.html', {'consultants': consultants})


def consultant_detail(request, pk):
    consultant = get_object_or_404(ConsultantProfile, pk=pk, verified=True)

    if request.method == 'POST':
        form = BookingForm(request.POST, consultant=consultant)
        if form.is_valid():
            booking = form.save(commit=False)
            # optional: attach request.user if authenticated (site is public, so it's optional)
            if request.user.is_authenticated:
                booking.user = request.user

            # Make start_datetime timezone-aware if it's naive
            if booking.start_datetime and timezone.is_naive(booking.start_datetime):
                local_tz = timezone.get_default_timezone()
                booking.start_datetime = timezone.make_aware(booking.start_datetime, local_tz)

            now = timezone.now()
            if booking.start_datetime < now:
                form.add_error('start_datetime', 'Start time must be in the future.')
            else:
                start = booking.start_datetime
                end = start + timedelta(minutes=booking.duration_minutes)

                conflict = Booking.objects.filter(
                    consultant=booking.consultant,
                    start_datetime__lt=end,
                    end_datetime__gt=start
                ).exists()
                if conflict:
                    form.add_error('start_datetime', 'This time overlaps an existing booking.')
                else:
                    weekday = start.astimezone(timezone.get_default_timezone()).strftime('%A').lower()
                    schedules = ConsultantSchedule.objects.filter(
                        consultant=consultant,
                        day=weekday,
                        is_available=True
                    )
                    start_time = start.astimezone(timezone.get_default_timezone()).time()
                    end_time = end.astimezone(timezone.get_default_timezone()).time()

                    valid_in_schedule = False
                    for s in schedules:
                        if s.start_time <= start_time and s.end_time >= end_time:
                            valid_in_schedule = True
                            break
                    if not schedules.exists():
                        valid_in_schedule = True

                    if not valid_in_schedule:
                        form.add_error('start_datetime', 'Requested time is outside consultant availability.')
                    else:
                        booking.save()
                        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                            return JsonResponse({
                                'success': True,
                                'message': 'Booking requested. Consultant will confirm.',
                                'redirect': None
                            })
                        messages.success(request, 'Booking requested. Consultant will confirm soon.')
                        return redirect('consultants:booking_success')
        # AJAX + invalid form -> return rendered HTML fragment
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render(request, 'consultants/consultant_detail.html', {'consultant': consultant, 'form': form}).content.decode('utf-8')
            return JsonResponse({'success': False, 'html': html})
    else:
        form = BookingForm(consultant=consultant)

    return render(request, 'consultants/consultant_detail.html', {'consultant': consultant, 'form': form})


def booking_success(request):
    return render(request, 'consultants/booking_success.html')


def delete_booking(request, pk):
    """
    Public delete: anyone may delete a booking (POST only).
    If you prefer to restrict deletion, implement checks here.
    """
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == "POST":
        booking.delete()
        messages.success(request, "The booking has been cancelled.")
        return redirect("consultants:my_bookings")

    return render(request, "consultants/booking_confirm_delete.html", {"booking": booking})


def my_bookings(request):
    """
    Public bookings listing: shows all bookings (no login required).
    """
    bookings = Booking.objects.all().order_by('-start_datetime')
    return render(request, 'consultants/my_bookings.html', {'bookings': bookings})



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
