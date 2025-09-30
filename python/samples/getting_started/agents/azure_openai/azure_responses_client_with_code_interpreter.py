# Copyright (c) Microsoft. All rights reserved.

import asyncio
from pathlib import Path

from agent_framework import AgentRunResponse, ChatResponseUpdate, HostedCodeInterpreterTool
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from openai.types.responses import (
    CodeInterpreterToolCall,
    ToolCall,
)

# Load environment variables from .env file
env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(dotenv_path=env_path)
