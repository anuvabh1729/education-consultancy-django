from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, get_user_model, logout 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import ContactMessage , User
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

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ROLE BASED REDIRECT
            if user.role == "student":
                return redirect("/students/dashboard/")
            elif user.role == "consultant":
                return redirect("/consultants/dashboard/")
            elif user.role == "admin":
                return redirect("/adminpanel/dashboard/")
            else:
                return redirect("/")  # fallback

        return render(request, "accounts/login.html", {"error": "Invalid credentials"})

    return render(request, "accounts/login.html")

 
User = get_user_model()

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/signup.html", {
                "error": "Username already exists. Please choose another one."
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            role=role
        )

        login(request, user)

        # Redirect based on role
        if user.role == "student":
            return redirect("/students/basic-info/")
        elif user.role == "consultant":
            return redirect("/consultants/profile/")
        elif user.role == "admin":
            return redirect("/adminpanel/dashboard/")
        else:
            return redirect("/")

    return render(request, "accounts/signup.html")

def welcome_view(request):
    return render(request, "accounts/welcome.html")

def services_view(request):
    return render(request, "accounts/services.html")

def about_view(request):
    return render(request, "accounts/about.html")

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        return render(request, "accounts/contact.html", {"success": True})

    return render(request, "accounts/contact.html")

def feedback_view(request):
    return render(request, "accounts/feedback.html")

def logout_view(request):
    logout(request)
    return redirect("/")