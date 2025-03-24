from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserLoginForm, UserSignupForm
from doctors.models import Doctor
from patients.models import Patient

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in!')
                
                # Redirect based on user_type
                if user.user_type == 'doctor':
                    return redirect('doctors:dashboard')
                elif user.user_type == 'patient':
                    return redirect('patients:dashboard')
                else:
                    return redirect('admin:index')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

# accounts/views.py
def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email  # Set username to email
            user.save()
            
            # Only create a minimal record - just enough to create the relation
            if user.user_type == 'doctor':
                # Add default values for all required fields
                Doctor.objects.create(
                    user=user,
                    full_name=f"{user.first_name} {user.last_name}",
                    experience_years=0,  # Default value
                    specialization="Not specified",  # Default value
                    license_number="Pending",  # Default value
                    consultation_fee=0.00,  # Default value
                    hospital_name="Not specified",  # Default value
                    hospital_location="Not specified"  # Default value
                )
                messages.success(request, 'Doctor account created successfully. Please complete your profile.')
                login(request, user)
                return redirect('doctors:profile')
            
            elif user.user_type == 'patient':
                # Create patient with default/minimal values for required fields
                Patient.objects.create(
                    user=user,
                    full_name=f"{user.first_name} {user.last_name}",
                    date_of_birth="2000-01-01",  # Default date
                    gender="other",              # Default gender
                    blood_type="A+",             # Default blood type
                    emergency_contact="None provided",
                    location="Not specified"
                )
                messages.success(request, 'Patient account created successfully. Please complete your profile.')
                login(request, user)
                return redirect('patients:profile')
    else:
        form = UserSignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')

def password_reset(request):
    # Simple placeholder for password reset
    return render(request, 'accounts/password_reset.html')
