# Copyright (c) Microsoft. All rights reserved.

"""
Azure AI Agent example with multi-turn weather conversations using real OpenWeatherMap data.

This example demonstrates:
- Multi-turn conversations with context
- Multiple weather queries in sequence
- Agent maintaining conversation history
- Using both basic and detailed weather functions

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


async def multi_turn_conversation() -> None:
    """Example of a multi-turn conversation about weather."""
    print("=== Multi-Turn Weather Conversation ===\n")

    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential).create_agent(
            name="WeatherChatBot",
            instructions=(
                "You are a friendly weather assistant. Help users learn about weather "
                "in different cities. Remember context from previous queries and provide "
                "helpful comparisons and suggestions. Be conversational and informative."
            ),
            tools=[get_real_weather, get_real_weather_detailed],
        ) as agent,
    ):
        # Query 1: Simple weather check
        query1 = "What's the weather like in Tokyo?"
        print(f"User: {query1}")
        result1 = await agent.run(query1)
        print(f"Agent: {result1}\n")

        # Query 2: Follow-up question using context
        query2 = "How does that compare to Seoul?"
        print(f"User: {query2}")
        result2 = await agent.run(query2)
        print(f"Agent: {result2}\n")

        # Query 3: Detailed information request
        query3 = "Can you give me more detailed information about Tokyo's weather?"
        print(f"User: {query3}")
        result3 = await agent.run(query3)
        print(f"Agent: {result3}\n")


async def vacation_planner() -> None:
    """Example of using weather data for vacation planning."""
    print("=== Vacation Planning Assistant ===\n")

    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential).create_agent(
            name="VacationWeatherPlanner",
            instructions=(
                "You are a vacation planning assistant. Help users choose between "
                "vacation destinations based on current weather. Consider temperature, "
                "conditions, and provide travel advice based on the weather data."
            ),
            tools=[get_real_weather, get_real_weather_detailed],
        ) as agent,
    ):
        query = (
            "I'm trying to decide between Barcelona, Rome, and Athens for a beach vacation. "
            "Which city has the best weather right now? Give me detailed info for your recommendation."
        )
        print(f"User: {query}")
        print("Agent: ", end="", flush=True)
        async for chunk in agent.run_stream(query):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print("\n\n")


async def weather_alert_assistant() -> None:
    """Example of checking weather conditions for activity planning."""
    print("=== Activity Planning Weather Assistant ===\n")

    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential).create_agent(
            name="ActivityWeatherAssistant",
            instructions=(
                "You are an outdoor activity planning assistant. Help users determine "
                "if weather conditions are suitable for their planned activities. "
                "Consider temperature, wind, humidity, and general conditions."
            ),
            tools=get_real_weather_detailed,
        ) as agent,
    ):
        queries = [
            "I want to go hiking in Denver tomorrow. Is the weather suitable?",
            "I'm planning a picnic in San Francisco this afternoon. What should I expect?",
            "Is it good weather for cycling in Amsterdam right now?",
        ]

        for query in queries:
            print(f"User: {query}")
            result = await agent.run(query)
            print(f"Agent: {result}\n")


async def main() -> None:
    print("=" * 70)
    print("Azure AI Agent - Advanced Real Weather Examples")
    print("Using OpenWeatherMap API")
    print("=" * 70)
    print()

    await multi_turn_conversation()
    await vacation_planner()
    await weather_alert_assistant()

    print("=" * 70)
    print("Examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
