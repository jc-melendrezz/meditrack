from django.core.management.base import BaseCommand
from core.models import MedicationReminder

class Command(BaseCommand):
    help = "Reset all reminder_sent to False."

    def handle(self, *args, **options):
        MedicationReminder.objects.update(reminder_sent=False)
        self.stdout.write("Reminder flags reset.")