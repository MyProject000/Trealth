from django.urls import path
from . import views
from django.urls import include
app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('contact/', views.contact, name='contact'),
    path('faqs/', views.faqs, name='faqs'),
    path('terms/', views.terms, name='terms'),
    path('find-doctor/', views.find_doctor, name='find_doctor'),
    path('payments/', include('payments.urls')),

]
