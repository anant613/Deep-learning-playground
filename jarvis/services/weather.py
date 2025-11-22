import requests
from config.settings import settings

class WeatherService:
    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = settings.WEATHER_BASE_URL
    
    def get_weather(self, city="London"):
        """Get current weather for a city"""
        try:
            if not self.api_key:
                return "I need a weather API key to provide weather updates. Please add your OpenWeatherMap API key."
            
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract weather info
            temp = round(data['main']['temp'])
            feels_like = round(data['main']['feels_like'])
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            
            return f"The weather in {city} is {description} with a temperature of {temp}°C, feels like {feels_like}°C. Humidity is {humidity}%."
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Weather API error: {e}")
            return f"Sorry, I couldn't get the weather information for {city} right now."
        except KeyError as e:
            print(f"❌ Weather data parsing error: {e}")
            return f"Sorry, I couldn't find weather information for {city}. Please check the city name."
        except Exception as e:
            print(f"❌ Weather service error: {e}")
            return "There was an error getting the weather information."