from django import forms
from .models import MedicalRecord

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'treatment_plan']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class DocumentUploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    medical_record = forms.ModelChoiceField(
        queryset=MedicalRecord.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
