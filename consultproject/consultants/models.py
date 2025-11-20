from django.db import models
from django.conf import settings


class ConsultantProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    specialization = models.CharField(max_length=255, blank=True, null=True)

    rating = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)

    profile_picture = models.ImageField(
        upload_to='consultants/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name
    
class ConsultantSchedule(models.Model):
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.consultant.full_name} – {self.date} {self.time}"

