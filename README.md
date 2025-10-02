# Microsoft Agent Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![.NET](https://img.shields.io/badge/.NET-8.0+-purple.svg)](https://dotnet.microsoft.com/)

Build, orchestrate, and deploy AI agents and multi-agent systems with the Microsoft Agent Framework - a flexible, production-ready framework for creating intelligent agents with Python and .NET.

## 🌟 What's New

### 📓 Interactive Jupyter Notebook Demos
Comprehensive interactive demonstrations showcasing the Microsoft Agent Framework through executable Jupyter notebooks:

- **Azure AI Foundry Agent Demo** - Persistent agents with code interpreter and function tools
- **Azure OpenAI Chat Completion Agent Demo** - Lightweight agents with advanced function calling
- **Concurrent Workflow Demo** - Multi-agent orchestration with real-time visualization
- **Workflow Tutorial** - Foundational concepts and patterns

**Created by:** Arturo Quiroga, Senior Cloud Solutions Architect (Partners), Microsoft Americas

👉 **[Get Started with Notebooks](python/samples/getting_started/agents/Notebooks/)**

## ✨ Key Features

- **🤖 Flexible Agent Framework** - Build, orchestrate, and deploy AI agents and multi-agent systems
- **🔄 Multi-Agent Orchestration** - Group chat, sequential, concurrent, and handoff patterns
- **🔌 Plugin Ecosystem** - Extend with native functions, OpenAPI, Model Context Protocol (MCP), and more
- **🧠 LLM Support** - OpenAI, Azure OpenAI, Azure AI Foundry, Anthropic, and more
- **⚡ Runtime Support** - In-process and distributed agent execution
- **🎭 Multimodal** - Text, vision, audio, and function calling
- **🌍 Cross-Platform** - Python and .NET implementations with feature parity
- **📊 Observability** - Built-in OpenTelemetry instrumentation and tracing
- **🔐 Enterprise-Ready** - Azure integration, security, and compliance features

## 🚀 Quick Start

### Python

```bash
# Install base framework
pip install agent-framework

# Or install with Azure AI support
pip install agent-framework[azure-ai]

# Or install everything
pip install agent-framework[all]
```

**Create your first agent in 3 lines:**

```python
import asyncio
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

async def main():
    agent = ChatAgent(
        chat_client=OpenAIChatClient(),
        instructions="You are a helpful assistant."
    )
    result = await agent.run("What are the three laws of robotics?")
    print(result.text)

asyncio.run(main())
```

### .NET

```bash
dotnet add package Microsoft.Agents.AI --prerelease
```

**Create your first agent:**

```csharp
using Microsoft.Agents.AI;
using OpenAI;

var client = new OpenAIClient(Environment.GetEnvironmentVariable("OPENAI_API_KEY"));
var chatClient = client.GetChatClient("gpt-4o-mini");

var agent = chatClient.CreateAIAgent(
    instructions: "You are a helpful assistant.",
    name: "MyAgent"
);

var result = await agent.RunAsync("What are the three laws of robotics?");
Console.WriteLine(result);
```

## 📚 Documentation & Learning Paths

### For Beginners
1. 🎓 **[Interactive Jupyter Notebooks](python/samples/getting_started/agents/Notebooks/)** - Best place to start!
2. 📖 **[Python Getting Started Guide](python/README.md)** - Step-by-step introduction
3. 📖 **[.NET Getting Started Guide](dotnet/README.md)** - .NET specific quickstart

### Core Concepts
- **[Agent Types](python/samples/getting_started/agents/)** - Azure AI, Azure OpenAI, OpenAI, Anthropic, Custom
- **[Function Tools](python/samples/getting_started/agents/azure_openai/)** - Extend agents with custom functions
- **[Workflows](python/samples/getting_started/workflow/)** - Orchestrate multi-agent systems
- **[Model Context Protocol (MCP)](python/samples/getting_started/agents/azure_ai/)** - Integrate MCP servers

### Advanced Topics
- **[Multi-Agent Patterns](python/samples/getting_started/workflow/)** - Sequential, concurrent, handoffs
- **[Observability & Tracing](python/samples/getting_started/observability/)** - OpenTelemetry integration
- **[Custom Agents](python/samples/getting_started/agents/custom/)** - Build your own agent implementations
- **[Workflow Samples](workflow-samples/)** - Real-world workflow examples

## 🏗️ Architecture

