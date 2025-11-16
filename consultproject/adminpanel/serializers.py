# adminpanel/serializers.py
from rest_framework import serializers


class SummarySerializer(serializers.Serializer):
    students = serializers.IntegerField()
    consultants = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    documents = serializers.DictField()


class ChartSerializer(serializers.Serializer):
    labels = serializers.ListField()
    data = serializers.ListField()
