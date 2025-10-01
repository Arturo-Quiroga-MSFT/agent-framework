# Agent Framework Architecture Deep Dive

> Expanded narrative for Slide #5 (Architecture Overview) with runnable code examples and file references. This document is intended for engineers and solution architects who need to understand the core building blocks, how they compose, and how to extend them safely.

## 1. Conceptual Map

```
User / System Input ─▶ Workflow (graph) ─▶ Executors / AgentExecutors ─▶ Chat Client (LLM) ─▶ Model
                                      │                              ▲
                                      │                              │
                                      ├── Tools / Plugins ◀──────────┘
                                      │
                                      ├── Event Stream (run_stream) ─▶ Observability / UI (DevUI, Tracing, Viz)
                                      │
                                      └── Output Emission (WorkflowOutputEvent)
```

Core components:
- **Chat Agents**: Stateful, tool-aware conversational reasoning units.
- **Agent Executors**: Adapters that let agents participate as workflow nodes.
- **Workflow Builder / Graph**: Fluent API for composing execution DAGs (linear, branching, parallel, looping, conditional, fan-in/out, sub‑workflows).
- **Chat Clients**: Provider abstractions (Azure OpenAI, Azure AI Foundry, OpenAI) for model invocation + agent creation.
- **Tools & Plugins**: Structured, schema-emitting Python callables (sync/async) surfaced to the model for tool calling.
- **Runtime**: In‑process orchestrator providing streaming, context propagation, event instrumentation, type‑aware message passing.

## 2. Chat Agents
Represents the core reasoning loop. A `ChatAgent` owns:
- Instructions / system persona.
- Message history management (user ↔ assistant turns, tool call traces).
- Tool registry (extracted from annotated Python functions or plugin descriptors).
- Streaming & middleware hooks.

### Key Responsibilities
- Normalize inputs into `ChatMessage` objects.
- Decide when to call tools vs respond directly.
- Aggregate multi‑chunk streaming responses.

### Minimal Example
```python
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient  # or agent_framework.azure import AzureOpenAIChatClient

client = OpenAIChatClient(api_key="...")
agent = ChatAgent(
    chat_client=client,
    instructions=(
        "You are a concise assistant. When given a topic, respond with a tight 2-sentence summary."
    ),
    tools=[],  # add later
)

result = await agent.run("Explain vector embeddings")
print(result.text)
```

### With a Tool
```python
from typing import Annotated
from pydantic import Field

async def get_weather(
    location: Annotated[str, Field(description="City name like 'Seattle' or 'London,UK'")]
) -> str:
    return f"Weather for {location}: (placeholder)"  # Replace with real implementation

agent_with_tool = ChatAgent(
    chat_client=client,
    instructions="Use tools when asked about weather.",
    tools=[get_weather],
)

response = await agent_with_tool.run("What's the weather in Seattle?")
print(response.text)
```

## 3. Tools & Plugins
Tools are introspected for signature + metadata to build a schema the model can invoke.
- Uses `typing.Annotated` + `pydantic.Field` (or string literal) for rich parameter descriptions.
- Supports async & sync functions.
- Automatic argument validation before execution.

### Real Example (Weather Tool)
_File: `python/samples/getting_started/agents/azure_ai_real_weather/weather_utils.py`_
```python
async def get_real_weather(
    location: Annotated[
        str, Field(description="The city name to get weather for (e.g., 'Seattle', 'London', 'Tokyo')")
    ],
) -> str:
    # Makes authenticated HTTP request to OpenWeatherMap, returns formatted multi-line string.
    ...  # See full implementation in repository
```

### Design Notes
- Returning a structured object (Pydantic model) is supported and recommended for downstream automation.
- Tools are pure functions from (validated inputs) → (text / structured response).
- Declarative metadata drives automatic OpenAI / Azure tool schema formatting.

## 4. Chat Clients
Abstractions for model backends that provide:
- Chat completion API surface.
- Agent factory helpers (`create_agent(...)`).
- Model / endpoint configuration & credential handling.

### Azure Example
```python
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

chat_client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),  # reuses az login
    # optionally: endpoint="https://my-resource.openai.azure.com", deployment_name="gpt-4o-mini"
)

agent = chat_client.create_agent(
    instructions="You are a fact-focused summarizer.",
    tools=[],
)
```

## 5. Agent Executors
Bridges a `ChatAgent` into the workflow engine as a node. Adds:
- Standardized request/response dataclasses (`AgentExecutorRequest`, `AgentExecutorResponse`).
- Streaming integration with workflow event bus.
- Uniform error + cancellation handling.

### Example (Fan-Out Domains)
_File: `python/samples/getting_started/workflow/parallelism/fan_out_fan_in_edges.py`_
```python
researcher = AgentExecutor(
    chat_client.create_agent(instructions="Research perspective."),
    id="researcher",
)
marketer = AgentExecutor(
    chat_client.create_agent(instructions="Marketing perspective."),
    id="marketer",
)
legal = AgentExecutor(
    chat_client.create_agent(instructions="Legal/compliance perspective."),
    id="legal",
)
```

## 6. Workflow Builder & Graph
Provides a fluent API to declare topology then build an immutable executable workflow.

### Common Patterns Supported
- Sequential chains: `.add_edge(a, b)`
- Parallel fan-out: `.add_fan_out_edges(dispatcher, [a, b, c])`
- Fan-in aggregation: `.add_fan_in_edges([a, b, c], aggregator)`
- Conditional routing: edge conditions / switch constructs
- Looping constructs & checkpointing
- Sub-workflows as composite executors

