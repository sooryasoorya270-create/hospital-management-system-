from django.db import models
from django.conf import settings


# Create your models here.
class dbt(models.Model):
    department_name=models.CharField(max_length=100)
    dbt_dsc=models.TextField()
    def __str__(self):
        return self.department_name

class  doctor(models.Model):
    doctor_name=models.CharField(max_length=100)
    specialization=models.CharField(max_length=100)
    doctor_dsc=models.TextField()
    department_name=models.ForeignKey(dbt,on_delete=models.CASCADE)
    doctor_image=models.ImageField(upload_to='doctor/',null=True,blank=True)

    def __str__(self):
        return self.doctor_name
    

class booking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_bookings',
        null=True,
        blank=True
    )

    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=15)

    doctor_name = models.ForeignKey(
        doctor,
        on_delete=models.CASCADE
    )

    booking_ON = models.DateField()

    # New appointment time field
    booking_time = models.TimeField(default='09:00')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.patient_name} - {self.doctor_name}"


class contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone_no=models.CharField(max_length=15)
    Address=models.TextField()
    def __str__(self):
        return self.name

class Appointment(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    doctor = models.ForeignKey(
        doctor,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.doctor_name}"

class PatientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_profile'
    )

    profile_image = models.ImageField(
        upload_to='patient_profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username 