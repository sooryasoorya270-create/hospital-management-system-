from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('doctors/',views.doctors,name='doctors'),
    path('contact/',views.contact,name='contact'),
    path('departments/',views.departments,name='departments'),
    path('booking/', views.booking,name='booking'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('smart_recommendation/', views.smart_recommendation, name='smart_recommendation'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    
]
