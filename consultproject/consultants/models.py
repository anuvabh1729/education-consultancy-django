from django.db import models
from django.conf import settings


class ConsultantProfile(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    profile_photo = models.ImageField(upload_to="consultants/photos/", null=True, blank=True)

    # Professional Details
    designation = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField()
    expertise_areas = models.JSONField(default=list)  # e.g. ["Visa", "SOP/LOR"]
    country_specialist = models.JSONField(default=list)  # e.g. ["Canada", "UK"]
    languages = models.CharField(max_length=200)
    certifications = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class ConsultantSchedule(models.Model):
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.consultant.full_name} - {self.date} {self.start_time}-{self.end_time}"

