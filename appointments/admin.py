from django.contrib import admin

# Register your models here.

# importing class models form models.py
from .models import Doctor
from .models import Patient
from .models import Availability
from .models import Appointment

# register doctor,patient,availability,appointment models in admin panel
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Availability)
admin.site.register(Appointment)
