from django.db import models
from users.models import CustomUser

class Medication(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  dosage = models.CharField(max_length=100)
  schedule = models.CharField(max_length=255)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  notes = models.TextField(null=True, blank=True)
  
  def __str__(self):
    return f"{self.name} for {self.user.username}"
    
class MedicationReminder(models.Model):
  medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
  reminder_time = models.TimeField()
  repeat_daily = models.BooleanField(default=True)
  reminder_message = models.CharField(max_length=255, null=True, blank=True)
  reminder_sent = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"Reminder at {self.reminder_time} for {self.medication.name}"
