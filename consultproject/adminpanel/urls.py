
from django.urls import path

from .views import (
    
    StatsSummaryAPI,
    PaymentsChartAPI,
    DocumentsChartAPI,
    RegistrationChartAPI,
    admin_dashboard
)

from . import views

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("stats/summary/", StatsSummaryAPI.as_view()),
    path("stats/payments/", PaymentsChartAPI.as_view()),
    path("stats/documents/", DocumentsChartAPI.as_view()),
    path("stats/registrations/", RegistrationChartAPI.as_view()),
]
