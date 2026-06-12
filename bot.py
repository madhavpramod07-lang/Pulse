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
def get_weather():
    CITY = "Kollam"
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

with open(filename, "w") as file:
    file.write(summary)

print(f"Summary saved to {filename}")
