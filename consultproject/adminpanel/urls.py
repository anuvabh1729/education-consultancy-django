
from django.urls import path
from .views import (
    AdminDashboardView,
    StatsSummaryAPI,
    PaymentsChartAPI,
    DocumentsChartAPI,
    RegistrationChartAPI,
)

urlpatterns = [
    path("dashboard/", AdminDashboardView.as_view()),
    path("stats/summary/", StatsSummaryAPI.as_view()),
    path("stats/payments/", PaymentsChartAPI.as_view()),
    path("stats/documents/", DocumentsChartAPI.as_view()),
    path("stats/registrations/", RegistrationChartAPI.as_view()),
]
