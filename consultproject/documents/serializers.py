# documents/serializers.py
from rest_framework import serializers
from .models import StudentDocument


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocument
        fields = ("id", "document_type", "file")


class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocument
        fields = "__all__"


class DocumentReviewSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=["verified", "rejected"])
    comment = serializers.CharField(required=False)
