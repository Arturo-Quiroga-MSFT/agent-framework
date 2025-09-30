# Copyright (c) Microsoft. All rights reserved.

"""
Basic Azure AI Agent example using REAL weather data from OpenWeatherMap API.

This example demonstrates:
- Creating an Azure AI Agent
- Using a real external API (OpenWeatherMap) as a tool
- Non-streaming response

Prerequisites:
- OPENWEATHERMAP_API_KEY environment variable set in .env file
- Sign up at https://openweathermap.org/api (free tier available)
"""

import asyncio
from pathlib import Path

from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

# Import the real weather function
from weather_utils import get_real_weather

# Load environment variables from .env file
env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(dotenv_path=env_path)


async def non_streaming_example() -> None:
    """Example of non-streaming response with real weather data."""
    print("=== Non-streaming Response with Real Weather ===")

    # Since no Agent ID is provided, the agent will be automatically created
    # and deleted after getting a response
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential).create_agent(
            name="RealWeatherAgent",
            instructions="You are a helpful weather agent that provides real, accurate weather information using live data.",
            tools=get_real_weather,
        ) as agent,
    ):
        query = "What's the weather like in Seattle?"
        print(f"User: {query}")
        result = await agent.run(query)
        print(f"Agent: {result}\n")


async def streaming_example() -> None:
    """Example of streaming response with real weather data."""
    print("=== Streaming Response with Real Weather ===")

    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential).create_agent(
            name="RealWeatherAgent",
            instructions="You are a helpful weather agent that provides real, accurate weather information using live data.",
            tools=get_real_weather,
        ) as agent,
    ):
        query = "Compare the weather in London and Tokyo right now"
        print(f"User: {query}")
        print("Agent: ", end="", flush=True)
        async for chunk in agent.run_stream(query):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print("\n")


async def main() -> None:
    print("=== Azure AI Agent with Real Weather Data ===")
    print("Using OpenWeatherMap API for live weather information\n")

    await non_streaming_example()
    await streaming_example()


if __name__ == "__main__":
    asyncio.run(main())
