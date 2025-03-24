from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Doctor, DoctorAvailability, DoctorSlots
from .forms import DoctorProfileForm, DoctorAvailabilityForm
from appointments.models import Appointment
from medical_records.models import MedicalRecord
from medical_records.forms import MedicalRecordForm
from django.utils import timezone

@login_required
def dashboard(request):
    # Get the doctor profile
    try:
        doctor = Doctor.objects.get(user=request.user)
        
        # Get today's appointments
        today = timezone.now().date()
        today_appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__date=today
        ).order_by('appointment_date')
        
        # Get upcoming appointments
        upcoming_appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__date__gt=today,
            status='scheduled'
        ).order_by('appointment_date')
        
        # Count statistics
        total_appointments = Appointment.objects.filter(doctor=doctor).count()
        completed_appointments = Appointment.objects.filter(doctor=doctor, status='completed').count()
        
        context = {
            'doctor': doctor,
            'today_appointments': today_appointments,
            'upcoming_appointments': upcoming_appointments,
            'total_appointments': total_appointments,
            'completed_appointments': completed_appointments
        }
        return render(request, 'doctors/dashboard.html', context)
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found. Please complete your profile.')
        return redirect('doctors:profile')

@login_required
def profile(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        doctor = Doctor(user=request.user, full_name=f"{request.user.first_name} {request.user.last_name}")
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('doctors:dashboard')
    else:
        form = DoctorProfileForm(instance=doctor)
    
    return render(request, 'doctors/profile.html', {'form': form})

@login_required
def schedule_management(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        availabilities = DoctorAvailability.objects.filter(doctor=doctor).order_by('date')
        return render(request, 'doctors/schedule_management.html', {'availabilities': availabilities})
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found. Please complete your profile.')
        return redirect('doctors:profile')

@login_required
def create_availability(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        
        if request.method == 'POST':
            form = DoctorAvailabilityForm(request.POST)
            if form.is_valid():
                availability = form.save(commit=False)
                availability.doctor = doctor
                availability.save()
                
                # Create doctor slots for this availability
                slots = DoctorSlots(
                    doctor=doctor,
                    date=availability.date,
                    slot_9_10=0,
                    slot_10_11=0,
                    slot_11_12=0,
                    slot_12_1=0,
                    slot_1_2=0,
                    slot_2_3=0,
                    slot_3_4=0
                )
                slots.save()
                
                messages.success(request, 'Availability added successfully.')
                return redirect('doctors:schedule_management')
        else:
            form = DoctorAvailabilityForm()
        
        return render(request, 'doctors/create_availability.html', {'form': form})
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found. Please complete your profile.')
        return redirect('doctors:profile')

@login_required
def update_availability(request, availability_id):
    try:
        doctor = Doctor.objects.get(user=request.user)
        availability = get_object_or_404(DoctorAvailability, availability_id=availability_id, doctor=doctor)
        
        if request.method == 'POST':
            form = DoctorAvailabilityForm(request.POST, instance=availability)
            if form.is_valid():
                form.save()
                messages.success(request, 'Availability updated successfully.')
                return redirect('doctors:schedule_management')
        else:
            form = DoctorAvailabilityForm(instance=availability)
        
        return render(request, 'doctors/update_availability.html', {'form': form})
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found. Please complete your profile.')
        return redirect('doctors:profile')

@login_required
def manage_appointments(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')
        return render(request, 'doctors/manage_appointments.html', {'appointments': appointments})
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found. Please complete your profile.')
        return redirect('doctors:profile')

@login_required
def appointment_detail(request, appointment_id):
    try:
        doctor = Doctor.objects.get(user=request.user)
        appointment = get_object_or_404(Appointment, appointment_id=appointment_id, doctor=doctor)
        
        # Check if medical record exists
        try:
            medical_record = MedicalRecord.objects.get(appointment=appointment)
            has_record = True
        except MedicalRecord.DoesNotExist:
            medical_record = None
            has_record = False
        
        if request.method == 'POST':
            action = request.POST.get('action')
            
            if action == 'complete':
                appointment.status = 'completed'
                appointment.save()
                messages.success(request, 'Appointment marked as completed.')
            elif action == 'cancel':
                appointment.status = 'cancelled'
                appointment.cancel_reason = request.POST.get('cancel_reason')
                appointment.save()
                messages.success(request, 'Appointment cancelled.')
        
        return render(request, 'doctors/appointment_detail.html', {
            'appointment': appointment,
            'medical_record': medical_record,
            'has_record': has_record
        })
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found. Please complete your profile.')
        return redirect('doctors:profile')

@login_required
def medical_records(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        records = MedicalRecord.objects.filter(doctor=doctor).order_by('-created_at')
        return render(request, 'doctors/medical_records.html', {'records': records})
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found. Please complete your profile.')
        return redirect('doctors:profile')

@login_required
def create_prescription(request):
    # This view will be implemented in the medical_records app
    return redirect('medical_records:create_record')

@login_required
def payment_info(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        # Get all completed appointments
        completed_appointments = Appointment.objects.filter(doctor=doctor, status='completed')
        
        total_earnings = doctor.consultation_fee * completed_appointments.count()
        
        return render(request, 'doctors/payment_info.html', {
            'doctor': doctor,
            'completed_appointments': completed_appointments,
            'total_earnings': total_earnings
        })
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found. Please complete your profile.')
        return redirect('doctors:profile')
