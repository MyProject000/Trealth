from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum
from accounts.models import User
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from medical_records.models import MedicalRecord
from payments.models import Payment

@login_required
def dashboard(request):
    # Only admin users can access this view
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('core:home')
    
    # Get system statistics
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()
    completed_appointments = Appointment.objects.filter(status='completed').count()
    total_earnings = Payment.objects.filter(payment_status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Recent registrations
    recent_doctors = Doctor.objects.all().order_by('-user__date_joined')[:5]
    recent_patients = Patient.objects.all().order_by('-user__date_joined')[:5]
    
    # Recent appointments
    recent_appointments = Appointment.objects.all().order_by('-created_at')[:10]
    
    return render(request, 'admin_portal/dashboard.html', {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
        'total_earnings': total_earnings,
        'recent_doctors': recent_doctors,
        'recent_patients': recent_patients,
        'recent_appointments': recent_appointments,
    })

@login_required
def user_management(request):
    # Only admin users can access this view
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('core:home')
    
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    
    return render(request, 'admin_portal/user_management.html', {
        'doctors': doctors,
        'patients': patients,
    })

@login_required
def user_detail(request, user_id):
    # Only admin users can access this view
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('core:home')
    
    user = get_object_or_404(User, id=user_id)
    
    if user.user_type == 'doctor':
        profile = Doctor.objects.get(user=user)
        appointments = Appointment.objects.filter(doctor=profile)
        medical_records = MedicalRecord.objects.filter(doctor=profile)
        payments = None
    elif user.user_type == 'patient':
        profile = Patient.objects.get(user=user)
        appointments = Appointment.objects.filter(patient=profile)
        medical_records = MedicalRecord.objects.filter(patient=profile)
        payments = Payment.objects.filter(patient=profile)
    else:
        profile = None
        appointments = None
        medical_records = None
        payments = None
    
    return render(request, 'admin_portal/user_detail.html', {
        'user': user,
        'profile': profile,
        'appointments': appointments,
        'medical_records': medical_records,
        'payments': payments,
    })

@login_required
def compliance_security(request):
    # Only admin users can access this view
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('core:home')
    
    return render(request, 'admin_portal/compliance_security.html')

@login_required
def analytics_reports(request):
    # Only admin users can access this view
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('core:home')
    
    # Appointments by status
    appointments_by_status = Appointment.objects.values('status').annotate(count=Count('status'))
    
    # Appointments by doctor
    appointments_by_doctor = Appointment.objects.values('doctor__full_name').annotate(count=Count('doctor_id'))
    
    return render(request, 'admin_portal/analytics_reports.html', {
        'appointments_by_status': appointments_by_status,
        'appointments_by_doctor': appointments_by_doctor,
    })
