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
    
    api_key = os.environ["OPENWEATHER_API_KEY"]
    city = "Kollam"

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={api_key}&units=metric"
    )

    response = requests.get(url)
    data = response.json()
    print(data)
    print(url)
    if "list" not in data:
        print("Weather API error:", data)
        return None, False
    temp = data["list"][0]["main"]["temp"]

    rain_expected = False

    for forecast in data["list"][:8]:
        if "rain" in forecast:
            rain_expected = True
            break

    return temp, rain_expected
def create_alert():
    temp, rain_expected = get_weather()

    if temp > 35:
        return f"🔥 Heat Alert! Current temperature is {temp}°C"

    if rain_expected:
        return "🌧️ Rain Alert! Rain is forecast in the coming hours."
    if temp is None:
        return "⚠️ Weather data unavailable. Please check the API or your internet connection."

    return None

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
alert = create_alert()

if alert:
    send_email(alert)
    print("Alert sent")
else:
    print("No alert needed")
with open(filename, "w") as file:
    file.write(alert)
