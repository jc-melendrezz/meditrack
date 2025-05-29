from django.core.management.base import BaseCommand
from core.models import MedicationReminder, Medication
from django.utils import timezone
import logging
from core.utils import send_reminder
from datetime import timedelta, time
logging.basicConfig(filename='check_reminders.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Command(BaseCommand):
    help = 'Sends medication reminders starting at a specific time and at fixed intervals, stopping at schedule limit.'

    def handle(self, *args, **kwargs):
        now = timezone.localtime()
        current_time = now.time()

        # Reset daily_meds_taken at midnight
        if time(0, 0) <= current_time < time(0, 1):
            medications = Medication.objects.all()
            for med in medications:
                med.daily_meds_taken = 0
                med.save()
            self.stdout.write("✅ Reset daily_meds_taken for all medications.")

        reminders = MedicationReminder.objects.select_related('medication', 'medication__user')

        for med_reminder in reminders:
            medication = med_reminder.medication

            # Stop if daily limit reached
            if medication.daily_meds_taken >= medication.schedule:
                continue

            should_send = False

            # Check if current time is after the configured start time
            if current_time >= med_reminder.reminder_time:
                # If no reminder was ever sent, start now
                if not med_reminder.last_reminder:
                    should_send = True
                else:
                    # Calculate interval
                    interval = (
                        timedelta(hours=med_reminder.interval_value)
                        if med_reminder.interval_unit == 'hours'
                        else timedelta(minutes=med_reminder.interval_value)
                    )
                    time_diff = now - med_reminder.last_reminder
                    if time_diff >= interval:
                        should_send = True

            if should_send:
                send_reminder(medication.user, med_reminder)
                medication.quantity_available -= 1
                medication.daily_meds_taken += 1
                medication.save()

                med_reminder.last_reminder = now
                med_reminder.save()

                self.stdout.write(
                    f"Sent reminder to {medication.user.username} for {medication.name} "
                    f"({medication.daily_meds_taken}/{medication.schedule})"
                )
