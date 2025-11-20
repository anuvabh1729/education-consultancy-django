from django.db import models
from django.conf import settings
from consultants.models import ConsultantProfile, ConsultantSchedule
from accounts.models import User

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


# class StudentDocument(models.Model):
#     STATUS_CHOICES = (
#         ("pending", "Pending"),
#         ("verified", "Verified"),
#         ("rejected", "Rejected"),
#     )

#     student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
#     document_type = models.CharField(max_length=100)
#     file = models.FileField(upload_to="student_documents/")
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

#     upload_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.document_type} - {self.student.full_name}"


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


class StudentInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    target_course = models.CharField(max_length=150)
    target_country = models.CharField(max_length=100)

    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_name} - {self.student.full_name}"


class StudentDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # TEMP = null allowed
    document_name = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class CounsellingSession(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_sessions")
    consultant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="consultant_sessions")
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Pending")  # Pending / Accepted / Rejected
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} → {self.consultant.username} ({self.date})"
