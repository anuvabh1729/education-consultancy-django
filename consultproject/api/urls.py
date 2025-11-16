
from django.urls import path, include
from .views import ApiHealthCheckView

urlpatterns = [
    path("health/", ApiHealthCheckView.as_view(), name="api-health"),

    # Version 1 API Routes
    path("v1/accounts/", include("accounts.urls")),
    path("v1/students/", include("students.urls")),
    path("v1/consultants/", include("consultants.urls")),
    path("v1/documents/", include("documents.urls")),
    path("v1/chat/", include("chatbox.urls")),
    path("v1/payments/", include("payments.urls")),
    path("v1/adminpanel/", include("adminpanel.urls")),
]
