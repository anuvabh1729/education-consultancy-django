from django.db import models
from django.conf import settings
from students.models import StudentProfile
from consultants.models import ConsultantProfile


class Payment(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paypal_order_id = models.CharField(max_length=255)
    paypal_capture_id = models.CharField(max_length=255, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.student.full_name} → {self.consultant.full_name}"


class Invoice(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to="invoices/", null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for Payment {self.payment.id}"
