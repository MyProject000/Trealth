from django.urls import path
from . import views

app_name = 'admin_portal'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-management/', views.user_management, name='user_management'),
    path('user-detail/<int:user_id>/', views.user_detail, name='user_detail'),
    path('compliance-security/', views.compliance_security, name='compliance_security'),
    path('analytics-reports/', views.analytics_reports, name='analytics_reports'),
]
