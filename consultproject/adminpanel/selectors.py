
from students.models import StudentProfile
from consultants.models import ConsultantProfile
from documents.models import StudentDocument
from payments.models import Payment
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.utils.timezone import now, timedelta

User = get_user_model()


def get_student_count():
    return StudentProfile.objects.count()


def get_consultant_count():
    return ConsultantProfile.objects.count()


def get_document_verification_counts():
    return StudentDocument.objects.values("status").annotate(count=Count("id"))


def get_total_revenue():
    return Payment.objects.filter(status="completed").aggregate(total=Sum("amount"))["total"] or 0


def get_recent_payments():
    last_7 = now() - timedelta(days=7)
    return (
        Payment.objects.filter(created_at__gte=last_7)
        .values("created_at", "amount")
        .order_by("created_at")
    )


def get_registration_trends():
    last_30 = now() - timedelta(days=30)
    return (
        User.objects.filter(date_joined__gte=last_30)
        .extra(select={"day": "date(date_joined)"})
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )
