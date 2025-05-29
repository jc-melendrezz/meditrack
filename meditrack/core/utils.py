import requests 
import logging
from .models import Medication
from django.core.mail import send_mail
from django.conf import settings

def send_reminder(user, reminder):
    url = "https://api.textbee.dev/api/v1/gateway/devices/682e66009f3070afa2617ad8/send-sms"

    headers = {
        "x-api-key": "fae9d2dd-44f7-4685-b6be-01bcd2dbb0a1",
        "Content-Type": "application/json"
    }

    if reminder.medication.quantity_available <= 5:
        message = f"Reminder: It's time to take your medication: {reminder.medication.name} - {reminder.medication.dosage}. Notes: {reminder.medication.notes}. Only { reminder.medication.quantity_available} pharmaceutical medicine. Please restock your medicine."
    else:
        message = f"Reminder: It's time to take your medication: {reminder.medication.name} - {reminder.medication.dosage}. Notes: {reminder.medication.notes}."

    number = user.phone_number

    if number.startswith("0"):
        number = "+63" + number[1:]
    data = {
        "recipients": [number],
        "message": message
    }

    try: 
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        logging.info(f"SMS sent to {user.phone_number}: {response.text}")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to send SMS to {user.phone_number}: {e}")
        return None
    
def send_email(user, reminder):
    subject = 'Medication Reminder'
    
    # Check if the medication details are available
    medication = reminder.medication
    if medication:
        # Create message based on quantity available
        if medication.quantity_available <= 5:
            message = (f"Reminder: It's time to take your medication: {medication.name} - "
                       f"{medication.dosage}.\n\n"
                       f"Only {medication.quantity_available} left. Please restock your medication soon.")
        else:
            message = (f"Reminder: It's time to take your medication: {medication.name} - "
                       f"{medication.dosage}.\n\n"
                       f"Notes: {medication.notes}.\n\n"
                       f"Please take your medication as scheduled.")
        
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        
        send_mail(subject, message, from_email, recipient_list)