from django.db import models
from django.conf import settings
from consultants.models import ConsultantProfile, ConsultantSchedule


class StudentProfile(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    parents_name = models.CharField(max_length=200)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    academic_10_score = models.FloatField()
    academic_12_score = models.FloatField()

    def __str__(self):
        return self.full_name


class StudentDocument(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
    )

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to="student_documents/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} - {self.student.full_name}"


class UniversityApplication(models.Model):
    STATUS_CHOICES = (
        ("applied", "Applied"),
        ("reviewing", "Reviewing"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    university_name = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    applied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.university_name} ({self.student.full_name})"


class ConsultantBooking(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    )

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)
    schedule = models.ForeignKey(ConsultantSchedule, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.student.full_name} with {self.consultant.full_name}"
