from django.db import models
from django.conf import settings
from datetime import timedelta


# ---------------------------------------------------------
#  CONSULTANT PROFILE
# ---------------------------------------------------------

class ConsultantProfile(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    SPECIALIZATION_CHOICES = (
        ("usa", "USA"),
        ("uk", "UK"),
        ("canada", "Canada"),
        ("australia", "Australia"),
        ("europe", "Europe"),
        ("other", "Other"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='consultant_profiles'
    )
    full_name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    experience_years = models.IntegerField(default=0)
    profile_image = models.ImageField(upload_to="consultant_profiles/", blank=True, null=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


# ---------------------------------------------------------
#  CONSULTANT WEEKLY SCHEDULE
# ---------------------------------------------------------

class ConsultantSchedule(models.Model):
    DAY_CHOICES = (
        ("monday", "Monday"),
        ("tuesday", "Tuesday"),
        ("wednesday", "Wednesday"),
        ("thursday", "Thursday"),
        ("friday", "Friday"),
        ("saturday", "Saturday"),
        ("sunday", "Sunday"),
    )

    consultant = models.ForeignKey(
        ConsultantProfile,
        on_delete=models.CASCADE,
        related_name="schedules",
    )

    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ("consultant", "day", "start_time")

    def __str__(self):
        return f"{self.consultant.full_name} - {self.day} {self.start_time} to {self.end_time}"


# ---------------------------------------------------------
#  CONSULTATION BOOKING
# ---------------------------------------------------------

class Booking(models.Model):
    CONSULTATION_TYPE_CHOICES = [
        ("online", "Online"),
        ("inperson", "In Person"),
    ]

    consultant = models.ForeignKey(
        ConsultantProfile,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    client_name = models.CharField(max_length=150)
    client_email = models.EmailField()
    consultation_type = models.CharField(
        max_length=20, choices=CONSULTATION_TYPE_CHOICES, default="online"
    )

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)

    duration_minutes = models.PositiveIntegerField(default=60)
    notes = models.TextField(blank=True)

    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_datetime"]

    def __str__(self):
        return f"{self.consultant.full_name} — {self.client_name} @ {self.start_datetime}"

    def save(self, *args, **kwargs):
        # Auto-calculate end time
        if self.start_datetime and self.duration_minutes:
            self.end_datetime = self.start_datetime + timedelta(minutes=self.duration_minutes)

        super().save(*args, **kwargs)
