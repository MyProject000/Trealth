from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('medical-history/', views.medical_history, name='medical_history'),
    path('prescriptions/', views.prescriptions, name='prescriptions'),
    path('billing-payments/', views.billing_payments, name='billing_payments'),
    path('search-doctors/', views.search_doctors, name='search_doctors'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
]
