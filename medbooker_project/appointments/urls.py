from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.book, name='book'),
    path('confirm/<int:appointment_id>/', views.confirm, name='confirm'),
    path('cancel/<int:appointment_id>/', views.cancel, name='cancel'),
    path('view/<int:appointment_id>/', views.view, name='view'),
]
