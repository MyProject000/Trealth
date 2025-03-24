from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment

@login_required
def book(request):
    # Appointment booking logic
    return render(request, 'appointments/book.html')

@login_required
def confirm(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    return render(request, 'appointments/confirm.html', {'appointment': appointment})

@login_required
def cancel(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    return render(request, 'appointments/cancel.html', {'appointment': appointment})

@login_required
def view(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    return render(request, 'appointments/view.html', {'appointment': appointment})
