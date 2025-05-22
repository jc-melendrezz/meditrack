import requests 
import logging
def send_reminder(user, reminder):
    url = "https://api.textbee.dev/api/v1/gateway/devices/682e66009f3070afa2617ad8/send-sms"

    headers = {
        "x-api-key": "fae9d2dd-44f7-4685-b6be-01bcd2dbb0a1",
        "Content-Type": "application/json"
    }

    message = f"Reminder: It's time to take your medication: {reminder.medication.name} - {reminder.medication.dosage}."

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