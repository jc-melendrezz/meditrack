from django.core.management.base import BaseCommand
from core.models import MedicationReminder
from django.utils import timezone
import logging
from core.utils import send_reminder

logging.basicConfig(filename='check_reminders.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        now = timezone.localtime()
        current_time = now.time()

        reminder = MedicationReminder.objects.all()
        for med_reminder in reminder:
            send_reminder(med_reminder.medication.user, med_reminder)
            med_reminder.reminder_sent = True
            med_reminder.save()
