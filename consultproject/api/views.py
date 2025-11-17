
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now


class ApiHealthCheckView(APIView):
    def get(self, request):
        return Response({
            "status": "OK",
            "message": "API is running successfully.",
            "timestamp": now(),
            "version": "v1",
            "apps": [
                "accounts",
                "students",
                "consultants",
                "documents",
                "chatbox",
                "payments",
                "adminpanel"
            ]
        })