### Example (Fan-Out / Fan-In)
```python
workflow = (
    WorkflowBuilder()
    .set_start_executor(dispatcher)
    .add_fan_out_edges(dispatcher, [researcher, marketer, legal])
    .add_fan_in_edges([researcher, marketer, legal], aggregator)
    .build()
)
```

### Custom Executor (Dispatcher Extract)
```python
class DispatchToExperts(Executor):
    def __init__(self, expert_ids: list[str]):
        super().__init__(id="dispatch_to_experts")
        self._expert_ids = expert_ids

    @handler
    async def dispatch(self, prompt: str, ctx: WorkflowContext[AgentExecutorRequest]):
        initial = ChatMessage(Role.USER, text=prompt)
        for expert_id in self._expert_ids:
            await ctx.send_message(
                AgentExecutorRequest(messages=[initial], should_respond=True),
                target_id=expert_id,
            )
```

## 7. Runtime & Streaming
The runtime executes the compiled graph:
- Maintains per-run `WorkflowContext` (message bus, cancellation tokens, state containers).
- Emits structured events (`AgentRunEvent`, `WorkflowOutputEvent`, tool invocation events, etc.).
- Supports async streaming via `run_stream()` for incremental progress consumption.

### Streaming Consumption
```python
async for event in workflow.run_stream("Launch plan for budget e-bike"):
    if isinstance(event, AgentRunEvent):
        print("Agent step:", event.executor_id, event.status)
    elif isinstance(event, WorkflowOutputEvent):
        print("Final Output:\n", event.data)
```

### Visualization Hook
```python
from agent_framework import WorkflowViz
viz = WorkflowViz(workflow)
print(viz.to_mermaid())
# Optionally export SVG (requires viz extras & GraphViz installed): viz.export_svg("workflow.svg")
```

## 8. Cross-Cutting Concerns
| Concern | Mechanism |
|---------|-----------|
| Environment / Secrets | `.env` + `dotenv` loading (scripts) / Azure Identity (managed creds) |
| Observability | Event stream, tracing (OTel instrumentation), structured events |
| Extensibility | Custom Executors, additional tool functions, middleware wrappers |
| Error Handling | Structured error events, status propagation, guarded tool execution |
| Security | Principle of least privilege for credentials; tool input validation via Pydantic |
| Determinism Controls | Model parameters in Chat Client (temperature, top_p, etc.) |
| State Management | Shared state objects / checkpointing samples |

## 9. End-to-End Mini Example
```python
# 1. Define a tool
async def get_weather(city: Annotated[str, Field(description="City name")]):
    return f"Weather for {city}: Sunny (demo)"

# 2. Create client & agent
chat_client = AzureOpenAIChatClient(credential=AzureCliCredential())
agent = chat_client.create_agent(
    instructions="Answer user questions; call tools when needed.",
    tools=[get_weather],
)

# 3. Wrap in executor and simple workflow
executor = AgentExecutor(agent, id="weather")
workflow = WorkflowBuilder().set_start_executor(executor).build()

# 4. Stream run
async for ev in workflow.run_stream("What's the weather in Berlin?"):
    if isinstance(ev, WorkflowOutputEvent):
        print(ev.data)
```

## 10. Extension Points & Roadmap Placeholders
| Area | Today | Future Direction |
|------|-------|------------------|
| Deployment | In-process Python | Multi-host / distributed runtime, queue-backed execution |
| Scheduling | Manual invocation | Cron / event-driven triggers |
| State Persistence | Sample checkpoint patterns | Pluggable durable stores (Redis, Cosmos DB) |
| Policy & Guardrails | Tool input validation | Rich policy engine (rate limits, content filters) |
| Multi-Language | Python + early .NET | Full parity & language-agnostic protocol |

## 11. Best Practices Summary
- Keep tool responses structured when they will feed automation (prefer models over free text).
- Use fan-out only when parallelism meaningfully reduces latency versus serial prompts.
- Introduce aggregation nodes that perform semantic reduction, not just concatenation.
- Guard external calls (network / APIs) with timeouts and explicit error messages.
- Stream results in user-facing UX; buffer only when atomic output is required.

## 12. File Reference Index
| Component | Representative File | Purpose |
|-----------|---------------------|---------|
| Weather Tool | `python/samples/getting_started/agents/azure_ai_real_weather/weather_utils.py` | Real external API tool |
| Fan-Out/Fan-In Workflow | `python/samples/getting_started/workflow/parallelism/fan_out_fan_in_edges.py` | Parallel pattern |
| Visualization | `python/samples/getting_started/workflow/visualization/concurrent_with_visualization.py` | Graph rendering |
| Tutorial Notebook | `python/samples/getting_started/workflow/_start-here/workflow_tutorial.ipynb` | Stepwise learning |
| DevUI Weather Agent | `python/packages/devui/samples/weather_agent_azure/weather_agent_demo.ipynb` | Interactive agent demo |

## 13. Glossary
| Term | Definition |
|------|------------|
| Agent | Reasoning entity with instructions + optional tools. |
| Executor | Executable unit in workflow graph (can be custom or an AgentExecutor). |
| AgentExecutor | Adapter that lets an agent run as an executor node. |
| Tool | Callable exposed to the model for grounded actions. |
| Workflow | Compiled directed graph of executors and edges. |
| Event Stream | Async sequence of structured runtime events. |

---
Contributions & improvements welcome. See `CONTRIBUTING.md`.
