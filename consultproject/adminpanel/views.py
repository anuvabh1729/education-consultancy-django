
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from accounts.permissions import IsAdmin
from . import selectors
from .serializers import SummarySerializer, ChartSerializer


class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        return render(request, "adminpanel/dashboard.html", {})


class StatsSummaryAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        data = {
            "students": selectors.get_student_count(),
            "consultants": selectors.get_consultant_count(),
            "total_revenue": selectors.get_total_revenue(),
            "documents": {d["status"]: d["count"] for d in selectors.get_document_verification_counts()},
        }

        serializer = SummarySerializer(data)
        return Response(serializer.data)


class PaymentsChartAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        payments = selectors.get_recent_payments()

        labels = [str(p["created_at"].date()) for p in payments]
        data = [float(p["amount"]) for p in payments]

        return Response(ChartSerializer({"labels": labels, "data": data}).data)


class DocumentsChartAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        stats = selectors.get_document_verification_counts()

        labels = [item["status"] for item in stats]
        data = [item["count"] for item in stats]

        return Response(ChartSerializer({"labels": labels, "data": data}).data)


class RegistrationChartAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        trends = selectors.get_registration_trends()

        labels = [str(item["day"]) for item in trends]
        data = [item["count"] for item in trends]

        return Response(ChartSerializer({"labels": labels, "data": data}).data)
    
def admin_dashboard(request):
    return render(request, 'adminpanel/dashboard.html')
