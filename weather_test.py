from agents import function_tool
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
# Get API key from environment
api_key = "92e28b14701807c7b3ac236d45e36fb9"
# if not api_key:
#     raise EnvironmentError("API key missing. Set 'OPENWEATHER_API_KEY' in environment variables.")

# -- Weather tool --

# @function_tool
def get_current_weather_forecast(city: str) -> str:
    """
    Fetches weather data for a specified city and date using OpenWeatherMap API.
    The API key is retrieved from the environment variable 'OPENWEATHER_API_KEY'.

    Parameters:
    - city (str): City name (e.g., "London").
    - date (str): Date in 'YYYY-MM-DD' format.

    Returns:
    - dict: Weather data for the specified city and date.
    """
    try:
        # # Convert date to UNIX timestamp
        # target_date = datetime.strptime(date, '%Y-%m-%d')
        # timestamp = int(target_date.timestamp())

        # Get city coordinates
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct"
        geo_params = {'q': city, 'limit': 1, 'appid': api_key}

        geo_response = requests.get(geo_url, params=geo_params)
        geo_response.raise_for_status()  # Raise HTTPError if request failed
        geo_data = geo_response.json()

        if not geo_data:
            raise ValueError(f"City '{city}' not found.")

        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        
        # https://api.openweathermap.org/data/2.5/weather?lat=35.6828387&lon=139.7594549&appid={api_key}&units=imperial
        # 'dt': timestamp
        # Get current weather data. We'll work with that.
        weather_url = f"https://api.openweathermap.org/data/2.5/weather"
        weather_params = {"lat": lat, "lon": lon, "units": "metric", "appid": api_key}

        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()


        return weather_data['main']["temp"]

        #For historical data, one might need subscription and I'm broke.
        #Here's the URL:
        # https://history.openweathermap.org/data/2.5/history/city?lat=35.6828387&lon=139.7594549&type=hour&start=1369728000&end=1369789200&appid={api_key}
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as val_err:
        print(f"Value error: {val_err}")
    except EnvironmentError as env_err:
        print(f"Environment error: {env_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

    return {}
    
# -- Main function --
# Example usage
if __name__ == "__main__":
    city = "Tokyo"
    # date = "2025-03-10"  # must be within the last 5 days

    weather = get_current_weather_forecast(city)

    if weather:
        print(f"Weather data for {city}:")
        print(weather)
    else:
        print("Failed to retrieve weather data.")