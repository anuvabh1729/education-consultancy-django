from django import forms
from .models import Booking, ConsultantProfile

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['consultant', 'client_name', 'client_email', 'consultation_type', 'start_datetime', 'duration_minutes', 'notes']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        # allow passing a consultant instance to hide the field in the template
        consultant = kwargs.pop('consultant', None)
        super().__init__(*args, **kwargs)
        if consultant:
            self.fields['consultant'].initial = consultant.pk
            self.fields['consultant'].widget = forms.HiddenInput()
        else:
            self.fields['consultant'].queryset = ConsultantProfile.objects.filter(verified=True)
