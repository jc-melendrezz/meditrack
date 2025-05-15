from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Medication, MedicationReminder
# Create your views here.
@login_required
def dashboard_view(request): 
  user = request.user
  medications = Medication.objects.filter(user=user)
  medication_reminders = MedicationReminder.objects.filter(medication__in=medications)
  return render(request, 'core/dashboard.html', {'medications': medications, 'medication_reminders': medication_reminders})
  
def landing_page_view(request):
  return render(request, 'core/landing_page.html')
  