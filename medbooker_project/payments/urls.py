from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('processing/<int:appointment_id>/', views.payment_processing, name='payment_processing'),
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('invoice/<int:payment_id>/', views.invoice_generation, name='invoice_generation'),
    path('security/', views.payment_security, name='payment_security'),
    path('subscription/', views.subscription, name='subscription'),
]
