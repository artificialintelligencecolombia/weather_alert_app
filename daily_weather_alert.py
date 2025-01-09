import requests
from twilio.rest import Client

# --------------- Set up the Openweather API --------------- 
API_KEY = 'a31826faf7d1eaa3b356be645473c542'
latitude = 6.281630
longitude = -75.332850
endpoint = 'https://api.openweathermap.org/data/2.5/forecast?'
params = {
    'lat': latitude,
    'lon': longitude,
    'appid': API_KEY,
    'units': 'metric',
    'lang': 'es',
    'cnt': 8
}

# --------------- Set up the Twilio API --------------- 
account_sid = "ACbb7d83b1756210b75dc987a5776c5b95"
auth_token = "5461081b3c0b6a87289a336a26a43265"
body="Hoy llueve papi, preparese."
from_wpp="whatsapp:+14155238886"
to_wpp="whatsapp:+573045201870"

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