from django import forms
from .models import Patient
from doctors.models import Doctor
from appointments.models import Appointment

class PatientProfileForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    
    BLOOD_TYPE_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
    
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    blood_type = forms.ChoiceField(choices=BLOOD_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    
    class Meta:
        model = Patient
        fields = ['full_name', 'date_of_birth', 'gender', 'blood_type', 'allergies', 
                  'emergency_contact', 'location']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'allergies': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AppointmentBookingForm(forms.Form):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a doctor"
    )
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    time_slot = forms.ChoiceField(
        choices=[
            ('9-10', '9:00 AM - 10:00 AM'),
            ('10-11', '10:00 AM - 11:00 AM'),
            ('11-12', '11:00 AM - 12:00 PM'),
            ('12-1', '12:00 PM - 1:00 PM'),
            ('1-2', '1:00 PM - 2:00 PM'),
            ('2-3', '2:00 PM - 3:00 PM'),
            ('3-4', '3:00 PM - 4:00 PM'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    symptoms_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )
