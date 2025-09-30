# Copyright (c) Microsoft. All rights reserved.

import asyncio
import importlib.util
from pathlib import Path

from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

# Load environment variables from .env file
# Look for .env in the python directory
# __file__ is in: python/samples/getting_started/agents/azure_ai/azure_ai_basic.py
# .env is in: python/.env
# So we need to go up 4 levels: azure_ai -> agents -> getting_started -> samples -> python
env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(dotenv_path=env_path)

# Import weather_utils from the azure_ai_real_weather directory (sibling directory)
weather_utils_path = Path(__file__).resolve().parent.parent / "azure_ai_real_weather" / "weather_utils.py"
spec = importlib.util.spec_from_file_location("weather_utils", weather_utils_path)
weather_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(weather_utils)
get_real_weather = weather_utils.get_real_weather


async def non_streaming_example() -> None:
    """Example of non-streaming response (get the complete result at once)."""
    print("=== Non-streaming Response Example ===")

    # Since no Agent ID is provided, the agent will be automatically created
    # and deleted after getting a response
    # For authentication, run `az login` command in terminal or replace AzureCliCredential with preferred
    # authentication option.
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential).create_agent(
            name="WeatherAgent",
            instructions="You are a helpful weather agent that provides real-time weather information.",
            tools=get_real_weather,
        ) as agent,
    ):
        query = "What's the weather like in Toronto?"
        print(f"User: {query}")
        result = await agent.run(query)
        print(f"Agent: {result}\n")


async def streaming_example() -> None:
    """Example of streaming response (get results as they are generated)."""
    print("=== Streaming Response Example ===")

    # Since no Agent ID is provided, the agent will be automatically created
    # and deleted after getting a response
    # For authentication, run `az login` command in terminal or replace AzureCliCredential with preferred
    # authentication option.
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential).create_agent(
            name="WeatherAgent",
            instructions="You are a helpful weather agent that provides real-time weather information.",
            tools=get_real_weather,
        ) as agent,
    ):
        query = "What's the weather like in Mexico City?"
        print(f"User: {query}")
        print("Agent: ", end="", flush=True)
        async for chunk in agent.run_stream(query):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print("\n")


async def main() -> None:
    print("=== Basic Azure AI Chat Client Agent Example with REAL Weather Data ===")

    await non_streaming_example()
    await streaming_example()


if __name__ == "__main__":
    asyncio.run(main())
