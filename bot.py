import os
import smtplib
from email.message import EmailMessage
import requests
from datetime import date

def get_quote():
    try:
        response = requests.get(
            "https://dummyjson.com/quotes/random",
            timeout=5
        )

        data = response.json()

        return f'"{data["quote"]}" — {data["author"]}'

    except Exception:
        return "Quote unavailable."
CITY = "KOLLAM"
def get_weather():
    
    response = requests.get(
    f"https://wttr.in/{CITY}?format=j1"
)

    data = response.json()

    temp = data["current_condition"][0]["temp_C"]
    condition = data["current_condition"][0]["weatherDesc"][0]["value"]

    return f"{temp}°C, {condition}"

def create_summary():
    today = date.today()

    return f"""
PULSE DAILY SUMMARY
===================

Date: {today}

Weather ({CITY}):
{get_weather()}

Quote of the Day:
{get_quote()}
"""

summary = create_summary()

filename = f"daily_summary_{date.today()}.txt"



print(f"Summary saved to {filename}")
def send_email(summary):
    email_address = os.environ["EMAIL_ADDRESS"]
    email_password = os.environ["EMAIL_APP_PASSWORD"]

    msg = EmailMessage()
    msg["Subject"] = "Pulse Daily Summary"
    msg["From"] = email_address
    msg["To"] = email_address

    msg.set_content(summary)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
summary = create_summary()
send_email(summary)
with open(filename, "w") as file:
    file.write(summary)
