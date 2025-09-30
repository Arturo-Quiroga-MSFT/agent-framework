# Copyright (c) Microsoft. All rights reserved.

import asyncio
import importlib.util
import os
from pathlib import Path

from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(dotenv_path=env_path)

# Import weather_utils from the azure_ai_real_weather directory (sibling directory)
weather_utils_path = Path(__file__).resolve().parent.parent / "azure_ai_real_weather" / "weather_utils.py"
spec = importlib.util.spec_from_file_location("weather_utils", weather_utils_path)
weather_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(weather_utils)
get_real_weather = weather_utils.get_real_weather


async def main() -> None:
    print("=== Azure AI Chat Client with Explicit Settings ===")

    # Since no Agent ID is provided, the agent will be automatically created
    # and deleted after getting a response
    # For authentication, run `az login` command in terminal or replace AzureCliCredential with preferred
    # authentication option.
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(
                project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
                model_deployment_name=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
                async_credential=credential,
                agent_name="WeatherAgent",
            ),
            instructions="You are a helpful weather agent that provides real-time weather information.",
            tools=get_real_weather,
        ) as agent,
    ):
        result = await agent.run("What's the weather like in New York?")
        print(f"Result: {result}\n")


if __name__ == "__main__":
    asyncio.run(main())
