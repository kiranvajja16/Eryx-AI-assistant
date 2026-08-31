def get_weather(city:str)->str:

    """
    Get the current weather for a city.
    Args: city:Name of the city
    """

    weather_data = {
        "hyderabad": "32°C, sunny",
        "delhi": "30°C, partly cloudy",
        "mumbai": "29°C, cloudy",
        "bangalore": "24°C, pleasant",
    }

    city_key= city.lower()

    if city_key in weather_data:
        return weather_data[city_key]

    return f"I don't have weather data for {city} yet."