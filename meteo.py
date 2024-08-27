import requests

def get_weather(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    current_weather = data['current_weather']
    return f"Температура: {current_weather['temperature']}°C, Скорость ветра: {current_weather['windspeed']} км/ч"

# Пример использования:
latitude = 59.57  # СПБ
longitude = 30.19  # СПБ
print(get_weather(latitude, longitude))
