# Copyright (c) Microsoft. All rights reserved.

"""
Azure AI Agent example using DETAILED real weather data from OpenWeatherMap API.

This example demonstrates:
- Creating an Azure AI Agent with multiple weather tool options
- Using detailed weather information
- Comparing weather across multiple cities

Prerequisites:
- OPENWEATHERMAP_API_KEY environment variable set in .env file
- Sign up at https://openweathermap.org/api (free tier available)
"""

import asyncio
from pathlib import Path

from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

# Import weather functions
from weather_utils import get_real_weather, get_real_weather_detailed

# Load environment variables from .env file
env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(dotenv_path=env_path)


async def detailed_weather_example() -> None:
    """Example using detailed weather information."""
    print("=== Detailed Weather Information Example ===")

    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential).create_agent(
            name="DetailedWeatherAgent",
            instructions=(
                "You are an expert meteorologist providing detailed weather analysis. "
                "Use the detailed weather function to provide comprehensive information. "
                "Explain weather conditions in a clear, informative way."
            ),
            tools=[get_real_weather, get_real_weather_detailed],
        ) as agent,
    ):
        query = "Give me a detailed weather report for Paris, France"
        print(f"User: {query}")
        result = await agent.run(query)
        print(f"Agent: {result}\n")


async def comparison_example() -> None:
    """Example comparing weather across multiple cities."""
    print("=== Weather Comparison Example ===")

    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential).create_agent(
            name="WeatherComparison",
            instructions=(
                "You are a weather comparison expert. When asked to compare weather, "
                "provide a clear comparison of the conditions in each location. "
                "Highlight differences in temperature, conditions, and other factors."
            ),
            tools=get_real_weather,
        ) as agent,
    ):
        query = "Compare the weather in New York, Los Angeles, and Miami. Which city has the best weather right now?"
        print(f"User: {query}")
        print("Agent: ", end="", flush=True)
        async for chunk in agent.run_stream(query):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print("\n")


async def travel_planning_example() -> None:
    """Example using weather for travel planning."""
    print("=== Travel Planning with Weather Example ===")

    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential).create_agent(
            name="TravelWeatherAdvisor",
            instructions=(
                "You are a travel advisor who uses weather information to help plan trips. "
                "When asked about travel destinations, check the weather and provide advice "
                "on what to pack, best times to visit outdoor attractions, etc."
            ),
            tools=get_real_weather_detailed,
        ) as agent,
    ):
        query = "I'm planning to visit London tomorrow. What should I know about the weather and what should I pack?"
        print(f"User: {query}")
        result = await agent.run(query)
        print(f"Agent: {result}\n")


async def main() -> None:
    print("=== Azure AI Agent with Detailed Real Weather Data ===")
    print("Using OpenWeatherMap API for comprehensive weather information\n")

    await detailed_weather_example()
    await comparison_example()
    await travel_planning_example()


if __name__ == "__main__":
    asyncio.run(main())
