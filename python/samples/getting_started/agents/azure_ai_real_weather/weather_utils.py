# Copyright (c) Microsoft. All rights reserved.

"""
Weather utility module using OpenWeatherMap API.

This module provides a real weather function that can be used as a tool
in AI agent examples.

To use this module:
1. Sign up at https://openweathermap.org/api
2. Get your free API key
3. Add OPENWEATHERMAP_API_KEY to your .env file
"""

import os
from typing import Annotated

import aiohttp
from pydantic import Field


async def get_real_weather(
    location: Annotated[
        str, Field(description="The city name to get weather for (e.g., 'Seattle', 'London', 'Tokyo')")
    ],
) -> str:
    """
    Get the real current weather for a given location using OpenWeatherMap API.

    Args:
        location: City name (e.g., "Seattle", "London,UK", "Tokyo,JP")

    Returns:
        A formatted string with current weather information

    Example:
        >>> weather = await get_real_weather("Seattle")
        >>> print(weather)
        Weather in Seattle:
        - Conditions: clear sky
        - Temperature: 15.5°C (feels like 14.2°C)
        - Humidity: 65%
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        return (
            "Error: OPENWEATHERMAP_API_KEY not set in environment variables.\n"
            "Please sign up at https://openweathermap.org/api and add your API key to .env file."
        )

    base_url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        async with aiohttp.ClientSession() as session:
            params = {"q": location, "appid": api_key, "units": "metric"}  # Use Celsius

            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    weather_desc = data["weather"][0]["description"]
                    temp = data["main"]["temp"]
                    feels_like = data["main"]["feels_like"]
                    humidity = data["main"]["humidity"]
                    wind_speed = data["wind"]["speed"]

                    return (
                        f"Weather in {location}:\n"
                        f"- Conditions: {weather_desc}\n"
                        f"- Temperature: {temp}°C (feels like {feels_like}°C)\n"
                        f"- Humidity: {humidity}%\n"
                        f"- Wind Speed: {wind_speed} m/s"
                    )
                elif response.status == 401:
                    return "Error: Invalid API key. Please check your OPENWEATHERMAP_API_KEY."
                elif response.status == 404:
                    return f"Error: City '{location}' not found. Try using format like 'Seattle' or 'London,UK'."
                else:
                    return f"Error: Could not fetch weather for {location} (Status: {response.status})"
    except aiohttp.ClientError as e:
        return f"Error: Network error occurred: {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error occurred: {str(e)}"


async def get_real_weather_detailed(
    location: Annotated[
        str, Field(description="The city name to get detailed weather for (e.g., 'Seattle', 'London', 'Tokyo')")
    ],
) -> str:
    """
    Get detailed weather information including forecast data.

    Args:
        location: City name (e.g., "Seattle", "London,UK", "Tokyo,JP")

    Returns:
        A formatted string with detailed weather information
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        return (
            "Error: OPENWEATHERMAP_API_KEY not set in environment variables.\n"
            "Please sign up at https://openweathermap.org/api and add your API key to .env file."
        )

    base_url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        async with aiohttp.ClientSession() as session:
            params = {"q": location, "appid": api_key, "units": "metric"}

            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()

                    # Extract detailed weather information
                    weather_desc = data["weather"][0]["description"]
                    temp = data["main"]["temp"]
                    feels_like = data["main"]["feels_like"]
                    temp_min = data["main"]["temp_min"]
                    temp_max = data["main"]["temp_max"]
                    pressure = data["main"]["pressure"]
                    humidity = data["main"]["humidity"]
                    wind_speed = data["wind"]["speed"]
                    wind_deg = data["wind"].get("deg", "N/A")
                    cloudiness = data["clouds"]["all"]
                    visibility = data.get("visibility", "N/A")

                    return (
                        f"Detailed Weather Report for {location}:\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"Conditions: {weather_desc.capitalize()}\n"
                        f"\n"
                        f"Temperature:\n"
                        f"  • Current: {temp}°C (feels like {feels_like}°C)\n"
                        f"  • Min/Max: {temp_min}°C / {temp_max}°C\n"
                        f"\n"
                        f"Atmospheric Conditions:\n"
                        f"  • Pressure: {pressure} hPa\n"
                        f"  • Humidity: {humidity}%\n"
                        f"  • Cloudiness: {cloudiness}%\n"
                        f"  • Visibility: {visibility} meters\n"
                        f"\n"
                        f"Wind:\n"
                        f"  • Speed: {wind_speed} m/s\n"
                        f"  • Direction: {wind_deg}°"
                    )
                elif response.status == 401:
                    return "Error: Invalid API key. Please check your OPENWEATHERMAP_API_KEY."
                elif response.status == 404:
                    return f"Error: City '{location}' not found. Try using format like 'Seattle' or 'London,UK'."
                else:
                    return f"Error: Could not fetch weather for {location} (Status: {response.status})"
    except aiohttp.ClientError as e:
        return f"Error: Network error occurred: {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error occurred: {str(e)}"
