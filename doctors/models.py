from django.db import models
from django.conf import settings

class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    full_name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    experience_years = models.IntegerField()
    license_number = models.CharField(max_length=50)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    hospital_name = models.CharField(max_length=255)
    hospital_location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.full_name

class DoctorAvailability(models.Model):
    availability_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_appointments = models.IntegerField()
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.doctor.full_name} - {self.date}"

class DoctorSlots(models.Model):
    slots_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    slot_9_10 = models.IntegerField(default=0)
    slot_10_11 = models.IntegerField(default=0)
    slot_11_12 = models.IntegerField(default=0)
    slot_12_1 = models.IntegerField(default=0)
    slot_1_2 = models.IntegerField(default=0)
    slot_2_3 = models.IntegerField(default=0)
    slot_3_4 = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.doctor.full_name} - {self.date}"
