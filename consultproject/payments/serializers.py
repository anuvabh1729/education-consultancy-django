from rest_framework import serializers
from .models import Payment, Invoice


class PaymentCreateSerializer(serializers.Serializer):
    consultant_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class CapturePaymentSerializer(serializers.Serializer):
    order_id = serializers.CharField()
