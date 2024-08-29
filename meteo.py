import requests
from config import WEATHER_TOKEN
def get_weather(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    current_weather = data['current_weather']
    return f"Температура: {current_weather['temperature']}°C, Скорость ветра: {current_weather['windspeed']} км/ч"

def get_weather2(latitude, longitude):
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={WEATHER_TOKEN}&units=metric"
    response = requests.get(url)
    data = response.json()
    #current_weather = data['current_weather']
    return data

# Пример использования:
#latitude = 59.57  # СПБ
#longitude = 30.19  # СПБ
#print(get_weather(latitude, longitude))
#print(get_weather2(latitude, longitude))



