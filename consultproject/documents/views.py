# documents/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from students.models import StudentProfile
from .models import StudentDocument
from .serializers import (
    DocumentUploadSerializer,
    DocumentListSerializer,
    DocumentReviewSerializer,
)
from .permissions import IsStudent, IsConsultantOrAdmin
from .verification_services import verify_document


class UploadDocumentView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        student = StudentProfile.objects.get(user=request.user)
        serializer = DocumentUploadSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(student=student)
            return Response(
                {"message": "Document uploaded successfully", "data": serializer.data},
                status=201,
            )
        return Response(serializer.errors, status=400)


class StudentDocumentListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get(self, request):
        student = StudentProfile.objects.get(user=request.user)
        documents = StudentDocument.objects.filter(student=student)
        return Response(DocumentListSerializer(documents, many=True).data)


class AllDocumentsListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsConsultantOrAdmin]

    def get(self, request):
        docs = StudentDocument.objects.filter(status="pending")
        return Response(DocumentListSerializer(docs, many=True).data)


class VerifyDocumentView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsConsultantOrAdmin]

    def post(self, request, doc_id):
        try:
            document = StudentDocument.objects.get(id=doc_id)
        except StudentDocument.DoesNotExist:
            return Response({"error": "Document not found"}, status=404)

        serializer = DocumentReviewSerializer(data=request.data)
        if serializer.is_valid():
            decision = serializer.validated_data["decision"]
            comment = serializer.validated_data.get("comment")

            updated = verify_document(
                document=document,
                reviewer=request.user,
                decision=decision,
                comment=comment,
            )
            return Response(
                {"message": f"Document {decision}", "data": DocumentListSerializer(updated).data}
            )
        return Response(serializer.errors, status=400)
