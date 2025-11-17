# documents/models.py
from django.db import models
from django.conf import settings
from students.models import StudentProfile


class StudentDocument(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
    )

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to="documents/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_documents"
    )
    review_comment = models.TextField(blank=True, null=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} - {self.student.full_name}"
