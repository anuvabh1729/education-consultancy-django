from django import forms
from .models import StudentInfo, StudentDocument

class StudentInfoForm(forms.ModelForm):
    class Meta:
        model = StudentInfo
        fields = [
            "full_name",
            "phone",
            "country",
            "target_course",
            "target_country",
            "profile_picture",
        ]


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = StudentDocument
        fields = ['document_name', 'file']



        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "target_course": forms.TextInput(attrs={"class": "form-control"}),
            "target_country": forms.TextInput(attrs={"class": "form-control"}),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }