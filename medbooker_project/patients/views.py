from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Patient
from .forms import PatientProfileForm, AppointmentBookingForm
from doctors.models import Doctor, DoctorAvailability, DoctorSlots
from appointments.models import Appointment
from medical_records.models import MedicalRecord
from payments.models import Payment

@login_required
def dashboard(request):
    try:
        patient = Patient.objects.get(user=request.user)
        
        # Get upcoming appointments
        upcoming_appointments = Appointment.objects.filter(
            patient=patient,
            appointment_date__gte=timezone.now(),
            status='scheduled'
        ).order_by('appointment_date')
        
        # Get recent medical records
        recent_records = MedicalRecord.objects.filter(
            patient=patient
        ).order_by('-created_at')[:5]
        
        context = {
            'patient': patient,
            'upcoming_appointments': upcoming_appointments,
            'recent_records': recent_records,
        }
        return render(request, 'patients/dashboard.html', context)
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found. Please complete your profile.')
        return redirect('patients:profile')

@login_required
def profile(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        patient = Patient(user=request.user, full_name=f"{request.user.first_name} {request.user.last_name}")
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('patients:dashboard')
    else:
        form = PatientProfileForm(instance=patient)
    
    return render(request, 'patients/profile.html', {'form': form})

@login_required
def search_doctors(request):
    specialization = request.GET.get('specialization', '')
    name = request.GET.get('name', '')
    
    doctors = Doctor.objects.all()
    
    if specialization:
        doctors = doctors.filter(specialization__icontains=specialization)
    
    if name:
        doctors = doctors.filter(full_name__icontains=name)
    
    return render(request, 'patients/search_doctors.html', {
        'doctors': doctors,
        'specialization': specialization,
        'name': name
    })

@login_required
def book_appointment(request):
    try:
        patient = Patient.objects.get(user=request.user)
        
        if request.method == 'POST':
            form = AppointmentBookingForm(request.POST)
            if form.is_valid():
                doctor_id = form.cleaned_data['doctor'].doctor_id
                appointment_date = form.cleaned_data['appointment_date']
                time_slot = form.cleaned_data['time_slot']
                symptoms = form.cleaned_data['symptoms_description']
                
                # Get the doctor
                doctor = Doctor.objects.get(doctor_id=doctor_id)
                
                # Convert time slot to datetime
                hour_map = {
                    '9-10': 9, '10-11': 10, '11-12': 11, 
                    '12-1': 12, '1-2': 13, '2-3': 14, '3-4': 15
                }
                hour = hour_map[time_slot]
                appointment_datetime = datetime.combine(
                    appointment_date, 
                    datetime.min.time().replace(hour=hour)
                )
                
                # Check if doctor is available on that date
                try:
                    availability = DoctorAvailability.objects.get(
                        doctor=doctor,
                        date=appointment_date,
                        status='available'
                    )
                    
                    # Check if the slot is available
                    try:
                        slots = DoctorSlots.objects.get(doctor=doctor, date=appointment_date)
                        slot_attr = f"slot_{time_slot.replace('-', '_')}"
                        
                        if getattr(slots, slot_attr) == 0:  # 0 means available
                            # Create the appointment
                            new_appointment = Appointment.objects.create(
                                doctor=doctor,
                                patient=patient,
                                appointment_date=appointment_datetime,
                                status='scheduled',
                                symptoms_description=symptoms
                            )
                            
                            # Update the slot to booked (1)
                            setattr(slots, slot_attr, 1)
                            slots.save()
                            
                            messages.success(request, 'Appointment booked successfully!')
                            return redirect('patients:appointment_detail', appointment_id=new_appointment.appointment_id)
                        else:
                            messages.error(request, 'This time slot is already booked.')
                    except DoctorSlots.DoesNotExist:
                        messages.error(request, 'Doctor slots not available for this date.')
                except DoctorAvailability.DoesNotExist:
                    messages.error(request, 'Doctor is not available on this date.')
        else:
            form = AppointmentBookingForm()
        
        return render(request, 'patients/book_appointment.html', {'form': form})
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found. Please complete your profile.')
        return redirect('patients:profile')

@login_required
def appointment_detail(request, appointment_id):
    try:
        patient = Patient.objects.get(user=request.user)
        appointment = get_object_or_404(Appointment, appointment_id=appointment_id, patient=patient)
        
        # Check if medical record exists
        try:
            medical_record = MedicalRecord.objects.get(appointment=appointment)
            has_record = True
        except MedicalRecord.DoesNotExist:
            medical_record = None
            has_record = False
        
        # Fetch all payments related to this appointment
        payments = Payment.objects.filter(appointment=appointment)
        has_payment = payments.exists()
        
        # If you want to show only the most recent payment:
        payment = payments.order_by('-payment_date').first() if has_payment else None
        
        if request.method == 'POST':
            action = request.POST.get('action')
            
            if action == 'cancel':
                if appointment.status == 'scheduled':
                    appointment.status = 'cancelled'
                    appointment.cancel_reason = request.POST.get('cancel_reason', 'Cancelled by patient')
                    appointment.save()
                    
                    # Free up the slot
                    date = appointment.appointment_date.date()
                    hour = appointment.appointment_date.hour
                    
                    # Map hour back to slot
                    slot_map = {
                        9: '9_10', 10: '10_11', 11: '11_12', 
                        12: '12_1', 13: '1_2', 14: '2_3', 15: '3_4'
                    }
                    
                    if hour in slot_map:
                        slot_attr = f"slot_{slot_map[hour]}"
                        try:
                            slots = DoctorSlots.objects.get(doctor=appointment.doctor, date=date)
                            setattr(slots, slot_attr, 0)  # 0 means available
                            slots.save()
                        except DoctorSlots.DoesNotExist:
                            pass
                    
                    messages.success(request, 'Appointment cancelled successfully.')
                else:
                    messages.error(request, 'Cannot cancel a completed or already cancelled appointment.')
        
        return render(request, 'patients/appointment_detail.html', {
            'appointment': appointment,
            'medical_record': medical_record,
            'has_record': has_record,
            'payment': payment,
            'has_payment': has_payment,
            'payments': payments,  # Pass all payments if needed in the template
        })
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found. Please complete your profile.')
        return redirect('patients:profile')


@login_required
def medical_history(request):
    try:
        patient = Patient.objects.get(user=request.user)
        medical_records = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')
        return render(request, 'patients/medical_history.html', {'medical_records': medical_records})
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found. Please complete your profile.')
        return redirect('patients:profile')

@login_required
def prescriptions(request):
    try:
        patient = Patient.objects.get(user=request.user)
        medical_records = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')
        return render(request, 'patients/prescriptions.html', {'medical_records': medical_records})
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found. Please complete your profile.')
        return redirect('patients:profile')

@login_required
def billing_payments(request):
    try:
        patient = Patient.objects.get(user=request.user)
        payments = Payment.objects.filter(patient=patient).order_by('-payment_date')
        
        # Get unpaid appointments
        unpaid_appointments = Appointment.objects.filter(
            patient=patient,
            status='completed'
        ).exclude(
            payments__payment_status='completed'
        )
        
        return render(request, 'patients/billing_payments.html', {
            'payments': payments,
            'unpaid_appointments': unpaid_appointments,
            'patient': patient
        })
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found. Please complete your profile.')
        return redirect('patients:profile')
