from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Medication, MedicationReminder
from django.contrib.auth import update_session_auth_hash
from datetime import timedelta
from django.contrib import messages
from .forms import MedicationForm, MedicationReminderForm, AddReminderForm, ProfileForm, ChangePasswordForm
# Create your views here.

@login_required
def dashboard_view(request): 
  user = request.user
  medications = Medication.objects.filter(user=user)
  medication_reminders = MedicationReminder.objects.filter(medication__in=medications)
  reminders_amount = medication_reminders.count()

  for reminder in medication_reminders: 
      if reminder.interval_unit == 'hours':
          delta = timedelta(hours=reminder.interval_value)
      else:
          delta = timedelta(minutes=reminder.interval_value)
      if reminder.medication.daily_meds_taken == reminder.medication.schedule:
        reminder.next_dose = reminder.reminder_time
      else:
        reminder.next_dose = reminder.last_reminder + delta

  return render(request, 'core/dashboard.html', {'medications': medications, 'medication_reminders': medication_reminders, 'reminders_amount': reminders_amount})
  
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

@login_required
def add_reminder(request):
  if request.method == 'POST':
    form = AddReminderForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('dashboard')
  else:
    form = AddReminderForm()
  return render(request, 'core/add_reminder.html', {'form': form})

@login_required
def manage_medications(request):
    search_query = request.GET.get('search', '')
    medications = Medication.objects.filter(user=request.user)
    
    if search_query:
        medications = medications.filter(name__icontains=search_query)
    
    return render(request, 'core/manage_medications.html', {
        'medications': medications,
        'search_query': search_query,
    })

@login_required
def edit_medication(request, medication_id):
  medication = get_object_or_404(Medication, id=medication_id, user=request.user)

  if request.method == "POST":
    form1 = MedicationForm(request.POST, instance=medication)
    form2 = MedicationReminderForm(request.POST, instance=medication)
    if form1.is_valid() and form2.is_valid():
      medication = form1.save(commit=False)
      reminder = form2.save(commit=False)

      medication.user = request.user
      medication.save()

      reminder.medication = medication
      reminder.save()

      return redirect('dashboard')
  else:
    form1 = MedicationForm(instance=medication)
    form2 = MedicationReminderForm(instance=medication)
  return render(request, 'core/medications.html', {'form1': form1, 'form2': form2})

@login_required
def delete_medication(request, medication_id):
  medication = get_object_or_404(Medication, id=medication_id, user=request.user)
  medication.delete()
  return redirect('manage_medications')

@login_required
def user_account(request):
    user = request.user
    # Handle profile form submission
    if request.method == 'POST':
        if "profile_submit" in request.POST:
            profile_form = ProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('user_account')  # Redirect to the same page after saving
            else:
                print(profile_form.errors) 
        if "password_submit" in request.POST:
              change_password_form = ChangePasswordForm(request.POST)
              if change_password_form.is_valid():
                  current_password = change_password_form.cleaned_data["current_password"]
                  new_password = change_password_form.cleaned_data["new_password"]

                  # Check the current password
                  if not user.check_password(current_password):
                      messages.error(request, "Current password is incorrect.")
                  else:
                      user.set_password(new_password)
                      user.save()
                      update_session_auth_hash(request, user)  # Prevent logout
                      messages.success(request, "Password changed successfully!")
                      return redirect('user_account')  # Redirect to the same page after saving

    else:
        profile_form = ProfileForm(instance=user)
        change_password_form = ChangePasswordForm()
        
    return render(request, 'core/user_account.html')