from django.urls import path
from . import views

app_name = 'medical_records'

urlpatterns = [
    path('view/<int:record_id>/', views.view_record, name='view_record'),
    path('create/<int:appointment_id>/', views.create_record, name='create_record'),
    path('upload-documents/', views.upload_documents, name='upload_documents'),
    path('download-prescription/<int:record_id>/', views.download_prescription, name='download_prescription'),
]
