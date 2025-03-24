from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment
from .forms import PaymentProcessingForm
from appointments.models import Appointment
from patients.models import Patient

@login_required
def payment_processing(request, appointment_id):
    # Only patients can make payments
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can make payments.')
        return redirect('core:home')
    
    try:
        patient = Patient.objects.get(user=request.user)
        appointment = get_object_or_404(Appointment, appointment_id=appointment_id, patient=patient)
        
        # Check if appointment is already paid
        try:
            payment = Payment.objects.get(appointment=appointment, payment_status='completed')
            messages.info(request, 'This appointment is already paid.')
            return redirect('patients:appointment_detail', appointment_id=appointment_id)
        except Payment.DoesNotExist:
            # Create a new payment
            payment = Payment(
                patient=patient,
                appointment=appointment,
                amount=appointment.doctor.consultation_fee,
                payment_status='pending'
            )
            payment.save()
        
        if request.method == 'POST':
            form = PaymentProcessingForm(request.POST)
            if form.is_valid():
                # In a real implementation, this would integrate with a payment gateway
                payment.payment_status = 'completed'
                payment.save()
                
                messages.success(request, 'Payment processed successfully!')
                return redirect('payments:payment_success', payment_id=payment.payment_id)
        else:
            form = PaymentProcessingForm()
        
        return render(request, 'payments/payment_processing.html', {
            'form': form,
            'payment': payment,
            'appointment': appointment
        })
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found.')
        return redirect('patients:profile')

@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, payment_id=payment_id)
    return render(request, 'payments/payment_success.html', {'payment': payment})

@login_required
def invoice_generation(request, payment_id):
    payment = get_object_or_404(Payment, payment_id=payment_id)
    return render(request, 'payments/invoice.html', {'payment': payment})

@login_required
def payment_security(request):
    return render(request, 'payments/payment_security.html')

@login_required
def subscription(request):
    return render(request, 'payments/subscription.html')
