# Copyright (c) Microsoft. All rights reserved.

import asyncio
import importlib.util
import os
from pathlib import Path

from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.ai.projects.aio import AIProjectClient
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
    print("=== Azure AI Chat Client with Existing Agent ===")

    # Create the client
    async with (
        AzureCliCredential() as credential,
        AIProjectClient(endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"], credential=credential) as client,
    ):
        # Create an agent that will persist
        created_agent = await client.agents.create_agent(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"], name="WeatherAgent"
        )

        try:
            async with ChatAgent(
                # passing in the client is optional here, so if you take the agent_id from the portal
                # you can use it directly without the two lines above.
                chat_client=AzureAIAgentClient(project_client=client, agent_id=created_agent.id),
                instructions="You are a helpful weather agent that provides real-time weather information.",
                tools=get_real_weather,
            ) as agent:
                result = await agent.run("What's the weather like in Tokyo?")
                print(f"Result: {result}\n")
        finally:
            # Clean up the agent manually
            await client.agents.delete_agent(created_agent.id)


if __name__ == "__main__":
    asyncio.run(main())
