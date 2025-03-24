from django.shortcuts import render
from doctors.models import Doctor
from .forms import ContactForm
from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    # Get some featured doctors
    featured_doctors = Doctor.objects.all()[:4]
    return render(request, 'core/home.html', {'featured_doctors': featured_doctors})

def about(request):
    return render(request, 'core/about.html')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def contact(request):
    return render(request, 'core/contact.html')

def faqs(request):
    return render(request, 'core/faqs.html')

def terms(request):
    return render(request, 'core/terms.html')

def find_doctor(request):
    # Fetch all doctors initially
    doctors = Doctor.objects.all()
    
    # Get search parameters from the request
    name = request.GET.get('name', '')
    specialization = request.GET.get('specialization', '')
    location = request.GET.get('location', '')
    
    # Apply filters based on search parameters
    if name:
        doctors = doctors.filter(full_name__icontains=name)
    
    if specialization:
        doctors = doctors.filter(specialization__iexact=specialization)
    
    if location:
        doctors = doctors.filter(hospital_location__icontains=location)
    
    # Render the template with filtered results
    return render(request, 'core/find_doctor.html', {
        'doctors': doctors,
        'name': name,
        'specialization': specialization,
        'location': location,
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # In a real implementation, this would send an email
            messages.success(request, 'Your message has been sent. We will get back to you soon!')
            return redirect('core:contact')
    else:
        form = ContactForm()
    
    return render(request, 'core/contact.html', {'form': form})
