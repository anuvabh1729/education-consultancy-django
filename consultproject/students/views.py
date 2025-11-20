from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.permissions import IsStudent
from .models import (
    StudentProfile,
    StudentDocument,
    UniversityApplication,
    StudentInfo,
    CounsellingSession,
)
from .forms import StudentInfoForm, DocumentUploadForm
from consultants.models import ConsultantProfile, ConsultantSchedule
from .serializers import (
    StudentProfileSerializer,
    StudentDocumentSerializer,
    UniversityApplicationSerializer,
)


class StudentProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        return Response(StudentProfileSerializer(profile).data)

    def post(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Profile updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadDocumentView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        student = StudentProfile.objects.get(user=request.user)
        serializer = StudentDocumentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(student=student)
            return Response({"message": "Document uploaded", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UniversityApplicationView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        student = StudentProfile.objects.get(user=request.user)
        serializer = UniversityApplicationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(student=student)
            return Response({"message": "Application submitted", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        student = StudentProfile.objects.get(user=request.user)
        apps = UniversityApplication.objects.filter(student=student)
        return Response(UniversityApplicationSerializer(apps, many=True).data)


class BookConsultantView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        student = StudentProfile.objects.get(user=request.user)
        consultant_id = request.data.get("consultant_id")
        schedule_id = request.data.get("schedule_id")

        consultant = ConsultantProfile.objects.get(id=consultant_id)
        schedule = ConsultantSchedule.objects.get(id=schedule_id)


        return Response({
            "message": "Consultant booked successfully",
            
        })


def student_profile(request):
    return render(request, "students/profile.html")


#updated made by Hash
@login_required
def student_basic_info(request):
    if request.method == "POST":
        StudentInfo.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            phone=request.POST.get("phone"),
            date_of_birth=request.POST.get("dob"),
            country_preference=request.POST.get("country"),
            course_preference=request.POST.get("course"),
        )
        return redirect("/students/dashboard/")

    return render(request, "students/basic_info.html")

@login_required
def student_dashboard(request):
    try:
        info = StudentInfo.objects.get(user=request.user)
    except StudentInfo.DoesNotExist:
        return redirect("/students/basic-info/")
    return render(request, "students/dashboard.html", {
        "info": info
    })

@login_required
def student_profile(request):
    info = StudentInfo.objects.get(user=request.user)
    return render(request, "students/profile.html", {"info": info})

@login_required
def edit_student_profile(request):
    info = StudentInfo.objects.get(user=request.user)

    if request.method == "POST":
        form = StudentInfoForm(request.POST, request.FILES, instance=info)
        if form.is_valid():
            form.save()
            return redirect("/students/profile/")
    else:
        form = StudentInfoForm(instance=info)

    return render(request, "students/edit_profile.html", {"form": form, "info": info})

@login_required
def upload_documents(request):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            return redirect("/students/upload-documents/")
    else:
        form = DocumentUploadForm()

    documents = StudentDocument.objects.filter(user=request.user)

    return render(request, "students/upload_documents.html", {
        "form": form,
        "documents": documents
    })


@login_required
def explore_universities(request):
    universities = [
        {
            "name": "Manipal University",
            "country": "India",
            "image": "https://images.unsplash.com/photo-1580584126903-1fea005f89ce",
            "desc": "Top private university known for Engineering, Medical, MBA and more."
        },
        {
            "name": "Amity University",
            "country": "India",
            "image": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b",
            "desc": "One of India's leading private universities with global campuses."
        },
        {
            "name": "Christ University",
            "country": "India",
            "image": "https://images.unsplash.com/photo-1557804506-669a67965ba0",
            "desc": "Premier university for commerce, law, psychology and arts."
        },
        {
            "name": "Lovely Professional University (LPU)",
            "country": "India",
            "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1",
            "desc": "Among the largest private universities with strong placement records."
        },
    ]

    return render(request, "students/universities.html", {"universities": universities})


def programs_page(request, uni_id):
    # Example program data (later you can fetch from database)
    programs = [
        "B.Tech (Computer Science)",
        "MBA (Finance / HR / Marketing)",
        "BBA",
        "MBBS",
        "MSc Data Science",
        "B.Sc Nursing",
        "BCA",
        "B.Sc Computer Science",
        "LLB (Law)",
    ]

    return render(request, "students/programs.html", {
        "programs": programs,
        "uni_id": uni_id
    })

def explore_universities(request):
    universities = [
        {"id": 1, "name": "Manipal University", "desc": "Top private engineering university"},
        {"id": 2, "name": "Amity University", "desc": "Famous for business & management programs"},
        {"id": 3, "name": "Christ University", "desc": "Top-rated for commerce & arts"},
    ]
    return render(request, "students/universities.html", {"universities": universities})

@login_required
def consultant_list(request):
    consultants = User.objects.filter(role="consultant")
    return render(request, "students/consultants_list.html", {"consultants": consultants})


@login_required
def book_session(request, consultant_id):
    consultant = User.objects.get(id=consultant_id)

    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")
        message = request.POST.get("message")

        CounsellingSession.objects.create(
            student=request.user,
            consultant=consultant,
            date=date,
            time=time,
            message=message
        )

        return redirect("my_sessions")

    return render(request, "students/book_session.html", {"consultant": consultant})


@login_required
def my_sessions(request):
    sessions = CounsellingSession.objects.filter(student=request.user)
    return render(request, "students/my_sessions.html", {"sessions": sessions})

