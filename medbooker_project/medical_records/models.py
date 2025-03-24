from django.db import models
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

class MedicalRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='medical_records')
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Record #{self.record_id} - {self.patient.full_name}"


class MedicalDocument(models.Model):
    document_id = models.AutoField(primary_key=True)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='medical_documents/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file_name
