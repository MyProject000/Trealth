from django import forms
from .models import Doctor, DoctorAvailability


SPECIALIZATIONS = [
    ("Cardiology", "Cardiology"),
    ("Dermatology", "Dermatology"),
    ("Neurology", "Neurology"),
    ("Orthopedics", "Orthopedics"),
    ("Pediatrics", "Pediatrics"),
    ("Psychiatry", "Psychiatry"),
    ("Ophthalmology", "Ophthalmology"),
]
class DoctorProfileForm(forms.ModelForm):
    specialization = forms.ChoiceField(
        choices=SPECIALIZATIONS,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Specialization"
    )
    class Meta:
        model = Doctor
        fields = ['full_name', 'specialization', 'experience_years', 'license_number', 
                 'consultation_fee', 'hospital_name', 'hospital_location']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'hospital_name': forms.TextInput(attrs={'class': 'form-control'}),
            'hospital_location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ['date', 'start_time', 'end_time', 'max_appointments', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'max_appointments': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }
