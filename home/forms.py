from django import forms
from . models import booking,contact

from django import forms
from .models import booking, contact, PatientProfile


class BookingForm(forms.ModelForm):

    class Meta:
        model = booking

        fields = [
            'patient_name',
            'patient_email',
            'patient_phone',
            'doctor_name',
            'booking_ON',
            'booking_time',
        ]

        labels = {
            'patient_name': 'Patient Name',
            'patient_email': 'Patient Email',
            'patient_phone': 'Patient Phone',
            'doctor_name': 'Selected Doctor',
            'booking_ON': 'Appointment Date',
            'booking_time': 'Appointment Time',
        }

        widgets = {
            'patient_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Patient Name',
                'readonly': 'readonly',
            }),

            'patient_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
            }),

            'patient_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
            }),

            'doctor_name': forms.Select(attrs={
                'class': 'form-control',
            }),

            'booking_ON': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': forms.fields.DateField().widget.attrs.get('min', ''),
            }),

            'booking_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
        }


class contactform(forms.ModelForm):
    class Meta:
        model = contact
        fields = ['name','email','phone_no','Address'] 
        labels = {
            'name': 'Name',
            'email': 'Email',
            'phone_no': 'Phone_No',
            'Address': 'Address'
        }
        widgets = {
            'name':forms.TextInput(attrs={'placeholder': 'Enter your name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-control'}),
            'Address':forms.Textarea(attrs={'placeholder': 'Enter your Address','class':'form-control'}),
        }

class PatientProfileForm(forms.ModelForm):

    class Meta:
        model = PatientProfile
        fields = ['profile_image']

        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }