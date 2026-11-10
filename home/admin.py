from django.contrib import admin
from . models import booking, dbt, doctor,contact,Appointment

# Register your models here.
admin.site.register(dbt)
admin.site.register(doctor)
admin.site.register(booking)
admin.site.register(contact)
admin.site.register(Appointment)