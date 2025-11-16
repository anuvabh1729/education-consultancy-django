from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import (
    RegisterStudentSerializer,
    RegisterConsultantSerializer,
    LoginSerializer,
    GoogleAuthSerializer,
    UserSerializer
)
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

def generate_jwt(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class RegisterStudentView(APIView):
    def post(self, request):
        serializer = RegisterStudentSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Student registered successfully",
                "tokens": generate_jwt(user),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterConsultantView(APIView):
    def post(self, request):
        serializer = RegisterConsultantSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Consultant registered successfully",
                "tokens": generate_jwt(user),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            return Response({
                "message": "Login successful",
                "tokens": generate_jwt(user),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginView(APIView):
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            google_id = serializer.validated_data["google_id"]

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": email.split("@")[0],
                    "role": "student",
                    "google_id": google_id,
                },
            )

            if user.google_id is None:
                user.google_id = google_id
                user.save()

            return Response({
                "message": "Google login successful",
                "tokens": generate_jwt(user),
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
