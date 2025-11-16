# documents/verification_services.py
from django.utils import timezone


def verify_document(document, reviewer, decision, comment=None):
    document.status = decision
    document.reviewer = reviewer
    document.review_comment = comment
    document.verified_at = timezone.now()
    document.save()
    return document
