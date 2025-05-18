from django import forms
from .models import Medication, MedicationReminder

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'schedule', 'start_date', 'end_date', 'notes', 'quantity_available']
        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date'}),
            'end_date': forms.DateInput(attrs={'type':'date'})
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise self.add_error('end_date', "End date can't be before start_date")

class MedicationReminderForm(forms.ModelForm):
    reminder_time = forms.TimeField()
    reminder_message = forms.CharField(max_length=200)

    class Meta:
        model = MedicationReminder
        fields = ['reminder_time', 'reminder_message']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

        

