from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Medication, MedicationReminder
from .forms import MedicationForm, MedicationReminderForm
# Create your views here.
@login_required
def dashboard_view(request): 
  user = request.user
  medications = Medication.objects.filter(user=user)
  medication_reminders = MedicationReminder.objects.filter(medication__in=medications)
  return render(request, 'core/dashboard.html', {'medications': medications, 'medication_reminders': medication_reminders})
  
def landing_page_view(request):
  return render(request, 'core/landing_page.html')

@login_required
def medications(request):
  if request.method == "POST":
    form1 = MedicationForm(request.POST)
    form2 = MedicationReminderForm(request.POST)
    if form1.is_valid() and form2.is_valid():
      medication = form1.save(commit=False)
      reminder = form2.save(commit=False)

      medication.user = request.user
      medication.save()

      reminder.medication = medication
      reminder.save()

      return redirect('dashboard')
  else:
    form1 = MedicationForm()
    form2 = MedicationReminderForm()
  return render(request, 'core/medications.html', {'form1': form1, 'form2': form2})