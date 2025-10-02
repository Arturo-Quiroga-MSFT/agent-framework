# Microsoft Agent Framework - Interactive Jupyter Notebook Demos

This directory contains comprehensive Jupyter Notebook demonstrations of the Microsoft Agent Framework (MAF), showcasing AI agents, workflows, and various agent types through interactive, executable examples.

## 👨‍💻 Author

**Arturo Quiroga**  
Senior Cloud Solutions Architect (Partners)  
Microsoft Americas

## 📚 Available Notebooks

### 1. **Azure AI Foundry Agent Demo** (`azure_ai_foundry_agent_demo.ipynb`)
Comprehensive guide to building agents with Azure AI Foundry (persistent agents service).

**Topics Covered:**
- Basic agent creation with environment variables
- Explicit configuration without environment variables
- Custom function tools for agents
- Hosted code interpreter for Python execution
- Streaming responses for real-time output
- Using existing agents by ID
- Creating and managing persistent agents
- Multiple tools combined (functions + code interpreter)
- Conversation threading and context management

**Prerequisites:**
- Azure AI Foundry project
- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`

### 2. **Azure OpenAI Chat Completion Agent Demo** (`azure_openai_chat_completion_agent_demo.ipynb`)
In-depth exploration of Azure OpenAI Chat Completion agents with emphasis on function tools.

**Topics Covered:**
- Basic agent creation and configuration
- Streaming responses
- Single and multiple function tools
- Decorated functions with `@ai_function`
- Class-based tool organization
- Conversation memory with threads
- Streaming combined with function calls
- Error handling best practices
- Advanced client configuration

**Prerequisites:**
- Azure OpenAI resource with deployed model
- Environment variables: `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`

### 3. **Concurrent Workflow Demo** (`concurrent_workflow_demo.ipynb`)
Advanced demonstration of multi-agent concurrent workflows with visualization.

**Topics Covered:**
- Fan-out/fan-in workflow patterns
- Parallel agent execution
- Workflow dispatcher and aggregator patterns
- Mermaid diagram visualization (inline rendering)
- GraphViz diagram generation
- SVG export for workflow diagrams
- Real-world multi-expert collaboration scenarios

**Features:**
- Interactive Mermaid diagram rendering (3 methods provided)
- Workflow event tracking and monitoring
- Expert agents working in parallel (researcher, marketer, legal)

### 4. **Workflow Tutorial** (`workflow_tutorial.ipynb`)
Foundational tutorial for building workflows in the Microsoft Agent Framework.

**Topics Covered:**
- Workflow basics and concepts
- Sequential and parallel execution patterns
- Agent coordination and handoffs
- State management in workflows

## 🚀 Getting Started

### Prerequisites

1. **Python Environment**
   ```bash
   # Python 3.10 or higher
   python --version
   ```

2. **Install Agent Framework**
   ```bash
   # Base installation
   pip install agent-framework
   
   # With Azure AI support
   pip install agent-framework[azure-ai]
   
   # Or install everything
   pip install agent-framework[all]
   ```

3. **Install Jupyter**
   ```bash
   pip install jupyter notebook
   # Or use JupyterLab
   pip install jupyterlab
   ```

4. **Azure Authentication**
   ```bash
   # For Azure-based notebooks
   az login
   ```

### Environment Setup

Create a `.env` file in the `python` directory (5 levels up from Notebooks):

```bash
# For Azure OpenAI Chat Completion
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-10-21  # Optional

# For Azure AI Foundry
AZURE_AI_PROJECT_ENDPOINT=https://<your-project>.services.ai.azure.com/api/projects/<project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o-mini

# Optional: For direct API key authentication (if not using Azure CLI)
AZURE_OPENAI_API_KEY=<your-api-key>
```

### Running the Notebooks

1. **Launch Jupyter**
   ```bash
   # From this directory
   jupyter notebook
   # Or with JupyterLab
   jupyter lab
   ```

2. **Open a Notebook**
   - Click on any `.ipynb` file
   - Run cells sequentially with `Shift+Enter`
   - Or use "Run All" from the menu

3. **Using VS Code**
   - Open the notebook in VS Code
   - VS Code will prompt to install Jupyter extension if needed
   - Select your Python kernel
   - Run cells interactively

## 🎯 Key Features Demonstrated

### Agent Types
- **Azure AI Foundry Agents** - Persistent, service-backed agents
- **Azure OpenAI Chat Completion Agents** - Lightweight, flexible agents
- **Custom Agents** - Build your own with full control

### Function Tools
- Simple function decorators
- Multiple tools per agent
- Class-based tool organization
- Custom parameters and descriptions
- Tool sharing between agents

### Workflows
- Sequential execution
- Concurrent/parallel execution
- Fan-out/fan-in patterns
- Agent handoffs and coordination
- State management

### Advanced Features
- Streaming responses for real-time output
- Conversation threading and memory
- Code interpreter integration
- Mermaid diagram visualization
- GraphViz diagram generation
- Event tracking and monitoring

## 📊 Visualization Features

The **Concurrent Workflow Demo** includes three methods for rendering Mermaid diagrams directly in notebooks:

1. **Mermaid.js via CDN** - JavaScript-based rendering
2. **Mermaid.ink API** - Image-based rendering (most reliable)
3. **Optional Packages** - Native Jupyter extensions

All methods are provided with working code examples!

## 🔗 Related Resources

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Python Samples Directory](../../)

## 💡 Tips for Learning

1. **Start with Azure OpenAI Chat Completion** - Easiest to set up
2. **Progress to Azure AI Foundry** - More advanced persistence features
3. **Explore Workflows** - Multi-agent orchestration patterns
4. **Experiment with Tools** - Modify function tools to see how agents adapt

## 🐛 Troubleshooting

### Import Errors
```bash
# Ensure packages are installed
pip install agent-framework[azure-ai]

# Verify installation
python -c "import agent_framework; print(agent_framework.__version__)"
```

### Environment Variable Issues
```bash
# Check if .env file is in the correct location
# Should be in: python/.env (5 directories up from Notebooks)

# Verify variables are loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('AZURE_OPENAI_ENDPOINT'))"
```

### Authentication Errors
```bash
# Re-authenticate with Azure
az login

# Check your subscription
az account show
```

### Kernel Issues in Jupyter
- Ensure your virtual environment is selected as the kernel
- Restart the kernel: `Kernel > Restart Kernel`
- Clear outputs and rerun: `Kernel > Restart & Clear Output`

## 📝 Contributing

These notebooks are part of the Microsoft Agent Framework repository. Contributions, improvements, and additional examples are welcome!

### Adding New Notebooks
1. Follow the existing structure and naming conventions
2. Include comprehensive markdown documentation
3. Add executable code examples with clear outputs
4. Update this README with notebook description

## 📄 License

See the main repository LICENSE file for details.

## 🤝 Support

For questions, issues, or feedback:
- Open an issue in the main repository
- Refer to the [SUPPORT.md](../../../../SUPPORT.md) file
- Check the [FAQ](../../../../docs/FAQS.md)

---

**Last Updated:** October 2025  
**Agent Framework Version:** 0.1.0b1  
**Python Version:** 3.10+
