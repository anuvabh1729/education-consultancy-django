from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.permissions import IsStudent
from students.models import StudentProfile
from consultants.models import ConsultantProfile
from .models import Payment, Invoice
from .serializers import (
    PaymentCreateSerializer,
    PaymentSerializer,
    CapturePaymentSerializer,
)
from .paypal_services import create_paypal_order, capture_paypal_order


class CreatePayPalOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)

        if serializer.is_valid():
            student = StudentProfile.objects.get(user=request.user)
            consultant = ConsultantProfile.objects.get(id=serializer.validated_data["consultant_id"])
            amount = serializer.validated_data["amount"]

            order = create_paypal_order(amount)

            paypal_order_id = order.get("id")
            approval_link = next(
                (link["href"] for link in order["links"] if link["rel"] == "approve"), None
            )

            payment = Payment.objects.create(
                student=student,
                consultant=consultant,
                amount=amount,
                paypal_order_id=paypal_order_id,
                status="pending",
            )

            return Response({
                "approval_url": approval_link,
                "payment_id": payment.id,
                "paypal_order_id": paypal_order_id,
            })

        return Response(serializer.errors, status=400)


class CapturePayPalOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        serializer = CapturePaymentSerializer(data=request.data)

        if serializer.is_valid():
            order_id = serializer.validated_data["order_id"]

            capture_data = capture_paypal_order(order_id)

            try:
                payment = Payment.objects.get(paypal_order_id=order_id)
            except Payment.DoesNotExist:
                return Response({"error": "Payment record not found"}, status=404)

            if capture_data.get("status") == "COMPLETED":
                payment.status = "completed"
                payment.paypal_capture_id = capture_data["purchase_units"][0]["payments"]["captures"][0]["id"]
                payment.save()

                Invoice.objects.create(payment=payment)

                return Response({
                    "message": "Payment successful",
                    "payment": PaymentSerializer(payment).data,
                })

            else:
                payment.status = "failed"
                payment.save()

                return Response({"error": "Payment failed"}, status=400)

        return Response(serializer.errors, status=400)


class ListStudentPaymentsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get(self, request):
        student = StudentProfile.objects.get(user=request.user)
        payments = Payment.objects.filter(student=student)
        return Response(PaymentSerializer(payments, many=True).data)