The Microsoft Agent Framework provides a unified programming model across Python and .NET:

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Application                          │
├─────────────────────────────────────────────────────────────┤
│              Microsoft Agent Framework                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │   Agents    │  │  Workflows   │  │  Observability  │   │
│  │  - Chat     │  │  - Sequential│  │  - OpenTelemetry│   │
│  │  - Custom   │  │  - Concurrent│  │  - Tracing      │   │
│  │  - Multi    │  │  - Handoffs  │  │  - Metrics      │   │
│  └─────────────┘  └──────────────┘  └─────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Chat Clients & Tools                    │   │
│  │  - Function Tools  - Code Interpreter  - MCP  - API │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                    LLM Providers                             │
│  Azure AI │ Azure OpenAI │ OpenAI │ Anthropic │ Custom     │
└─────────────────────────────────────────────────────────────┘
```

## 📂 Repository Structure

```
agent-framework/
├── python/                          # Python implementation
│   ├── packages/                    # Python packages
│   │   ├── main/                   # Core agent-framework package
│   │   ├── azure-ai/               # Azure AI integration
│   │   ├── copilotstudio/          # Copilot Studio integration
│   │   └── ...                     # Additional integrations
│   └── samples/                     # Python examples
│       └── getting_started/
│           ├── agents/
│           │   └── Notebooks/      # 🌟 NEW! Interactive demos
│           ├── workflow/           # Workflow examples
│           └── observability/      # Tracing examples
├── dotnet/                          # .NET implementation
│   ├── src/                        # .NET source code
│   └── samples/                    # .NET examples
├── workflow-samples/                # YAML workflow definitions
├── docs/                           # Documentation & ADRs
└── presentations/                   # Presentation materials
```

## 🎯 Use Cases

### Single Agent Scenarios
- **Conversational AI** - Chatbots, virtual assistants, customer support
- **Code Generation** - Development assistants, code review bots
- **Data Analysis** - Query natural language, generate insights
- **Content Creation** - Writing, summarization, translation

### Multi-Agent Scenarios
- **Research & Analysis** - Parallel research with aggregation
- **Workflow Automation** - Sequential task execution with handoffs
- **Expert Systems** - Specialized agents for different domains
- **Quality Assurance** - Multi-stage review and validation

## 🔧 Supported Platforms & Integrations

### LLM Providers
- ✅ Azure OpenAI Service
- ✅ Azure AI Foundry (Persistent Agents)
- ✅ OpenAI
- ✅ Anthropic
- ✅ Custom providers via chat client interface

### Tools & Extensions
- ✅ Function Tools (custom Python/C# functions)
- ✅ Code Interpreter (Python execution)
- ✅ File Search & RAG
- ✅ Web Search (Bing)
- ✅ Model Context Protocol (MCP)
- ✅ OpenAPI/REST APIs

### Platforms
- **Python:** 3.10, 3.11, 3.12, 3.13
- **.NET:** 8.0+
- **OS:** Windows, macOS, Linux

## 🤝 Contributing

We welcome contributions! Please see:
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Documentation Contributing Guide](docs/CONTRIBUTING_TO_DOCS.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation:** [Microsoft Learn - Agent Framework](https://learn.microsoft.com/en-us/agent-framework/)
- **Issues:** [GitHub Issues](https://github.com/microsoft/agent-framework/issues)
- **Discussions:** [GitHub Discussions](https://github.com/microsoft/agent-framework/discussions)
- **Support:** See [SUPPORT.md](SUPPORT.md)
- **FAQ:** See [docs/FAQS.md](docs/FAQS.md)

## 🌟 Featured Examples

### Interactive Notebooks (Python)
- [Azure AI Foundry Agent](python/samples/getting_started/agents/Notebooks/azure_ai_foundry_agent_demo.ipynb) - 9 complete examples
- [Azure OpenAI Chat Completion](python/samples/getting_started/agents/Notebooks/azure_openai_chat_completion_agent_demo.ipynb) - 11 comprehensive examples
- [Concurrent Workflows](python/samples/getting_started/agents/Notebooks/concurrent_workflow_demo.ipynb) - Multi-agent orchestration with visualization

### Code Samples (Python)
- [Basic Agent Creation](python/samples/getting_started/agents/azure_ai/azure_ai_basic.py)
- [Function Tools](python/samples/getting_started/agents/azure_openai/azure_openai_with_function_tools.py)
- [Code Interpreter](python/samples/getting_started/agents/azure_ai/azure_ai_with_code_interpreter.py)
- [MCP Integration](python/samples/getting_started/agents/azure_ai/azure_ai_with_hosted_mcp.py)
- [Multi-Agent Workflows](python/samples/getting_started/workflow/)

### Code Samples (.NET)
- [Getting Started](dotnet/samples/GettingStarted/)
- [Agent-to-Agent Communication](dotnet/samples/A2AClientServer/)
- [Web Chat Integration](dotnet/samples/AgentWebChat/)

## 📊 Project Status

This project is under active development. We release regular updates with new features, improvements, and bug fixes.

- **Current Version:** 0.1.0-beta1
- **Latest Release:** Check [Releases](https://github.com/microsoft/agent-framework/releases)
- **Roadmap:** See [GitHub Projects](https://github.com/microsoft/agent-framework/projects)

## 🙏 Acknowledgments

Special thanks to all contributors and the open-source community for making this project possible.

**Interactive Notebook Demos:** Created by Arturo Quiroga, Senior Cloud Solutions Architect (Partners), Microsoft Americas

---

**© Microsoft Corporation. All rights reserved.**

For more information about Microsoft's AI initiatives, visit [Microsoft AI](https://www.microsoft.com/ai).
