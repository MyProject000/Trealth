from django.db import models
from django.conf import settings

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    blood_type = models.CharField(max_length=5)
    allergies = models.CharField(max_length=255, blank=True)
    emergency_contact = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.full_name
