from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from .models import MedicalRecord
from .forms import MedicalRecordForm
from .forms import DocumentUploadForm
from .models import MedicalDocument
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

@login_required
def view_record(request, record_id):
    # Check if user is a doctor or patient
    if request.user.user_type == 'doctor':
        try:
            doctor = Doctor.objects.get(user=request.user)
            medical_record = get_object_or_404(MedicalRecord, record_id=record_id, doctor=doctor)
            return render(request, 'medical_records/view_record.html', {'record': medical_record})
        except Doctor.DoesNotExist:
            messages.error(request, 'Doctor profile not found.')
            return redirect('doctors:profile')
    
    elif request.user.user_type == 'patient':
        try:
            patient = Patient.objects.get(user=request.user)
            medical_record = get_object_or_404(MedicalRecord, record_id=record_id, patient=patient)
            return render(request, 'medical_records/view_record.html', {'record': medical_record})
        except Patient.DoesNotExist:
            messages.error(request, 'Patient profile not found.')
            return redirect('patients:profile')
    
    else:
        messages.error(request, 'Unauthorized access.')
        return redirect('core:home')

@login_required
def create_record(request, appointment_id):
    # Only doctors can create medical records
    if request.user.user_type != 'doctor':
        messages.error(request, 'Only doctors can create medical records.')
        return redirect('core:home')
    
    try:
        doctor = Doctor.objects.get(user=request.user)
        appointment = get_object_or_404(Appointment, appointment_id=appointment_id, doctor=doctor)
        
        # Check if record already exists
        try:
            medical_record = MedicalRecord.objects.get(appointment=appointment)
            messages.info(request, 'Medical record already exists for this appointment.')
            return redirect('medical_records:view_record', record_id=medical_record.record_id)
        except MedicalRecord.DoesNotExist:
            pass
        
        if request.method == 'POST':
            form = MedicalRecordForm(request.POST)
            if form.is_valid():
                medical_record = form.save(commit=False)
                medical_record.doctor = doctor
                medical_record.patient = appointment.patient
                medical_record.appointment = appointment
                medical_record.created_at = timezone.now()
                medical_record.save()
                
                # Mark appointment as completed
                appointment.status = 'completed'
                appointment.save()
                
                messages.success(request, 'Medical record created successfully.')
                return redirect('medical_records:view_record', record_id=medical_record.record_id)
        else:
            form = MedicalRecordForm()
        
        return render(request, 'medical_records/create_record.html', {
            'form': form,
            'appointment': appointment
        })
    
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('doctors:profile')

@login_required
def upload_documents(request):
    # This would handle document uploads
    return render(request, 'medical_records/upload_documents.html')

@login_required
def download_prescription(request, record_id):
    # Check if user is a doctor or patient
    if request.user.user_type == 'doctor':
        try:
            doctor = Doctor.objects.get(user=request.user)
            medical_record = get_object_or_404(MedicalRecord, record_id=record_id, doctor=doctor)
        except Doctor.DoesNotExist:
            messages.error(request, 'Doctor profile not found.')
            return redirect('doctors:profile')
    
    elif request.user.user_type == 'patient':
        try:
            patient = Patient.objects.get(user=request.user)
            medical_record = get_object_or_404(MedicalRecord, record_id=record_id, patient=patient)
        except Patient.DoesNotExist:
            messages.error(request, 'Patient profile not found.')
            return redirect('patients:profile')
    
    else:
        messages.error(request, 'Unauthorized access.')
        return redirect('core:home')
    
    # For now, just render a prescription view
    return render(request, 'medical_records/prescription.html', {'record': medical_record})


@login_required
def upload_documents(request):
    # Check if user is a doctor or patient
    if request.user.user_type == 'doctor':
        try:
            doctor = Doctor.objects.get(user=request.user)
            records = MedicalRecord.objects.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            messages.error(request, 'Doctor profile not found.')
            return redirect('doctors:profile')
    
    elif request.user.user_type == 'patient':
        try:
            patient = Patient.objects.get(user=request.user)
            records = MedicalRecord.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            messages.error(request, 'Patient profile not found.')
            return redirect('patients:profile')
    
    else:
        messages.error(request, 'Unauthorized access.')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        form.fields['medical_record'].queryset = records
        
        if form.is_valid():
            medical_record = form.cleaned_data['medical_record']
            file = request.FILES['file']
            
            document = MedicalDocument(
                medical_record=medical_record,
                file=file,
                file_name=file.name,
                file_type=file.content_type
            )
            document.save()
            
            messages.success(request, 'Document uploaded successfully.')
            return redirect('medical_records:view_record', record_id=medical_record.record_id)
    else:
        form = DocumentUploadForm()
        form.fields['medical_record'].queryset = records
    
    return render(request, 'medical_records/upload_documents.html', {'form': form})
