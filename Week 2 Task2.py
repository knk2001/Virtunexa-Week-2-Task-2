import requests
import smtplib
from twilio.rest import Client
from datetime import datetime

# === CONFIGURATION ===
API_KEY = "c55aab85cd50a58314cbbeb9acf06c4e"

# Email settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "komaraneelakantam143@gmail.com"
EMAIL_PASS = "Neela@123"

# Twilio settings
TWILIO_SID = "AC71e3ad4b48e052fcc4a716de23bd6294"
TWILIO_AUTH = "7548a41c7801b9cfa50ed93bf837cc26"
TWILIO_FROM = "+12133440926"
TWILIO_TO = "+919701844183"

# === FUNCTIONS ===

def get_weather(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        raise Exception(f"Error: {data.get('message', 'Unknown error')}")

    weather = {
        "description": data["weather"][0]["description"].title(),
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"]
    }

    return weather

def format_weather_report(city, weather):
    date = datetime.now().strftime("%A, %B %d, %Y")
    return (
        f"Weather in {city} on {date}:\n"
        f"- Condition: {weather['description']}\n"
        f"- Temperature: {weather['temp']}°C (Feels like {weather['feels_like']}°C)\n"
        f"- Humidity: {weather['humidity']}%\n"
        f"- Wind Speed: {weather['wind']} m/s"
    )

def send_email(subject, body, to_addr):
    msg = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, to_addr, msg)

def send_sms(body):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    message = client.messages.create(body=body, from_=TWILIO_FROM, to=TWILIO_TO)
    return message.sid

# === CONSOLE INTERFACE ===

def main():
    print("=== Weather Notifier ===")
    city = input("Enter your city: ").strip()

    try:
        weather = get_weather(city, API_KEY)
        report = format_weather_report(city, weather)
        print("\n" + report + "\n")

        method = input("Send this report via [email/sms/none]? ").lower()
        if method == "email":
            to_email = input("Enter recipient email: ").strip()
            send_email("Your Daily Weather Report", report, to_email)
            print("Email sent.")
        elif method == "sms":
            sid = send_sms(report)
            print(f"SMS sent. SID: {sid}")
        else:
            print("No message sent.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
