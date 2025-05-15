from django.contrib import admin
from .models import Medication, MedicationReminder
# Register your models here.
admin.site.register(Medication)
admin.site.register(MedicationReminder)