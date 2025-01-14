import os
from dotenv import load_dotenv
import requests
from twilio.rest import Client

# --------------- Load the environment variables ---------------
load_dotenv()

# --------------- Set up the Openweather API --------------- 
API_KEY = os.getenv("OWM_API_KEY")
latitude = os.getenv("OWM_LAT")
longitude = os.getenv("OWM_LONG")
endpoint = 'https://api.openweathermap.org/data/2.5/forecast?'
params = {
    'lat': latitude,
    'lon': longitude,
    'appid': API_KEY,
    'units': 'metric',
    'lang': 'es',
    'cnt': 8
}
# Twilio wpp sandbox: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
# note: I believe this sandbox must to be activated every 72 hours

# --------------- Set up the Twilio API --------------- 
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
body="Hoy llueve mi terrón de azúcar, prepárate."
from_wpp="whatsapp:+14155238886" # Note: twilio sandbox number(wpp) is different to twilio phone number(msn) 
to_wpp=os.getenv("TO_WPP")

# --------------- Get the weather data --------------- 
response = requests.get(endpoint, params=params)
response.raise_for_status()
# print(f"Response: {response}")
# print(f"code: {response.status_code}")

data = response.json()
raw_list = data['list']
# print(data)

# --------------- Check if it will rain ---------------
umbrella_required = False
for timestamp in raw_list:
    weather_code = timestamp['weather'][0]['id']
    if int(weather_code) < 701:
        will_rain = True
        break  # Exit the loop since we found a match

# --------------- Send a wpp message if it will rain ---------------    
if will_rain:
    client = Client(account_sid, auth_token)
    msn = client.messages.create( 
        body=body,
        from_=from_wpp,
        to=to_wpp,
        )
    print(msn.status)