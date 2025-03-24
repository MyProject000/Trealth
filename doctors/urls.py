from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('schedule-management/', views.schedule_management, name='schedule_management'),
    path('manage-appointments/', views.manage_appointments, name='manage_appointments'),
    path('medical-records/', views.medical_records, name='medical_records'),
    path('prescriptions/', views.create_prescription, name='create_prescription'),
    path('payment-info/', views.payment_info, name='payment_info'),
    path('availability/create/', views.create_availability, name='create_availability'),
    path('availability/update/<int:availability_id>/', views.update_availability, name='update_availability'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
]
