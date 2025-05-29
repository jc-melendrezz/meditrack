from django import forms
from .models import Medication, MedicationReminder
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

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
    UNIT_CHOICES = [
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days')
    ]
    reminder_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'id': 'reminder_time'}),
        label='Set Reminder Time'
    )
    reminder_message = forms.CharField(max_length=200)
    interval_unit = forms.ChoiceField(choices=UNIT_CHOICES)
    interval_value = forms.IntegerField(initial=1)

    class Meta:
        model = MedicationReminder
        fields = ['reminder_time', 'reminder_message', 'interval_unit', 'interval_value']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class AddReminderForm(forms.ModelForm):
    medication = forms.ModelChoiceField(
        queryset=Medication.objects.all(),
        empty_label="Select a medication",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    reminder_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'id': 'reminder_time'}),
        label='Set Reminder Time'
    )
    reminder_message = forms.CharField(max_length=200)

    class Meta:
        model = MedicationReminder
        fields = ['medication','reminder_time', 'reminder_message']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


#user account forms
class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, required=False, label='Phone Number')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")

        return cleaned_data
