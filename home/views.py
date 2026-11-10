from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from . models import dbt,doctor,Appointment,booking as Booking,PatientProfile
from .forms import BookingForm, contactform, PatientProfileForm 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required
from .recommendation import recommend_doctors, find_specializations
from django.contrib import messages
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User



# Create your views here.

def index(request):
    numbers={
        "num1":[1,2,3,4,5,6,7,8,9,10]
        }
    return render(request,"index.html",numbers)
def about(request):
    fruits={
        "fruits_name":["apple","banana","grapes","mango"]
    }
    return render(request,"about.html",fruits)
def doctors(request):
    data=doctor.objects.all()
    doctr_dtls={
        "doctorr":data
    }
    
    return render(request,"doctors.html",doctr_dtls)
def contact(request):
    if request.method=='POST':
        form=contactform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form=contactform()
    return render(request,"contact.html",{'form':form})

def departments(request):
    dict_dbt={
        "department":dbt.objects.all()
    }
    return render(request,"departments.html",dict_dbt)



@login_required
def booking(request):

    # Get selected doctor from URL
    doctor_id = request.GET.get('doctor_id')

    selected_doctor = None

    if doctor_id:
        selected_doctor = get_object_or_404(
            doctor,
            id=doctor_id
        )

    # Automatically get logged-in patient details
    patient_name = (
        request.user.get_full_name()
        or request.user.username
    )

    patient_email = request.user.email

    if request.method == 'POST':

        form = BookingForm(request.POST)

        if form.is_valid():

            appointment = form.save(commit=False)

            # Automatically save logged-in patient
            appointment.user = request.user
            appointment.patient_name = patient_name
            

            appointment.save()

            messages.success(
                request,
                'Your appointment has been booked successfully!'
            )

            return redirect('patient_dashboard')

    else:

        initial_data = {
            'patient_name': patient_name,
            'patient_email': patient_email,
        }

        if selected_doctor:
            initial_data['doctor_name'] = selected_doctor

        form = BookingForm(initial=initial_data)

    # Prevent selecting a past appointment date
    form.fields['booking_ON'].widget.attrs['min'] = (
        timezone.localdate().isoformat()
    )

    return render(
        request,
        'booking.html',
        {'form': form}
    )



class CustomSignupForm(UserCreationForm):

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name'
        })
    )

    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name'
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]



def signup(request):

    if request.method == 'POST':

        form = CustomSignupForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Registration successful! Please login.'
            )

            return redirect('login')

    else:
        form = CustomSignupForm()

    return render(
        request,
        'signup.html',
        {'form': form}
    )

def smart_recommendation(request):
    doctors = []
    symptoms = ""
    searched = False

    if request.method == "POST":
        symptoms = request.POST.get("symptoms", "").strip()
        searched = True

        if symptoms:
            doctors = recommend_doctors(symptoms)

    return render(
        request,
        "smart_recommendation.html",
        {
            "doctors": doctors,
            "symptoms": symptoms,
            "searched": searched,
        },
    )

@login_required
def patient_dashboard(request):

    profile, created = PatientProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST' and 'update_profile_photo' in request.POST:

        profile_form = PatientProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if profile_form.is_valid():
            profile_form.save()

            messages.success(
                request,
                'Profile photo updated successfully!'
            )

            return redirect('patient_dashboard')

        else:
            messages.error(
                request,
                'Please select a valid image.'
            )

    else:
        profile_form = PatientProfileForm(instance=profile)

    appointments = Booking.objects.filter(
        user=request.user
    ).select_related('doctor_name').order_by('-booking_ON')

    total_appointments = appointments.count()

    pending_appointments = appointments.filter(
        status='Pending'
    ).count()

    confirmed_appointments = appointments.filter(
        status='Confirmed'
    ).count()

    cancelled_appointments = appointments.filter(
        status='Cancelled'
    ).count()

    context = {
        'appointments': appointments,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'profile': profile,
        'profile_form': profile_form,
    }

    return render(request, 'patient_dashboard.html', context)

@login_required
def cancel_appointment(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user
    )

    if request.method == 'POST':

        if appointment.status == 'Pending':

            appointment.status = 'Cancelled'
            appointment.save()

            messages.success(
                request,
                'Appointment cancelled successfully!'
            )

        else:
            messages.error(
                request,
                'Only pending appointments can be cancelled.'
            )

    return redirect('patient_dashboard')




