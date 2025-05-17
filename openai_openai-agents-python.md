Prompt: Analyze the openai-agents-python-main repository (partial content) ...

README:
# OpenAI Agents SDK

The OpenAI Agents SDK is a lightweight yet powerful framework for building multi-agent workflows.

<img src="https://cdn.openai.com/API/docs/images/orchestration.png" alt="Image of the Agents Tracing UI" style="max-height: 803px;">

### Core concepts:

1. [**Agents**](https://openai.github.io/openai-agents-python/agents): LLMs configured with instructions, tools, guardrails, and handoffs
2. [**Handoffs**](https://openai.github.io/openai-agents-python/handoffs/): Allow agents to transfer control to other agents for specific tasks
3. [**Guardrails**](https://openai.github.io/openai-agents-python/guardrails/): Configurable safety checks for input and output validation
4. [**Tracing**](https://openai.github.io/openai-agents-python/tracing/): Built-in tracking of agent runs, allowing you to view, debug and optimize your workflows

Explore the [examples](examples) directory to see the SDK in action, and read our [documentation](https://openai.github.io/openai-agents-python/) for more details.

Notably, our SDK [is compatible](https://openai.github.io/openai-agents-python/models/) with any model providers that support the OpenAI Chat Completions API format.

## Get started

1. Set up your Python environment

```
python -m venv env
source env/bin/activate
```

2. Install Agents SDK

```
pip install openai-agents
```

## Hello world example

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.
```

(_If running this, ensure you set the `OPENAI_API_KEY` environment variable_)

(_For Jupyter notebook users, see [hello_world_jupyter.py](examples/basic/hello_world_jupyter.py)_)

## Handoffs example

```python
from agents import Agent, Runner
import asyncio

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
)


async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)
    # ¡Hola! Estoy bien, gracias por preguntar. ¿Y tú, cómo estás?


if __name__ == "__main__":
    asyncio.run(main())
```

## Functions example

```python
import asyncio

from agents import Agent, Runner, function_tool


@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."


agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)


async def main():
    result = await Runner.run(agent, input="What's the weather in Tokyo?")
    print(result.final_output)
    # The weather in Tokyo is sunny.


if __name__ == "__main__":
    asyncio.run(main())
```

## The agent loop

When you call `Runner.run()`, we run a loop until we get a final output.

1. We call the LLM, using the model and settings on the agent, and the message history.
2. The LLM returns a response, which may include tool calls.
3. If the response has a final output (see below for more on this), we return it and end the loop.
4. If the response has a handoff, we set the agent to the new agent and go back to step 1.
5. We process the tool calls (if any) and append the tool responses messages. Then we go to step 1.

There is a `max_turns` parameter that you can use to limit the number of times the loop executes.

### Final output

Final output is the last thing the agent produces in the loop.

1.  If you set an `output_type` on the agent, the final output is when the LLM returns something of that type. We use [structured outputs](https://platform.openai.com/docs/guides/structured-outputs) for this.
2.  If there's no `output_type` (i.e. plain text responses), then the first LLM response without any tool calls or handoffs is considered as the final output.

As a result, the mental model for the agent loop is:

1. If the current agent has an `output_type`, the loop runs until the agent produces structured output matching that type.
2. If the current agent does not have an `output_type`, the loop runs until the current agent produces a message without any tool calls/handoffs.

## Common agent patterns

The Agents SDK is designed to be highly flexible, allowing you to model a wide range of LLM workflows including deterministic flows, iterative loops, and more. See examples in [`examples/agent_patterns`](examples/agent_patterns).

## Tracing

The Agents SDK automatically traces your agent runs, making it easy to track and debug the behavior of your agents. Tracing is extensible by design, supporting custom spans and a wide variety of external destinations, including [Logfire](https://logfire.pydantic.dev/docs/integrations/llms/openai/#openai-agents), [AgentOps](https://docs.agentops.ai/v1/integrations/agentssdk), [Braintrust](https://braintrust.dev/docs/guides/traces/integrations#openai-agents-sdk), [Scorecard](https://docs.scorecard.io/docs/documentation/features/tracing#openai-agents-sdk-integration), and [Keywords AI](https://docs.keywordsai.co/integration/development-frameworks/openai-agent). For more details about how to customize or disable tracing, see [Tracing](http://openai.github.io/openai-agents-python/tracing).

## Development (only needed if you need to edit the SDK/examples)

0. Ensure you have [`uv`](https://docs.astral.sh/uv/) installed.

```bash
uv --version
```

1. Install dependencies

```bash
make sync
```

2. (After making changes) lint/test

```
make tests  # run tests
make mypy   # run typechecker
make lint   # run linter
```

## Acknowledgements

We'd like to acknowledge the excellent work of the open-source community, especially:

-   [Pydantic](https://docs.pydantic.dev/latest/) (data validation) and [PydanticAI](https://ai.pydantic.dev/) (advanced agent framework)
-   [MkDocs](https://github.com/squidfunk/mkdocs-material)
-   [Griffe](https://github.com/mkdocstrings/griffe)
-   [uv](https://github.com/astral-sh/uv) and [ruff](https://github.com/astral-sh/ruff)

We're committed to continuing to build the Agents SDK as an open source framework so others in the community can expand on our approach.


Repository Structure:
./README.md
docs/
docs/guardrails.md
docs/context.md
docs/quickstart.md
docs/handoffs.md
docs/streaming.md
docs/running_agents.md
docs/config.md
docs/results.md
docs/index.md
docs/models.md
docs/tracing.md
docs/agents.md
docs/tools.md
docs/multi_agent.md
docs/ref/
docs/ref/agent.md
docs/ref/lifecycle.md
docs/ref/exceptions.md
docs/ref/agent_output.md
docs/ref/result.md
docs/ref/run_context.md
docs/ref/tool.md
docs/ref/usage.md
docs/ref/items.md
docs/ref/handoffs.md
docs/ref/guardrail.md
docs/ref/stream_events.md
docs/ref/index.md
docs/ref/run.md
docs/ref/model_settings.md
docs/ref/function_schema.md
docs/ref/tracing/
docs/ref/tracing/processor_interface.md
docs/ref/tracing/setup.md
docs/ref/tracing/scope.md
docs/ref/tracing/processors.md
docs/ref/tracing/traces.md
docs/ref/tracing/index.md
docs/ref/tracing/create.md
docs/ref/tracing/spans.md
docs/ref/tracing/util.md
docs/ref/tracing/span_data.md
docs/ref/models/
docs/ref/models/openai_responses.md
docs/ref/models/interface.md
docs/ref/models/openai_chatcompletions.md
docs/ref/extensions/
docs/ref/extensions/handoff_filters.md
docs/ref/extensions/handoff_prompt.md
docs/assets/
docs/assets/logo.svg
docs/assets/images/
docs/assets/images/favicon-platform.svg
docs/assets/images/orchestration.png
docs/stylesheets/
docs/stylesheets/extra.css
examples/
examples/__init__.py
examples/tools/
examples/tools/computer_use.py
examples/tools/file_search.py
examples/tools/web_search.py
examples/customer_service/
examples/customer_service/main.py
examples/model_providers/
examples/model_providers/custom_example_global.py
examples/model_providers/custom_example_agent.py
examples/model_providers/custom_example_provider.py
examples/model_providers/README.md
examples/basic/
examples/basic/lifecycle_example.py
examples/basic/hello_world.py
examples/basic/dynamic_system_prompt.py
examples/basic/stream_text.py
examples/basic/hello_world_jupyter.py
examples/basic/agent_lifecycle_example.py
examples/basic/stream_items.py
examples/research_bot/
examples/research_bot/__init__.py
examples/research_bot/README.md
examples/research_bot/main.py
examples/research_bot/printer.py
examples/research_bot/manager.py
examples/research_bot/agents/
examples/research_bot/agents/planner_agent.py
examples/research_bot/agents/__init__.py
examples/research_bot/agents/search_agent.py
examples/research_bot/agents/writer_agent.py
examples/research_bot/sample_outputs/
examples/research_bot/sample_outputs/vacation.md
examples/research_bot/sample_outputs/product_recs.md
examples/research_bot/sample_outputs/vacation.txt
examples/research_bot/sample_outputs/product_recs.txt
examples/agent_patterns/
examples/agent_patterns/deterministic.py
examples/agent_patterns/input_guardrails.py
examples/agent_patterns/agents_as_tools.py
examples/agent_patterns/output_guardrails.py
examples/agent_patterns/README.md
examples/agent_patterns/parallelization.py
examples/agent_patterns/routing.py
examples/agent_patterns/llm_as_a_judge.py
examples/handoffs/
examples/handoffs/message_filter_streaming.py
examples/handoffs/message_filter.py




--- START OF FILE README.md ---

# OpenAI Agents SDK

The OpenAI Agents SDK is a lightweight yet powerful framework for building multi-agent workflows.

<img src="https://cdn.openai.com/API/docs/images/orchestration.png" alt="Image of the Agents Tracing UI" style="max-height: 803px;">

### Core concepts:

1. [**Agents**](https://openai.github.io/openai-agents-python/agents): LLMs configured with instructions, tools, guardrails, and handoffs
2. [**Handoffs**](https://openai.github.io/openai-agents-python/handoffs/): Allow agents to transfer control to other agents for specific tasks
3. [**Guardrails**](https://openai.github.io/openai-agents-python/guardrails/): Configurable safety checks for input and output validation
4. [**Tracing**](https://openai.github.io/openai-agents-python/tracing/): Built-in tracking of agent runs, allowing you to view, debug and optimize your workflows

Explore the [examples](examples) directory to see the SDK in action, and read our [documentation](https://openai.github.io/openai-agents-python/) for more details.

Notably, our SDK [is compatible](https://openai.github.io/openai-agents-python/models/) with any model providers that support the OpenAI Chat Completions API format.

## Get started

1. Set up your Python environment

```
python -m venv env
source env/bin/activate
```

2. Install Agents SDK

```
pip install openai-agents
```

## Hello world example

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.
```

(_If running this, ensure you set the `OPENAI_API_KEY` environment variable_)

(_For Jupyter notebook users, see [hello_world_jupyter.py](examples/basic/hello_world_jupyter.py)_)

## Handoffs example

```python
from agents import Agent, Runner
import asyncio

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
)


async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)
    # ¡Hola! Estoy bien, gracias por preguntar. ¿Y tú, cómo estás?


if __name__ == "__main__":
    asyncio.run(main())
```

## Functions example

```python
import asyncio

from agents import Agent, Runner, function_tool


@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."


agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)


async def main():
    result = await Runner.run(agent, input="What's the weather in Tokyo?")
    print(result.final_output)
    # The weather in Tokyo is sunny.


if __name__ == "__main__":
    asyncio.run(main())
```

## The agent loop

When you call `Runner.run()`, we run a loop until we get a final output.

1. We call the LLM, using the model and settings on the agent, and the message history.
2. The LLM returns a response, which may include tool calls.
3. If the response has a final output (see below for more on this), we return it and end the loop.
4. If the response has a handoff, we set the agent to the new agent and go back to step 1.
5. We process the tool calls (if any) and append the tool responses messages. Then we go to step 1.

There is a `max_turns` parameter that you can use to limit the number of times the loop executes.

### Final output

Final output is the last thing the agent produces in the loop.

1.  If you set an `output_type` on the agent, the final output is when the LLM returns something of that type. We use [structured outputs](https://platform.openai.com/docs/guides/structured-outputs) for this.
2.  If there's no `output_type` (i.e. plain text responses), then the first LLM response without any tool calls or handoffs is considered as the final output.

As a result, the mental model for the agent loop is:

1. If the current agent has an `output_type`, the loop runs until the agent produces structured output matching that type.
2. If the current agent does not have an `output_type`, the loop runs until the current agent produces a message without any tool calls/handoffs.

## Common agent patterns

The Agents SDK is designed to be highly flexible, allowing you to model a wide range of LLM workflows including deterministic flows, iterative loops, and more. See examples in [`examples/agent_patterns`](examples/agent_patterns).

## Tracing

The Agents SDK automatically traces your agent runs, making it easy to track and debug the behavior of your agents. Tracing is extensible by design, supporting custom spans and a wide variety of external destinations, including [Logfire](https://logfire.pydantic.dev/docs/integrations/llms/openai/#openai-agents), [AgentOps](https://docs.agentops.ai/v1/integrations/agentssdk), [Braintrust](https://braintrust.dev/docs/guides/traces/integrations#openai-agents-sdk), [Scorecard](https://docs.scorecard.io/docs/documentation/features/tracing#openai-agents-sdk-integration), and [Keywords AI](https://docs.keywordsai.co/integration/development-frameworks/openai-agent). For more details about how to customize or disable tracing, see [Tracing](http://openai.github.io/openai-agents-python/tracing).

## Development (only needed if you need to edit the SDK/examples)

0. Ensure you have [`uv`](https://docs.astral.sh/uv/) installed.

```bash
uv --version
```

1. Install dependencies

```bash
make sync
```

2. (After making changes) lint/test

```
make tests  # run tests
make mypy   # run typechecker
make lint   # run linter
```

## Acknowledgements

We'd like to acknowledge the excellent work of the open-source community, especially:

-   [Pydantic](https://docs.pydantic.dev/latest/) (data validation) and [PydanticAI](https://ai.pydantic.dev/) (advanced agent framework)
-   [MkDocs](https://github.com/squidfunk/mkdocs-material)
-   [Griffe](https://github.com/mkdocstrings/griffe)
-   [uv](https://github.com/astral-sh/uv) and [ruff](https://github.com/astral-sh/ruff)

We're committed to continuing to build the Agents SDK as an open source framework so others in the community can expand on our approach.



--- START OF FILE docs/guardrails.md ---

# Guardrails

Guardrails run _in parallel_ to your agents, enabling you to do checks and validations of user input. For example, imagine you have an agent that uses a very smart (and hence slow/expensive) model to help with customer requests. You wouldn't want malicious users to ask the model to help them with their math homework. So, you can run a guardrail with a fast/cheap model. If the guardrail detects malicious usage, it can immediately raise an error, which stops the expensive model from running and saves you time/money.

There are two kinds of guardrails:

1. Input guardrails run on the initial user input
2. Output guardrails run on the final agent output

## Input guardrails

Input guardrails run in 3 steps:

1. First, the guardrail receives the same input passed to the agent.
2. Next, the guardrail function runs to produce a [`GuardrailFunctionOutput`][agents.guardrail.GuardrailFunctionOutput], which is then wrapped in an [`InputGuardrailResult`][agents.guardrail.InputGuardrailResult]
3. Finally, we check if [`.tripwire_triggered`][agents.guardrail.GuardrailFunctionOutput.tripwire_triggered] is true. If true, an [`InputGuardrailTripwireTriggered`][agents.exceptions.InputGuardrailTripwireTriggered] exception is raised, so you can appropriately respond to the user or handle the exception.

!!! Note

    Input guardrails are intended to run on user input, so an agent's guardrails only run if the agent is the *first* agent. You might wonder, why is the `guardrails` property on the agent instead of passed to `Runner.run`? It's because guardrails tend to be related to the actual Agent - you'd run different guardrails for different agents, so colocating the code is useful for readability.

## Output guardrails

Output guardrails run in 3 steps:

1. First, the guardrail receives the same input passed to the agent.
2. Next, the guardrail function runs to produce a [`GuardrailFunctionOutput`][agents.guardrail.GuardrailFunctionOutput], which is then wrapped in an [`OutputGuardrailResult`][agents.guardrail.OutputGuardrailResult]
3. Finally, we check if [`.tripwire_triggered`][agents.guardrail.GuardrailFunctionOutput.tripwire_triggered] is true. If true, an [`OutputGuardrailTripwireTriggered`][agents.exceptions.OutputGuardrailTripwireTriggered] exception is raised, so you can appropriately respond to the user or handle the exception.

!!! Note

    Output guardrails are intended to run on the final agent input, so an agent's guardrails only run if the agent is the *last* agent. Similar to the input guardrails, we do this because guardrails tend to be related to the actual Agent - you'd run different guardrails for different agents, so colocating the code is useful for readability.

## Tripwires

If the input or output fails the guardrail, the Guardrail can signal this with a tripwire. As soon as we see a guardrail that has triggered the tripwires, we immediately raise a `{Input,Output}GuardrailTripwireTriggered` exception and halt the Agent execution.

## Implementing a guardrail

You need to provide a function that receives input, and returns a [`GuardrailFunctionOutput`][agents.guardrail.GuardrailFunctionOutput]. In this example, we'll do this by running an Agent under the hood.

```python
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent( # (1)!
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
)


@input_guardrail
async def math_guardrail( # (2)!
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output, # (3)!
        tripwire_triggered=result.final_output.is_math_homework,
    )


agent = Agent(  # (4)!
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
)

async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?")
        print("Guardrail didn't trip - this is unexpected")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")
```

1. We'll use this agent in our guardrail function.
2. This is the guardrail function that receives the agent's input/context, and returns the result.
3. We can include extra information in the guardrail result.
4. This is the actual agent that defines the workflow.

Output guardrails are similar.

```python
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
)
class MessageOutput(BaseModel): # (1)!
    response: str

class MathOutput(BaseModel): # (2)!
    is_math: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the output includes any math.",
    output_type=MathOutput,
)

@output_guardrail
async def math_guardrail(  # (3)!
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, output.response, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math,
    )

agent = Agent( # (4)!
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[math_guardrail],
    output_type=MessageOutput,
)

async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?")
        print("Guardrail didn't trip - this is unexpected")

    except OutputGuardrailTripwireTriggered:
        print("Math output guardrail tripped")
```

1. This is the actual agent's output type.
2. This is the guardrail's output type.
3. This is the guardrail function that receives the agent's output, and returns the result.
4. This is the actual agent that defines the workflow.



--- START OF FILE docs/context.md ---

# Context management

Context is an overloaded term. There are two main classes of context you might care about:

1. Context available locally to your code: this is data and dependencies you might need when tool functions run, during callbacks like `on_handoff`, in lifecycle hooks, etc.
2. Context available to LLMs: this is data the LLM sees when generating a response.

## Local context

This is represented via the [`RunContextWrapper`][agents.run_context.RunContextWrapper] class and the [`context`][agents.run_context.RunContextWrapper.context] property within it. The way this works is:

1. You create any Python object you want. A common pattern is to use a dataclass or a Pydantic object.
2. You pass that object to the various run methods (e.g. `Runner.run(..., **context=whatever**))`.
3. All your tool calls, lifecycle hooks etc will be passed a wrapper object, `RunContextWrapper[T]`, where `T` represents your context object type which you can access via `wrapper.context`.

The **most important** thing to be aware of: every agent, tool function, lifecycle etc for a given agent run must use the same _type_ of context.

You can use the context for things like:

-   Contextual data for your run (e.g. things like a username/uid or other information about the user)
-   Dependencies (e.g. logger objects, data fetchers, etc)
-   Helper functions

!!! danger "Note"

    The context object is **not** sent to the LLM. It is purely a local object that you can read from, write to and call methods on it.

```python
import asyncio
from dataclasses import dataclass

from agents import Agent, RunContextWrapper, Runner, function_tool

@dataclass
class UserInfo:  # (1)!
    name: str
    uid: int

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  # (2)!
    return f"User {wrapper.context.name} is 47 years old"

async def main():
    user_info = UserInfo(name="John", uid=123)  # (3)!

    agent = Agent[UserInfo](  # (4)!
        name="Assistant",
        tools=[fetch_user_age],
    )

    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info,
    )

    print(result.final_output)  # (5)!
    # The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())
```

1. This is the context object. We've used a dataclass here, but you can use any type.
2. This is a tool. You can see it takes a `RunContextWrapper[UserInfo]`. The tool implementation reads from the context.
3. We mark the agent with the generic `UserInfo`, so that the typechecker can catch errors (for example, if we tried to pass a tool that took a different context type).
4. The context is passed to the `run` function.
5. The agent correctly calls the tool and gets the age.

## Agent/LLM context

When an LLM is called, the **only** data it can see is from the conversation history. This means that if you want to make some new data available to the LLM, you must do it in a way that makes it available in that history. There are a few ways to do this:

1. You can add it to the Agent `instructions`. This is also known as a "system prompt" or "developer message". System prompts can be static strings, or they can be dynamic functions that receive the context and output a string. This is a common tactic for information that is always useful (for example, the user's name or the current date).
2. Add it to the `input` when calling the `Runner.run` functions. This is similar to the `instructions` tactic, but allows you to have messages that are lower in the [chain of command](https://cdn.openai.com/spec/model-spec-2024-05-08.html#follow-the-chain-of-command).
3. Expose it via function tools. This is useful for _on-demand_ context - the LLM decides when it needs some data, and can call the tool to fetch that data.
4. Use retrieval or web search. These are special tools that are able to fetch relevant data from files or databases (retrieval), or from the web (web search). This is useful for "grounding" the response in relevant contextual data.



--- START OF FILE docs/quickstart.md ---

# Quickstart

## Create a project and virtual environment

You'll only need to do this once.

```bash
mkdir my_project
cd my_project
python -m venv .venv
```

### Activate the virtual environment

Do this every time you start a new terminal session.

```bash
source .venv/bin/activate
```

### Install the Agents SDK

```bash
pip install openai-agents # or `uv add openai-agents`, etc
```

### Set an OpenAI API key

If you don't have one, follow [these instructions](https://platform.openai.com/docs/quickstart#create-and-export-an-api-key) to create an OpenAI API key.

```bash
export OPENAI_API_KEY=sk-...
```

## Create your first agent

Agents are defined with instructions, a name, and optional config (such as `model_config`)

```python
from agents import Agent

agent = Agent(
    name="Math Tutor",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)
```

## Add a few more agents

Additional agents can be defined in the same way. `handoff_descriptions` provide additional context for determining handoff routing

```python
from agents import Agent

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)
```

## Define your handoffs

On each agent, you can define an inventory of outgoing handoff options that the agent can choose from to decide how to make progress on their task.

```python
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent]
)
```

## Run the agent orchestration

Let's check that the workflow runs and the triage agent correctly routes between the two specialist agents.

```python
from agents import Runner

async def main():
    result = await Runner.run(triage_agent, "What is the capital of France?")
    print(result.final_output)
```

## Add a guardrail

You can define custom guardrails to run on the input or output.

```python
from agents import GuardrailFunctionOutput, Agent, Runner
from pydantic import BaseModel

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )
```

## Put it all together

Let's put it all together and run the entire workflow, using handoffs and the input guardrail.

```python
from agents import Agent, InputGuardrail,GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)


async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

async def main():
    result = await Runner.run(triage_agent, "who was the first president of the united states?")
    print(result.final_output)

    result = await Runner.run(triage_agent, "what is life")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## View your traces

To review what happened during your agent run, navigate to the [Trace viewer in the OpenAI Dashboard](https://platform.openai.com/traces) to view traces of your agent runs.

## Next steps

Learn how to build more complex agentic flows:

-   Learn about how to configure [Agents](agents.md).
-   Learn about [running agents](running_agents.md).
-   Learn about [tools](tools.md), [guardrails](guardrails.md) and [models](models.md).



--- START OF FILE docs/handoffs.md ---

# Handoffs

Handoffs allow an agent to delegate tasks to another agent. This is particularly useful in scenarios where different agents specialize in distinct areas. For example, a customer support app might have agents that each specifically handle tasks like order status, refunds, FAQs, etc.

Handoffs are represented as tools to the LLM. So if there's a handoff to an agent named `Refund Agent`, the tool would be called `transfer_to_refund_agent`.

## Creating a handoff

All agents have a [`handoffs`][agents.agent.Agent.handoffs] param, which can either take an `Agent` directly, or a `Handoff` object that customizes the Handoff.

You can create a handoff using the [`handoff()`][agents.handoffs.handoff] function provided by the Agents SDK. This function allows you to specify the agent to hand off to, along with optional overrides and input filters.

### Basic Usage

Here's how you can create a simple handoff:

```python
from agents import Agent, handoff

billing_agent = Agent(name="Billing agent")
refund_agent = Agent(name="Refund agent")

# (1)!
triage_agent = Agent(name="Triage agent", handoffs=[billing_agent, handoff(refund_agent)])
```

1. You can use the agent directly (as in `billing_agent`), or you can use the `handoff()` function.

### Customizing handoffs via the `handoff()` function

The [`handoff()`][agents.handoffs.handoff] function lets you customize things.

-   `agent`: This is the agent to which things will be handed off.
-   `tool_name_override`: By default, the `Handoff.default_tool_name()` function is used, which resolves to `transfer_to_<agent_name>`. You can override this.
-   `tool_description_override`: Override the default tool description from `Handoff.default_tool_description()`
-   `on_handoff`: A callback function executed when the handoff is invoked. This is useful for things like kicking off some data fetching as soon as you know a handoff is being invoked. This function receives the agent context, and can optionally also receive LLM generated input. The input data is controlled by the `input_type` param.
-   `input_type`: The type of input expected by the handoff (optional).
-   `input_filter`: This lets you filter the input received by the next agent. See below for more.

```python
from agents import Agent, handoff, RunContextWrapper

def on_handoff(ctx: RunContextWrapper[None]):
    print("Handoff called")

agent = Agent(name="My agent")

handoff_obj = handoff(
    agent=agent,
    on_handoff=on_handoff,
    tool_name_override="custom_handoff_tool",
    tool_description_override="Custom description",
)
```

## Handoff inputs

In certain situations, you want the LLM to provide some data when it calls a handoff. For example, imagine a handoff to an "Escalation agent". You might want a reason to be provided, so you can log it.

```python
from pydantic import BaseModel

from agents import Agent, handoff, RunContextWrapper

class EscalationData(BaseModel):
    reason: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
    print(f"Escalation agent called with reason: {input_data.reason}")

agent = Agent(name="Escalation agent")

handoff_obj = handoff(
    agent=agent,
    on_handoff=on_handoff,
    input_type=EscalationData,
)
```

## Input filters

When a handoff occurs, it's as though the new agent takes over the conversation, and gets to see the entire previous conversation history. If you want to change this, you can set an [`input_filter`][agents.handoffs.Handoff.input_filter]. An input filter is a function that receives the existing input via a [`HandoffInputData`][agents.handoffs.HandoffInputData], and must return a new `HandoffInputData`.

There are some common patterns (for example removing all tool calls from the history), which are implemented for you in [`agents.extensions.handoff_filters`][]

```python
from agents import Agent, handoff
from agents.extensions import handoff_filters

agent = Agent(name="FAQ agent")

handoff_obj = handoff(
    agent=agent,
    input_filter=handoff_filters.remove_all_tools, # (1)!
)
```

1. This will automatically remove all tools from the history when `FAQ agent` is called.

## Recommended prompts

To make sure that LLMs understand handoffs properly, we recommend including information about handoffs in your agents. We have a suggested prefix in [`agents.extensions.handoff_prompt.RECOMMENDED_PROMPT_PREFIX`][], or you can call [`agents.extensions.handoff_prompt.prompt_with_handoff_instructions`][] to automatically add recommended data to your prompts.

```python
from agents import Agent
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

billing_agent = Agent(
    name="Billing agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    <Fill in the rest of your prompt here>.""",
)
```



--- START OF FILE docs/streaming.md ---

# Streaming

Streaming lets you subscribe to updates of the agent run as it proceeds. This can be useful for showing the end-user progress updates and partial responses.

To stream, you can call [`Runner.run_streamed()`][agents.run.Runner.run_streamed], which will give you a [`RunResultStreaming`][agents.result.RunResultStreaming]. Calling `result.stream_events()` gives you an async stream of [`StreamEvent`][agents.stream_events.StreamEvent] objects, which are described below.

## Raw response events

[`RawResponsesStreamEvent`][agents.stream_events.RawResponsesStreamEvent] are raw events passed directly from the LLM. They are in OpenAI Responses API format, which means each event has a type (like `response.created`, `response.output_text.delta`, etc) and data. These events are useful if you want to stream response messages to the user as soon as they are generated.

For example, this will output the text generated by the LLM token-by-token.

```python
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner

async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
    )

    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
```

## Run item events and agent events

[`RunItemStreamEvent`][agents.stream_events.RunItemStreamEvent]s are higher level events. They inform you when an item has been fully generated. This allows you to push progress updates at the level of "message generated", "tool ran", etc, instead of each token. Similarly, [`AgentUpdatedStreamEvent`][agents.stream_events.AgentUpdatedStreamEvent] gives you updates when the current agent changes (e.g. as the result of a handoff).

For example, this will ignore raw events and stream updates to the user.

```python
import asyncio
import random
from agents import Agent, ItemHelpers, Runner, function_tool

@function_tool
def how_many_jokes() -> int:
    return random.randint(1, 10)


async def main():
    agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes],
    )

    result = Runner.run_streamed(
        agent,
        input="Hello",
    )
    print("=== Run starting ===")

    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        # When the agent updates, print that
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        # When items are generated, print them
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types

    print("=== Run complete ===")


if __name__ == "__main__":
    asyncio.run(main())
```



--- START OF FILE docs/running_agents.md ---

# Running agents

You can run agents via the [`Runner`][agents.run.Runner] class. You have 3 options:

1. [`Runner.run()`][agents.run.Runner.run], which runs async and returns a [`RunResult`][agents.result.RunResult].
2. [`Runner.run_sync()`][agents.run.Runner.run_sync], which is a sync method and just runs `.run()` under the hood.
3. [`Runner.run_streamed()`][agents.run.Runner.run_streamed], which runs async and returns a [`RunResultStreaming`][agents.result.RunResultStreaming]. It calls the LLM in streaming mode, and streams those events to you as they are received.

```python
from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant")

    result = await Runner.run(agent, "Write a haiku about recursion in programming.")
    print(result.final_output)
    # Code within the code,
    # Functions calling themselves,
    # Infinite loop's dance.
```

Read more in the [results guide](results.md).

## The agent loop

When you use the run method in `Runner`, you pass in a starting agent and input. The input can either be a string (which is considered a user message), or a list of input items, which are the items in the OpenAI Responses API.

The runner then runs a loop:

1. We call the LLM for the current agent, with the current input.
2. The LLM produces its output.
    1. If the LLM returns a `final_output`, the loop ends and we return the result.
    2. If the LLM does a handoff, we update the current agent and input, and re-run the loop.
    3. If the LLM produces tool calls, we run those tool calls, append the results, and re-run the loop.
3. If we exceed the `max_turns` passed, we raise a [`MaxTurnsExceeded`][agents.exceptions.MaxTurnsExceeded] exception.

!!! note

    The rule for whether the LLM output is considered as a "final output" is that it produces text output with the desired type, and there are no tool calls.

## Streaming

Streaming allows you to additionally receive streaming events as the LLM runs. Once the stream is done, the [`RunResultStreaming`][agents.result.RunResultStreaming] will contain the complete information about the run, including all the new outputs produces. You can call `.stream_events()` for the streaming events. Read more in the [streaming guide](streaming.md).

## Run config

The `run_config` parameter lets you configure some global settings for the agent run:

-   [`model`][agents.run.RunConfig.model]: Allows setting a global LLM model to use, irrespective of what `model` each Agent has.
-   [`model_provider`][agents.run.RunConfig.model_provider]: A model provider for looking up model names, which defaults to OpenAI.
-   [`model_settings`][agents.run.RunConfig.model_settings]: Overrides agent-specific settings. For example, you can set a global `temperature` or `top_p`.
-   [`input_guardrails`][agents.run.RunConfig.input_guardrails], [`output_guardrails`][agents.run.RunConfig.output_guardrails]: A list of input or output guardrails to include on all runs.
-   [`handoff_input_filter`][agents.run.RunConfig.handoff_input_filter]: A global input filter to apply to all handoffs, if the handoff doesn't already have one. The input filter allows you to edit the inputs that are sent to the new agent. See the documentation in [`Handoff.input_filter`][agents.handoffs.Handoff.input_filter] for more details.
-   [`tracing_disabled`][agents.run.RunConfig.tracing_disabled]: Allows you to disable [tracing](tracing.md) for the entire run.
-   [`trace_include_sensitive_data`][agents.run.RunConfig.trace_include_sensitive_data]: Configures whether traces will include potentially sensitive data, such as LLM and tool call inputs/outputs.
-   [`workflow_name`][agents.run.RunConfig.workflow_name], [`trace_id`][agents.run.RunConfig.trace_id], [`group_id`][agents.run.RunConfig.group_id]: Sets the tracing workflow name, trace ID and trace group ID for the run. We recommend at least setting `workflow_name`. The session ID is an optional field that lets you link traces across multiple runs.
-   [`trace_metadata`][agents.run.RunConfig.trace_metadata]: Metadata to include on all traces.

## Conversations/chat threads

Calling any of the run methods can result in one or more agents running (and hence one or more LLM calls), but it represents a single logical turn in a chat conversation. For example:

1. User turn: user enter text
2. Runner run: first agent calls LLM, runs tools, does a handoff to a second agent, second agent runs more tools, and then produces an output.

At the end of the agent run, you can choose what to show to the user. For example, you might show the user every new item generated by the agents, or just the final output. Either way, the user might then ask a followup question, in which case you can call the run method again.

You can use the base [`RunResultBase.to_input_list()`][agents.result.RunResultBase.to_input_list] method to get the inputs for the next turn.

```python
async def main():
    agent = Agent(name="Assistant", instructions="Reply very concisely.")

    with trace(workflow_name="Conversation", group_id=thread_id):
        # First turn
        result = await Runner.run(agent, "What city is the Golden Gate Bridge in?")
        print(result.final_output)
        # San Francisco

        # Second turn
        new_input = result.to_input_list() + [{"role": "user", "content": "What state is it in?"}]
        result = await Runner.run(agent, new_input)
        print(result.final_output)
        # California
```

## Exceptions

The SDK raises exceptions in certain cases. The full list is in [`agents.exceptions`][]. As an overview:

-   [`AgentsException`][agents.exceptions.AgentsException] is the base class for all exceptions raised in the SDK.
-   [`MaxTurnsExceeded`][agents.exceptions.MaxTurnsExceeded] is raised when the run exceeds the `max_turns` passed to the run methods.
-   [`ModelBehaviorError`][agents.exceptions.ModelBehaviorError] is raised when the model produces invalid outputs, e.g. malformed JSON or using non-existent tools.
-   [`UserError`][agents.exceptions.UserError] is raised when you (the person writing code using the SDK) make an error using the SDK.
-   [`InputGuardrailTripwireTriggered`][agents.exceptions.InputGuardrailTripwireTriggered], [`OutputGuardrailTripwireTriggered`][agents.exceptions.OutputGuardrailTripwireTriggered] is raised when a [guardrail](guardrails.md) is tripped.



--- START OF FILE docs/config.md ---

# Configuring the SDK

## API keys and clients

By default, the SDK looks for the `OPENAI_API_KEY` environment variable for LLM requests and tracing, as soon as it is imported. If you are unable to set that environment variable before your app starts, you can use the [set_default_openai_key()][agents.set_default_openai_key] function to set the key.

```python
from agents import set_default_openai_key

set_default_openai_key("sk-...")
```

Alternatively, you can also configure an OpenAI client to be used. By default, the SDK creates an `AsyncOpenAI` instance, using the API key from the environment variable or the default key set above. You can change this by using the [set_default_openai_client()][agents.set_default_openai_client] function.

```python
from openai import AsyncOpenAI
from agents import set_default_openai_client

custom_client = AsyncOpenAI(base_url="...", api_key="...")
set_default_openai_client(custom_client)
```

Finally, you can also customize the OpenAI API that is used. By default, we use the OpenAI Responses API. You can override this to use the Chat Completions API by using the [set_default_openai_api()][agents.set_default_openai_api] function.

```python
from agents import set_default_openai_api

set_default_openai_api("chat_completions")
```

## Tracing

Tracing is enabled by default. It uses the OpenAI API keys from the section above by default (i.e. the environment variable or the default key you set). You can specifically set the API key used for tracing by using the [`set_tracing_export_api_key`][agents.set_tracing_export_api_key] function.

```python
from agents import set_tracing_export_api_key

set_tracing_export_api_key("sk-...")
```

You can also disable tracing entirely by using the [`set_tracing_disabled()`][agents.set_tracing_disabled] function.

```python
from agents import set_tracing_disabled

set_tracing_disabled(True)
```

## Debug logging

The SDK has two Python loggers without any handlers set. By default, this means that warnings and errors are sent to `stdout`, but other logs are suppressed.

To enable verbose logging, use the [`enable_verbose_stdout_logging()`][agents.enable_verbose_stdout_logging] function.

```python
from agents import enable_verbose_stdout_logging

enable_verbose_stdout_logging()
```

Alternatively, you can customize the logs by adding handlers, filters, formatters, etc. You can read more in the [Python logging guide](https://docs.python.org/3/howto/logging.html).

```python
import logging

logger =  logging.getLogger("openai.agents") # or openai.agents.tracing for the Tracing logger

# To make all logs show up
logger.setLevel(logging.DEBUG)
# To make info and above show up
logger.setLevel(logging.INFO)
# To make warning and above show up
logger.setLevel(logging.WARNING)
# etc

# You can customize this as needed, but this will output to `stderr` by default
logger.addHandler(logging.StreamHandler())
```

### Sensitive data in logs

Certain logs may contain sensitive data (for example, user data). If you want to disable this data from being logged, set the following environment variables.

To disable logging LLM inputs and outputs:

```bash
export OPENAI_AGENTS_DONT_LOG_MODEL_DATA=1
```

To disable logging tool inputs and outputs:

```bash
export OPENAI_AGENTS_DONT_LOG_TOOL_DATA=1
```



--- START OF FILE docs/results.md ---

# Results

When you call the `Runner.run` methods, you either get a:

-   [`RunResult`][agents.result.RunResult] if you call `run` or `run_sync`
-   [`RunResultStreaming`][agents.result.RunResultStreaming] if you call `run_streamed`

Both of these inherit from [`RunResultBase`][agents.result.RunResultBase], which is where most useful information is present.

## Final output

The [`final_output`][agents.result.RunResultBase.final_output] property contains the final output of the last agent that ran. This is either:

-   a `str`, if the last agent didn't have an `output_type` defined
-   an object of type `last_agent.output_type`, if the agent had an output type defined.

!!! note

    `final_output` is of type `Any`. We can't statically type this, because of handoffs. If handoffs occur, that means any Agent might be the last agent, so we don't statically know the set of possible output types.

## Inputs for the next turn

You can use [`result.to_input_list()`][agents.result.RunResultBase.to_input_list] to turn the result into an input list that concatenates the original input you provided, to the items generated during the agent run. This makes it convenient to take the outputs of one agent run and pass them into another run, or to run it in a loop and append new user inputs each time.

## Last agent

The [`last_agent`][agents.result.RunResultBase.last_agent] property contains the last agent that ran. Depending on your application, this is often useful for the next time the user inputs something. For example, if you have a frontline triage agent that hands off to a language-specific agent, you can store the last agent, and re-use it the next time the user messages the agent.

## New items

The [`new_items`][agents.result.RunResultBase.new_items] property contains the new items generated during the run. The items are [`RunItem`][agents.items.RunItem]s. A run item wraps the raw item generated by the LLM.

-   [`MessageOutputItem`][agents.items.MessageOutputItem] indicates a message from the LLM. The raw item is the message generated.
-   [`HandoffCallItem`][agents.items.HandoffCallItem] indicates that the LLM called the handoff tool. The raw item is the tool call item from the LLM.
-   [`HandoffOutputItem`][agents.items.HandoffOutputItem] indicates that a handoff occurred. The raw item is the tool response to the handoff tool call. You can also access the source/target agents from the item.
-   [`ToolCallItem`][agents.items.ToolCallItem] indicates that the LLM invoked a tool.
-   [`ToolCallOutputItem`][agents.items.ToolCallOutputItem] indicates that a tool was called. The raw item is the tool response. You can also access the tool output from the item.
-   [`ReasoningItem`][agents.items.ReasoningItem] indicates a reasoning item from the LLM. The raw item is the reasoning generated.

## Other information

### Guardrail results

The [`input_guardrail_results`][agents.result.RunResultBase.input_guardrail_results] and [`output_guardrail_results`][agents.result.RunResultBase.output_guardrail_results] properties contain the results of the guardrails, if any. Guardrail results can sometimes contain useful information you want to log or store, so we make these available to you.

### Raw responses

The [`raw_responses`][agents.result.RunResultBase.raw_responses] property contains the [`ModelResponse`][agents.items.ModelResponse]s generated by the LLM.

### Original input

The [`input`][agents.result.RunResultBase.input] property contains the original input you provided to the `run` method. In most cases you won't need this, but it's available in case you do.



--- START OF FILE docs/index.md ---

# OpenAI Agents SDK

The [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) enables you to build agentic AI apps in a lightweight, easy-to-use package with very few abstractions. It's a production-ready upgrade of our previous experimentation for agents, [Swarm](https://github.com/openai/swarm/tree/main). The Agents SDK has a very small set of primitives:

-   **Agents**, which are LLMs equipped with instructions and tools
-   **Handoffs**, which allow agents to delegate to other agents for specific tasks
-   **Guardrails**, which enable the inputs to agents to be validated

In combination with Python, these primitives are powerful enough to express complex relationships between tools and agents, and allow you to build real-world applications without a steep learning curve. In addition, the SDK comes with built-in **tracing** that lets you visualize and debug your agentic flows, as well as evaluate them and even fine-tune models for your application.

## Why use the Agents SDK

The SDK has two driving design principles:

1. Enough features to be worth using, but few enough primitives to make it quick to learn.
2. Works great out of the box, but you can customize exactly what happens.

Here are the main features of the SDK:

-   Agent loop: Built-in agent loop that handles calling tools, sending results to the LLM, and looping until the LLM is done.
-   Python-first: Use built-in language features to orchestrate and chain agents, rather than needing to learn new abstractions.
-   Handoffs: A powerful feature to coordinate and delegate between multiple agents.
-   Guardrails: Run input validations and checks in parallel to your agents, breaking early if the checks fail.
-   Function tools: Turn any Python function into a tool, with automatic schema generation and Pydantic-powered validation.
-   Tracing: Built-in tracing that lets you visualize, debug and monitor your workflows, as well as use the OpenAI suite of evaluation, fine-tuning and distillation tools.

## Installation

```bash
pip install openai-agents
```

## Hello world example

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.
```

(_If running this, ensure you set the `OPENAI_API_KEY` environment variable_)

```bash
export OPENAI_API_KEY=sk-...
```



--- START OF FILE docs/models.md ---

# Models

The Agents SDK comes with out-of-the-box support for OpenAI models in two flavors:

-   **Recommended**: the [`OpenAIResponsesModel`][agents.models.openai_responses.OpenAIResponsesModel], which calls OpenAI APIs using the new [Responses API](https://platform.openai.com/docs/api-reference/responses).
-   The [`OpenAIChatCompletionsModel`][agents.models.openai_chatcompletions.OpenAIChatCompletionsModel], which calls OpenAI APIs using the [Chat Completions API](https://platform.openai.com/docs/api-reference/chat).

## Mixing and matching models

Within a single workflow, you may want to use different models for each agent. For example, you could use a smaller, faster model for triage, while using a larger, more capable model for complex tasks. When configuring an [`Agent`][agents.Agent], you can select a specific model by either:

1. Passing the name of an OpenAI model.
2. Passing any model name + a [`ModelProvider`][agents.models.interface.ModelProvider] that can map that name to a Model instance.
3. Directly providing a [`Model`][agents.models.interface.Model] implementation.

!!!note

    While our SDK supports both the [`OpenAIResponsesModel`][agents.models.openai_responses.OpenAIResponsesModel] and the [`OpenAIChatCompletionsModel`][agents.models.openai_chatcompletions.OpenAIChatCompletionsModel] shapes, we recommend using a single model shape for each workflow because the two shapes support a different set of features and tools. If your workflow requires mixing and matching model shapes, make sure that all the features you're using are available on both.

```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import asyncio

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
    model="o3-mini", # (1)!
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
    model=OpenAIChatCompletionsModel( # (2)!
        model="gpt-4o",
        openai_client=AsyncOpenAI()
    ),
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
    model="gpt-3.5-turbo",
)

async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)
```

1.  Sets the name of an OpenAI model directly.
2.  Provides a [`Model`][agents.models.interface.Model] implementation.

## Using other LLM providers

You can use other LLM providers in 3 ways (examples [here](https://github.com/openai/openai-agents-python/tree/main/examples/model_providers/)):

1. [`set_default_openai_client`][agents.set_default_openai_client] is useful in cases where you want to globally use an instance of `AsyncOpenAI` as the LLM client. This is for cases where the LLM provider has an OpenAI compatible API endpoint, and you can set the `base_url` and `api_key`. See a configurable example in [examples/model_providers/custom_example_global.py](https://github.com/openai/openai-agents-python/tree/main/examples/model_providers/custom_example_global.py).
2. [`ModelProvider`][agents.models.interface.ModelProvider] is at the `Runner.run` level. This lets you say "use a custom model provider for all agents in this run". See a configurable example in [examples/model_providers/custom_example_provider.py](https://github.com/openai/openai-agents-python/tree/main/examples/model_providers/custom_example_provider.py).
3. [`Agent.model`][agents.agent.Agent.model] lets you specify the model on a specific Agent instance. This enables you to mix and match different providers for different agents. See a configurable example in [examples/model_providers/custom_example_agent.py](https://github.com/openai/openai-agents-python/tree/main/examples/model_providers/custom_example_agent.py).

In cases where you do not have an API key from `platform.openai.com`, we recommend disabling tracing via `set_tracing_disabled()`, or setting up a [different tracing processor](tracing.md).

!!! note

    In these examples, we use the Chat Completions API/model, because most LLM providers don't yet support the Responses API. If your LLM provider does support it, we recommend using Responses.

## Common issues with using other LLM providers

### Tracing client error 401

If you get errors related to tracing, this is because traces are uploaded to OpenAI servers, and you don't have an OpenAI API key. You have three options to resolve this:

1. Disable tracing entirely: [`set_tracing_disabled(True)`][agents.set_tracing_disabled].
2. Set an OpenAI key for tracing: [`set_tracing_export_api_key(...)`][agents.set_tracing_export_api_key]. This API key will only be used for uploading traces, and must be from [platform.openai.com](https://platform.openai.com/).
3. Use a non-OpenAI trace processor. See the [tracing docs](tracing.md#custom-tracing-processors).

### Responses API support

The SDK uses the Responses API by default, but most other LLM providers don't yet support it. You may see 404s or similar issues as a result. To resolve, you have two options:

1. Call [`set_default_openai_api("chat_completions")`][agents.set_default_openai_api]. This works if you are setting `OPENAI_API_KEY` and `OPENAI_BASE_URL` via environment vars.
2. Use [`OpenAIChatCompletionsModel`][agents.models.openai_chatcompletions.OpenAIChatCompletionsModel]. There are examples [here](https://github.com/openai/openai-agents-python/tree/main/examples/model_providers/).

### Structured outputs support

Some model providers don't have support for [structured outputs](https://platform.openai.com/docs/guides/structured-outputs). This sometimes results in an error that looks something like this:

```
BadRequestError: Error code: 400 - {'error': {'message': "'response_format.type' : value is not one of the allowed values ['text','json_object']", 'type': 'invalid_request_error'}}
```

This is a shortcoming of some model providers - they support JSON outputs, but don't allow you to specify the `json_schema` to use for the output. We are working on a fix for this, but we suggest relying on providers that do have support for JSON schema output, because otherwise your app will often break because of malformed JSON.



--- START OF FILE docs/tracing.md ---

# Tracing

The Agents SDK includes built-in tracing, collecting a comprehensive record of events during an agent run: LLM generations, tool calls, handoffs, guardrails, and even custom events that occur. Using the [Traces dashboard](https://platform.openai.com/traces), you can debug, visualize, and monitor your workflows during development and in production.

!!!note

    Tracing is enabled by default. There are two ways to disable tracing:

    1. You can globally disable tracing by setting the env var `OPENAI_AGENTS_DISABLE_TRACING=1`
    2. You can disable tracing for a single run by setting [`agents.run.RunConfig.tracing_disabled`][] to `True`

## Traces and spans

-   **Traces** represent a single end-to-end operation of a "workflow". They're composed of Spans. Traces have the following properties:
    -   `workflow_name`: This is the logical workflow or app. For example "Code generation" or "Customer service".
    -   `trace_id`: A unique ID for the trace. Automatically generated if you don't pass one. Must have the format `trace_<32_alphanumeric>`.
    -   `group_id`: Optional group ID, to link multiple traces from the same conversation. For example, you might use a chat thread ID.
    -   `disabled`: If True, the trace will not be recorded.
    -   `metadata`: Optional metadata for the trace.
-   **Spans** represent operations that have a start and end time. Spans have:
    -   `started_at` and `ended_at` timestamps.
    -   `trace_id`, to represent the trace they belong to
    -   `parent_id`, which points to the parent Span of this Span (if any)
    -   `span_data`, which is information about the Span. For example, `AgentSpanData` contains information about the Agent, `GenerationSpanData` contains information about the LLM generation, etc.

## Default tracing

By default, the SDK traces the following:

-   The entire `Runner.{run, run_sync, run_streamed}()` is wrapped in a `trace()`.
-   Each time an agent runs, it is wrapped in `agent_span()`
-   LLM generations are wrapped in `generation_span()`
-   Function tool calls are each wrapped in `function_span()`
-   Guardrails are wrapped in `guardrail_span()`
-   Handoffs are wrapped in `handoff_span()`

By default, the trace is named "Agent trace". You can set this name if you use `trace`, or you can can configure the name and other properties with the [`RunConfig`][agents.run.RunConfig].

In addition, you can set up [custom trace processors](#custom-tracing-processors) to push traces to other destinations (as a replacement, or secondary destination).

## Higher level traces

Sometimes, you might want multiple calls to `run()` to be part of a single trace. You can do this by wrapping the entire code in a `trace()`.

```python
from agents import Agent, Runner, trace

async def main():
    agent = Agent(name="Joke generator", instructions="Tell funny jokes.")

    with trace("Joke workflow"): # (1)!
        first_result = await Runner.run(agent, "Tell me a joke")
        second_result = await Runner.run(agent, f"Rate this joke: {first_result.final_output}")
        print(f"Joke: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")
```

1. Because the two calls to `Runner.run` are wrapped in a `with trace()`, the individual runs will be part of the overall trace rather than creating two traces.

## Creating traces

You can use the [`trace()`][agents.tracing.trace] function to create a trace. Traces need to be started and finished. You have two options to do so:

1. **Recommended**: use the trace as a context manager, i.e. `with trace(...) as my_trace`. This will automatically start and end the trace at the right time.
2. You can also manually call [`trace.start()`][agents.tracing.Trace.start] and [`trace.finish()`][agents.tracing.Trace.finish].

The current trace is tracked via a Python [`contextvar`](https://docs.python.org/3/library/contextvars.html). This means that it works with concurrency automatically. If you manually start/end a trace, you'll need to pass `mark_as_current` and `reset_current` to `start()`/`finish()` to update the current trace.

## Creating spans

You can use the various [`*_span()`][agents.tracing.create] methods to create a span. In general, you don't need to manually create spans. A [`custom_span()`][agents.tracing.custom_span] function is available for tracking custom span information.

Spans are automatically part of the current trace, and are nested under the nearest current span, which is tracked via a Python [`contextvar`](https://docs.python.org/3/library/contextvars.html).

## Sensitive data

Some spans track potentially sensitive data. For example, the `generation_span()` stores the inputs/outputs of the LLM generation, and `function_span()` stores the inputs/outputs of function calls. These may contain sensitive data, so you can disable capturing that data via [`RunConfig.trace_include_sensitive_data`][agents.run.RunConfig.trace_include_sensitive_data].

## Custom tracing processors

The high level architecture for tracing is:

-   At initialization, we create a global [`TraceProvider`][agents.tracing.setup.TraceProvider], which is responsible for creating traces.
-   We configure the `TraceProvider` with a [`BatchTraceProcessor`][agents.tracing.processors.BatchTraceProcessor] that sends traces/spans in batches to a [`BackendSpanExporter`][agents.tracing.processors.BackendSpanExporter], which exports the spans and traces to the OpenAI backend in batches.

To customize this default setup, to send traces to alternative or additional backends or modifying exporter behavior, you have two options:

1. [`add_trace_processor()`][agents.tracing.add_trace_processor] lets you add an **additional** trace processor that will receive traces and spans as they are ready. This lets you do your own processing in addition to sending traces to OpenAI's backend.
2. [`set_trace_processors()`][agents.tracing.set_trace_processors] lets you **replace** the default processors with your own trace processors. This means traces will not be sent to the OpenAI backend unless you include a `TracingProcessor` that does so.

External trace processors include:

-   [Braintrust](https://braintrust.dev/docs/guides/traces/integrations#openai-agents-sdk)
-   [Pydantic Logfire](https://logfire.pydantic.dev/docs/integrations/llms/openai/#openai-agents)
-   [AgentOps](https://docs.agentops.ai/v1/integrations/agentssdk)
-   [Scorecard](https://docs.scorecard.io/docs/documentation/features/tracing#openai-agents-sdk-integration))
-   [Keywords AI](https://docs.keywordsai.co/integration/development-frameworks/openai-agent)



--- START OF FILE docs/agents.md ---

# Agents

Agents are the core building block in your apps. An agent is a large language model (LLM), configured with instructions and tools.

## Basic configuration

The most common properties of an agent you'll configure are:

-   `instructions`: also known as a developer message or system prompt.
-   `model`: which LLM to use, and optional `model_settings` to configure model tuning parameters like temperature, top_p, etc.
-   `tools`: Tools that the agent can use to achieve its tasks.

```python
from agents import Agent, ModelSettings, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model="o3-mini",
    tools=[get_weather],
)
```

## Context

Agents are generic on their `context` type. Context is a dependency-injection tool: it's an object you create and pass to `Runner.run()`, that is passed to every agent, tool, handoff etc, and it serves as a grab bag of dependencies and state for the agent run. You can provide any Python object as the context.

```python
@dataclass
class UserContext:
  uid: str
  is_pro_user: bool

  async def fetch_purchases() -> list[Purchase]:
     return ...

agent = Agent[UserContext](
    ...,
)
```

## Output types

By default, agents produce plain text (i.e. `str`) outputs. If you want the agent to produce a particular type of output, you can use the `output_type` parameter. A common choice is to use [Pydantic](https://docs.pydantic.dev/) objects, but we support any type that can be wrapped in a Pydantic [TypeAdapter](https://docs.pydantic.dev/latest/api/type_adapter/) - dataclasses, lists, TypedDict, etc.

```python
from pydantic import BaseModel
from agents import Agent


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

agent = Agent(
    name="Calendar extractor",
    instructions="Extract calendar events from text",
    output_type=CalendarEvent,
)
```

!!! note

    When you pass an `output_type`, that tells the model to use [structured outputs](https://platform.openai.com/docs/guides/structured-outputs) instead of regular plain text responses.

## Handoffs

Handoffs are sub-agents that the agent can delegate to. You provide a list of handoffs, and the agent can choose to delegate to them if relevant. This is a powerful pattern that allows orchestrating modular, specialized agents that excel at a single task. Read more in the [handoffs](handoffs.md) documentation.

```python
from agents import Agent

booking_agent = Agent(...)
refund_agent = Agent(...)

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions."
        "If they ask about booking, handoff to the booking agent."
        "If they ask about refunds, handoff to the refund agent."
    ),
    handoffs=[booking_agent, refund_agent],
)
```

## Dynamic instructions

In most cases, you can provide instructions when you create the agent. However, you can also provide dynamic instructions via a function. The function will receive the agent and context, and must return the prompt. Both regular and `async` functions are accepted.

```python
def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"The user's name is {context.context.name}. Help them with their questions."


agent = Agent[UserContext](
    name="Triage agent",
    instructions=dynamic_instructions,
)
```

## Lifecycle events (hooks)

Sometimes, you want to observe the lifecycle of an agent. For example, you may want to log events, or pre-fetch data when certain events occur. You can hook into the agent lifecycle with the `hooks` property. Subclass the [`AgentHooks`][agents.lifecycle.AgentHooks] class, and override the methods you're interested in.

## Guardrails

Guardrails allow you to run checks/validations on user input, in parallel to the agent running. For example, you could screen the user's input for relevance. Read more in the [guardrails](guardrails.md) documentation.

## Cloning/copying agents

By using the `clone()` method on an agent, you can duplicate an Agent, and optionally change any properties you like.

```python
pirate_agent = Agent(
    name="Pirate",
    instructions="Write like a pirate",
    model="o3-mini",
)

robot_agent = pirate_agent.clone(
    name="Robot",
    instructions="Write like a robot",
)
```



--- START OF FILE docs/tools.md ---

# Tools

Tools let agents take actions: things like fetching data, running code, calling external APIs, and even using a computer. There are three classes of tools in the Agent SDK:

-   Hosted tools: these run on LLM servers alongside the AI models. OpenAI offers retrieval, web search and computer use as hosted tools.
-   Function calling: these allow you to use any Python function as a tool.
-   Agents as tools: this allows you to use an agent as a tool, allowing Agents to call other agents without handing off to them.

## Hosted tools

OpenAI offers a few built-in tools when using the [`OpenAIResponsesModel`][agents.models.openai_responses.OpenAIResponsesModel]:

-   The [`WebSearchTool`][agents.tool.WebSearchTool] lets an agent search the web.
-   The [`FileSearchTool`][agents.tool.FileSearchTool] allows retrieving information from your OpenAI Vector Stores.
-   The [`ComputerTool`][agents.tool.ComputerTool] allows automating computer use tasks.

```python
from agents import Agent, FileSearchTool, Runner, WebSearchTool

agent = Agent(
    name="Assistant",
    tools=[
        WebSearchTool(),
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=["VECTOR_STORE_ID"],
        ),
    ],
)

async def main():
    result = await Runner.run(agent, "Which coffee shop should I go to, taking into account my preferences and the weather today in SF?")
    print(result.final_output)
```

## Function tools

You can use any Python function as a tool. The Agents SDK will setup the tool automatically:

-   The name of the tool will be the name of the Python function (or you can provide a name)
-   Tool description will be taken from the docstring of the function (or you can provide a description)
-   The schema for the function inputs is automatically created from the function's arguments
-   Descriptions for each input are taken from the docstring of the function, unless disabled

We use Python's `inspect` module to extract the function signature, along with [`griffe`](https://mkdocstrings.github.io/griffe/) to parse docstrings and `pydantic` for schema creation.

```python
import json

from typing_extensions import TypedDict, Any

from agents import Agent, FunctionTool, RunContextWrapper, function_tool


class Location(TypedDict):
    lat: float
    long: float

@function_tool  # (1)!
async def fetch_weather(location: Location) -> str:
    # (2)!
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    return "sunny"


@function_tool(name_override="fetch_data")  # (3)!
def read_file(ctx: RunContextWrapper[Any], path: str, directory: str | None = None) -> str:
    """Read the contents of a file.

    Args:
        path: The path to the file to read.
        directory: The directory to read the file from.
    """
    # In real life, we'd read the file from the file system
    return "<file contents>"


agent = Agent(
    name="Assistant",
    tools=[fetch_weather, read_file],  # (4)!
)

for tool in agent.tools:
    if isinstance(tool, FunctionTool):
        print(tool.name)
        print(tool.description)
        print(json.dumps(tool.params_json_schema, indent=2))
        print()

```

1.  You can use any Python types as arguments to your functions, and the function can be sync or async.
2.  Docstrings, if present, are used to capture descriptions and argument descriptions
3.  Functions can optionally take the `context` (must be the first argument). You can also set overrides, like the name of the tool, description, which docstring style to use, etc.
4.  You can pass the decorated functions to the list of tools.

??? note "Expand to see output"

    ```
    fetch_weather
    Fetch the weather for a given location.
    {
    "$defs": {
      "Location": {
        "properties": {
          "lat": {
            "title": "Lat",
            "type": "number"
          },
          "long": {
            "title": "Long",
            "type": "number"
          }
        },
        "required": [
          "lat",
          "long"
        ],
        "title": "Location",
        "type": "object"
      }
    },
    "properties": {
      "location": {
        "$ref": "#/$defs/Location",
        "description": "The location to fetch the weather for."
      }
    },
    "required": [
      "location"
    ],
    "title": "fetch_weather_args",
    "type": "object"
    }

    fetch_data
    Read the contents of a file.
    {
    "properties": {
      "path": {
        "description": "The path to the file to read.",
        "title": "Path",
        "type": "string"
      },
      "directory": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "default": null,
        "description": "The directory to read the file from.",
        "title": "Directory"
      }
    },
    "required": [
      "path"
    ],
    "title": "fetch_data_args",
    "type": "object"
    }
    ```

### Custom function tools

Sometimes, you don't want to use a Python function as a tool. You can directly create a [`FunctionTool`][agents.tool.FunctionTool] if you prefer. You'll need to provide:

-   `name`
-   `description`
-   `params_json_schema`, which is the JSON schema for the arguments
-   `on_invoke_tool`, which is an async function that receives the context and the arguments as a JSON string, and must return the tool output as a string.

```python
from typing import Any

from pydantic import BaseModel

from agents import RunContextWrapper, FunctionTool



def do_some_work(data: str) -> str:
    return "done"


class FunctionArgs(BaseModel):
    username: str
    age: int


async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return do_some_work(data=f"{parsed.username} is {parsed.age} years old")


tool = FunctionTool(
    name="process_user",
    description="Processes extracted user data",
    params_json_schema=FunctionArgs.model_json_schema(),
    on_invoke_tool=run_function,
)
```

### Automatic argument and docstring parsing

As mentioned before, we automatically parse the function signature to extract the schema for the tool, and we parse the docstring to extract descriptions for the tool and for individual arguments. Some notes on that:

1. The signature parsing is done via the `inspect` module. We use type annotations to understand the types for the arguments, and dynamically build a Pydantic model to represent the overall schema. It supports most types, including Python primitives, Pydantic models, TypedDicts, and more.
2. We use `griffe` to parse docstrings. Supported docstring formats are `google`, `sphinx` and `numpy`. We attempt to automatically detect the docstring format, but this is best-effort and you can explicitly set it when calling `function_tool`. You can also disable docstring parsing by setting `use_docstring_info` to `False`.

The code for the schema extraction lives in [`agents.function_schema`][].

## Agents as tools

In some workflows, you may want a central agent to orchestrate a network of specialized agents, instead of handing off control. You can do this by modeling agents as tools.

```python
from agents import Agent, Runner
import asyncio

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish",
)

french_agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French",
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
    ],
)

async def main():
    result = await Runner.run(orchestrator_agent, input="Say 'Hello, how are you?' in Spanish.")
    print(result.final_output)
```

## Handling errors in function tools

When you create a function tool via `@function_tool`, you can pass a `failure_error_function`. This is a function that provides an error response to the LLM in case the tool call crashes.

-   By default (i.e. if you don't pass anything), it runs a `default_tool_error_function` which tells the LLM an error occurred.
-   If you pass your own error function, it runs that instead, and sends the response to the LLM.
-   If you explicitly pass `None`, then any tool call errors will be re-raised for you to handle. This could be a `ModelBehaviorError` if the model produced invalid JSON, or a `UserError` if your code crashed, etc.

If you are manually creating a `FunctionTool` object, then you must handle errors inside the `on_invoke_tool` function.



--- START OF FILE docs/multi_agent.md ---

# Orchestrating multiple agents

Orchestration refers to the flow of agents in your app. Which agents run, in what order, and how do they decide what happens next? There are two main ways to orchestrate agents:

1. Allowing the LLM to make decisions: this uses the intelligence of an LLM to plan, reason, and decide on what steps to take based on that.
2. Orchestrating via code: determining the flow of agents via your code.

You can mix and match these patterns. Each has their own tradeoffs, described below.

## Orchestrating via LLM

An agent is an LLM equipped with instructions, tools and handoffs. This means that given an open-ended task, the LLM can autonomously plan how it will tackle the task, using tools to take actions and acquire data, and using handoffs to delegate tasks to sub-agents. For example, a research agent could be equipped with tools like:

-   Web search to find information online
-   File search and retrieval to search through proprietary data and connections
-   Computer use to take actions on a computer
-   Code execution to do data analysis
-   Handoffs to specialized agents that are great at planning, report writing and more.

This pattern is great when the task is open-ended and you want to rely on the intelligence of an LLM. The most important tactics here are:

1. Invest in good prompts. Make it clear what tools are available, how to use them, and what parameters it must operate within.
2. Monitor your app and iterate on it. See where things go wrong, and iterate on your prompts.
3. Allow the agent to introspect and improve. For example, run it in a loop, and let it critique itself; or, provide error messages and let it improve.
4. Have specialized agents that excel in one task, rather than having a general purpose agent that is expected to be good at anything.
5. Invest in [evals](https://platform.openai.com/docs/guides/evals). This lets you train your agents to improve and get better at tasks.

## Orchestrating via code

While orchestrating via LLM is powerful, orchestrating via code makes tasks more deterministic and predictable, in terms of speed, cost and performance. Common patterns here are:

-   Using [structured outputs](https://platform.openai.com/docs/guides/structured-outputs) to generate well formed data that you can inspect with your code. For example, you might ask an agent to classify the task into a few categories, and then pick the next agent based on the category.
-   Chaining multiple agents by transforming the output of one into the input of the next. You can decompose a task like writing a blog post into a series of steps - do research, write an outline, write the blog post, critique it, and then improve it.
-   Running the agent that performs the task in a `while` loop with an agent that evaluates and provides feedback, until the evaluator says the output passes certain criteria.
-   Running multiple agents in parallel, e.g. via Python primitives like `asyncio.gather`. This is useful for speed when you have multiple tasks that don't depend on each other.

We have a number of examples in [`examples/agent_patterns`](https://github.com/openai/openai-agents-python/tree/main/examples/agent_patterns).



--- START OF FILE docs/ref/agent.md ---

# `Agents`

::: agents.agent



--- START OF FILE docs/ref/lifecycle.md ---

# `Lifecycle`

::: agents.lifecycle

    options:
        show_source: false



--- START OF FILE docs/ref/exceptions.md ---

# `Exceptions`

::: agents.exceptions



--- START OF FILE docs/ref/agent_output.md ---

# `Agent output`

::: agents.agent_output



--- START OF FILE docs/ref/result.md ---

# `Results`

::: agents.result



--- START OF FILE docs/ref/run_context.md ---

# `Run context`

::: agents.run_context



--- START OF FILE docs/ref/tool.md ---

# `Tools`

::: agents.tool



--- START OF FILE docs/ref/usage.md ---

# `Usage`

::: agents.usage



--- START OF FILE docs/ref/items.md ---

# `Items`

::: agents.items



--- START OF FILE docs/ref/handoffs.md ---

# `Handoffs`

::: agents.handoffs



--- START OF FILE docs/ref/guardrail.md ---

# `Guardrails`

::: agents.guardrail



--- START OF FILE docs/ref/stream_events.md ---

# `Streaming events`

::: agents.stream_events



--- START OF FILE docs/ref/index.md ---

# Agents module

::: agents

    options:
        members:
            - set_default_openai_key
            - set_default_openai_client
            - set_default_openai_api
            - set_tracing_export_api_key
            - set_tracing_disabled
            - set_trace_processors
            - enable_verbose_stdout_logging



--- START OF FILE docs/ref/run.md ---

# `Runner`

::: agents.run

    options:
        members:
            - Runner
            - RunConfig



--- START OF FILE docs/ref/model_settings.md ---

# `Model settings`

::: agents.model_settings



--- START OF FILE docs/ref/function_schema.md ---

# `Function schema`

::: agents.function_schema



--- START OF FILE docs/ref/tracing/processor_interface.md ---

# `Processor interface`

::: agents.tracing.processor_interface



--- START OF FILE docs/ref/tracing/setup.md ---

# `Setup`

::: agents.tracing.setup



--- START OF FILE docs/ref/tracing/scope.md ---

# `Scope`

::: agents.tracing.scope



--- START OF FILE docs/ref/tracing/processors.md ---

# `Processors`

::: agents.tracing.processors



--- START OF FILE docs/ref/tracing/traces.md ---

# `Traces`

::: agents.tracing.traces



--- START OF FILE docs/ref/tracing/index.md ---

# Tracing module

::: agents.tracing



--- START OF FILE docs/ref/tracing/create.md ---

# `Creating traces/spans`

::: agents.tracing.create



--- START OF FILE docs/ref/tracing/spans.md ---

# `Spans`

::: agents.tracing.spans

    options:
        members:
            - Span
            - NoOpSpan
            - SpanImpl



--- START OF FILE docs/ref/tracing/util.md ---

# `Util`

::: agents.tracing.util



--- START OF FILE docs/ref/tracing/span_data.md ---

# `Span data`

::: agents.tracing.span_data



--- START OF FILE docs/ref/models/openai_responses.md ---

# `OpenAI Responses model`

::: agents.models.openai_responses



--- START OF FILE docs/ref/models/interface.md ---

# `Model interface`

::: agents.models.interface



--- START OF FILE docs/ref/models/openai_chatcompletions.md ---

# `OpenAI Chat Completions model`

::: agents.models.openai_chatcompletions



--- START OF FILE docs/ref/extensions/handoff_filters.md ---

# `Handoff filters`

::: agents.extensions.handoff_filters



--- START OF FILE docs/ref/extensions/handoff_prompt.md ---

# `Handoff prompt`

::: agents.extensions.handoff_prompt

    options:
        members:
            - RECOMMENDED_PROMPT_PREFIX
            - prompt_with_handoff_instructions



--- START OF FILE docs/stylesheets/extra.css ---

@font-face {
    font-display: swap;
    font-family: "OpenAI Sans";
    font-style: normal;
    font-weight: 400;
    src: url("https://cdn.openai.com/common/fonts/openai-sans/OpenAISans-Regular.woff2")
        format("woff2");
}

@font-face {
    font-display: swap;
    font-family: "OpenAI Sans";
    font-style: italic;
    font-weight: 400;
    src: url("https://cdn.openai.com/common/fonts/openai-sans/OpenAISans-RegularItalic.woff2")
        format("woff2");
}

@font-face {
    font-display: swap;
    font-family: "OpenAI Sans";
    font-style: normal;
    font-weight: 500;
    src: url("https://cdn.openai.com/common/fonts/openai-sans/OpenAISans-Medium.woff2")
        format("woff2");
}

@font-face {
    font-display: swap;
    font-family: "OpenAI Sans";
    font-style: italic;
    font-weight: 500;
    src: url("https://cdn.openai.com/common/fonts/openai-sans/OpenAISans-MediumItalic.woff2")
        format("woff2");
}

@font-face {
    font-display: swap;
    font-family: "OpenAI Sans";
    font-style: normal;
    font-weight: 600;
    src: url("https://cdn.openai.com/common/fonts/openai-sans/OpenAISans-Semibold.woff2")
        format("woff2");
}

@font-face {
    font-display: swap;
    font-family: "OpenAI Sans";
    font-style: italic;
    font-weight: 600;
    src: url("https://cdn.openai.com/common/fonts/openai-sans/OpenAISans-SemiboldItalic.woff2")
        format("woff2");
}

@font-face {
    font-display: swap;
    font-family: "OpenAI Sans";
    font-style: normal;
    font-weight: 700;
    src: url("https://cdn.openai.com/common/fonts/openai-sans/OpenAISans-Bold.woff2")
        format("woff2");
}

@font-face {
    font-display: swap;
    font-family: "OpenAI Sans";
    font-style: italic;
    font-weight: 700;
    src: url("https://cdn.openai.com/common/fonts/openai-sans/OpenAISans-BoldItalic.woff2")
        format("woff2");
}

/* 
    Root variables that apply to all color schemes.
    Material for MkDocs automatically switches data-md-color-scheme
    between "default" (light) and "slate" (dark) when you use the toggles.
*/
:root {
    /* Font families */
    --md-text-font: "OpenAI Sans", -apple-system, system-ui, Helvetica, Arial,
        sans-serif;
    --md-typeface-heading: "OpenAI Sans", -apple-system, system-ui, Helvetica,
        Arial, sans-serif;

    /* Global color variables */
    --md-default-fg-color: #212121;
    --md-default-bg-color: #ffffff;
    --md-primary-fg-color: #000;
    --md-accent-fg-color: #000;

    /* Code block theming */
    --md-code-fg-color: red;
    --md-code-bg-color: #f5f5f5;

    /* Tables, blockquotes, etc. */
    --md-table-row-border-color: #e0e0e0;
    --md-admonition-bg-color: #f8f8f8;
    --md-admonition-title-fg-color: #373737;
    --md-default-fg-color--light: #000;

    --md-typeset-a-color: #000;
    --md-accent-fg-color: #000;

    --md-code-fg-color: #000;
}

/* Header styling */
.md-header {
    background-color: #000;
}

.md-header--shadow {
    box-shadow: none;
}

.md-content .md-typeset h1 {
    color: #000;
}

.md-typeset p,
.md-typeset li {
    font-size: 16px;
}

.md-typeset__table p {
    line-height: 1em;
}

.md-nav {
    font-size: 14px;
}
.md-nav__title {
    color: #000;
    font-weight: 600;
}

.md-typeset h1,
.md-typeset h2,
.md-typeset h3,
.md-typeset h4 {
    font-weight: 600;
}

.md-typeset h1 code {
    color: #000;
    padding: 0;
    background-color: transparent;
}
.md-footer {
    display: none;
}

.md-header__title {
    margin-left: 0 !important;
}

.md-typeset .admonition,
.md-typeset details {
    border: none;
    outline: none;
    border-radius: 8px;
    overflow: hidden;
}

.md-typeset pre > code {
    font-size: 14px;
}

.md-typeset__table code {
    font-size: 14px;
}

/* Custom link styling */
.md-content a {
    text-decoration: none;
}

.md-content a:hover {
    text-decoration: underline;
}

/* Code block styling */
.md-content .md-code__content {
    border-radius: 8px;
}

.md-clipboard.md-icon {
    color: #9e9e9e;
}

/* Reset scrollbar styling to browser default with high priority */
.md-sidebar__scrollwrap {
    scrollbar-color: auto !important;
}



--- START OF FILE examples/__init__.py ---

# Make the examples directory into a package to avoid top-level module name collisions.
# This is needed so that mypy treats files like examples/customer_service/main.py and
# examples/researcher_app/main.py as distinct modules rather than both named "main".



--- START OF FILE examples/tools/computer_use.py ---

import asyncio
import base64
from typing import Literal, Union

from playwright.async_api import Browser, Page, Playwright, async_playwright

from agents import (
    Agent,
    AsyncComputer,
    Button,
    ComputerTool,
    Environment,
    ModelSettings,
    Runner,
    trace,
)

# Uncomment to see very verbose logs
# import logging
# logging.getLogger("openai.agents").setLevel(logging.DEBUG)
# logging.getLogger("openai.agents").addHandler(logging.StreamHandler())


async def main():
    async with LocalPlaywrightComputer() as computer:
        with trace("Computer use example"):
            agent = Agent(
                name="Browser user",
                instructions="You are a helpful agent.",
                tools=[ComputerTool(computer)],
                # Use the computer using model, and set truncation to auto because its required
                model="computer-use-preview",
                model_settings=ModelSettings(truncation="auto"),
            )
            result = await Runner.run(agent, "Search for SF sports news and summarize.")
            print(result.final_output)


CUA_KEY_TO_PLAYWRIGHT_KEY = {
    "/": "Divide",
    "\\": "Backslash",
    "alt": "Alt",
    "arrowdown": "ArrowDown",
    "arrowleft": "ArrowLeft",
    "arrowright": "ArrowRight",
    "arrowup": "ArrowUp",
    "backspace": "Backspace",
    "capslock": "CapsLock",
    "cmd": "Meta",
    "ctrl": "Control",
    "delete": "Delete",
    "end": "End",
    "enter": "Enter",
    "esc": "Escape",
    "home": "Home",
    "insert": "Insert",
    "option": "Alt",
    "pagedown": "PageDown",
    "pageup": "PageUp",
    "shift": "Shift",
    "space": " ",
    "super": "Meta",
    "tab": "Tab",
    "win": "Meta",
}


class LocalPlaywrightComputer(AsyncComputer):
    """A computer, implemented using a local Playwright browser."""

    def __init__(self):
        self._playwright: Union[Playwright, None] = None
        self._browser: Union[Browser, None] = None
        self._page: Union[Page, None] = None

    async def _get_browser_and_page(self) -> tuple[Browser, Page]:
        width, height = self.dimensions
        launch_args = [f"--window-size={width},{height}"]
        browser = await self.playwright.chromium.launch(headless=False, args=launch_args)
        page = await browser.new_page()
        await page.set_viewport_size({"width": width, "height": height})
        await page.goto("https://www.bing.com")
        return browser, page

    async def __aenter__(self):
        # Start Playwright and call the subclass hook for getting browser/page
        self._playwright = await async_playwright().start()
        self._browser, self._page = await self._get_browser_and_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    @property
    def playwright(self) -> Playwright:
        assert self._playwright is not None
        return self._playwright

    @property
    def browser(self) -> Browser:
        assert self._browser is not None
        return self._browser

    @property
    def page(self) -> Page:
        assert self._page is not None
        return self._page

    @property
    def environment(self) -> Environment:
        return "browser"

    @property
    def dimensions(self) -> tuple[int, int]:
        return (1024, 768)

    async def screenshot(self) -> str:
        """Capture only the viewport (not full_page)."""
        png_bytes = await self.page.screenshot(full_page=False)
        return base64.b64encode(png_bytes).decode("utf-8")

    async def click(self, x: int, y: int, button: Button = "left") -> None:
        playwright_button: Literal["left", "middle", "right"] = "left"

        # Playwright only supports left, middle, right buttons
        if button in ("left", "right", "middle"):
            playwright_button = button  # type: ignore

        await self.page.mouse.click(x, y, button=playwright_button)

    async def double_click(self, x: int, y: int) -> None:
        await self.page.mouse.dblclick(x, y)

    async def scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:
        await self.page.mouse.move(x, y)
        await self.page.evaluate(f"window.scrollBy({scroll_x}, {scroll_y})")

    async def type(self, text: str) -> None:
        await self.page.keyboard.type(text)

    async def wait(self) -> None:
        await asyncio.sleep(1)

    async def move(self, x: int, y: int) -> None:
        await self.page.mouse.move(x, y)

    async def keypress(self, keys: list[str]) -> None:
        for key in keys:
            mapped_key = CUA_KEY_TO_PLAYWRIGHT_KEY.get(key.lower(), key)
            await self.page.keyboard.press(mapped_key)

    async def drag(self, path: list[tuple[int, int]]) -> None:
        if not path:
            return
        await self.page.mouse.move(path[0][0], path[0][1])
        await self.page.mouse.down()
        for px, py in path[1:]:
            await self.page.mouse.move(px, py)
        await self.page.mouse.up()


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/tools/file_search.py ---

import asyncio

from agents import Agent, FileSearchTool, Runner, trace


async def main():
    agent = Agent(
        name="File searcher",
        instructions="You are a helpful agent.",
        tools=[
            FileSearchTool(
                max_num_results=3,
                vector_store_ids=["vs_67bf88953f748191be42b462090e53e7"],
                include_search_results=True,
            )
        ],
    )

    with trace("File search example"):
        result = await Runner.run(
            agent, "Be concise, and tell me 1 sentence about Arrakis I might not know."
        )
        print(result.final_output)
        """
        Arrakis, the desert planet in Frank Herbert's "Dune," was inspired by the scarcity of water
        as a metaphor for oil and other finite resources.
        """

        print("\n".join([str(out) for out in result.new_items]))
        """
        {"id":"...", "queries":["Arrakis"], "results":[...]}
        """


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/tools/web_search.py ---

import asyncio

from agents import Agent, Runner, WebSearchTool, trace


async def main():
    agent = Agent(
        name="Web searcher",
        instructions="You are a helpful agent.",
        tools=[WebSearchTool(user_location={"type": "approximate", "city": "New York"})],
    )

    with trace("Web search example"):
        result = await Runner.run(
            agent,
            "search the web for 'local sports news' and give me 1 interesting update in a sentence.",
        )
        print(result.final_output)
        # The New York Giants are reportedly pursuing quarterback Aaron Rodgers after his ...


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/customer_service/main.py ---

from __future__ import annotations as _annotations

import asyncio
import random
import uuid

from pydantic import BaseModel

from agents import (
    Agent,
    HandoffOutputItem,
    ItemHelpers,
    MessageOutputItem,
    RunContextWrapper,
    Runner,
    ToolCallItem,
    ToolCallOutputItem,
    TResponseInputItem,
    function_tool,
    handoff,
    trace,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

### CONTEXT


class AirlineAgentContext(BaseModel):
    passenger_name: str | None = None
    confirmation_number: str | None = None
    seat_number: str | None = None
    flight_number: str | None = None


### TOOLS


@function_tool(
    name_override="faq_lookup_tool", description_override="Lookup frequently asked questions."
)
async def faq_lookup_tool(question: str) -> str:
    if "bag" in question or "baggage" in question:
        return (
            "You are allowed to bring one bag on the plane. "
            "It must be under 50 pounds and 22 inches x 14 inches x 9 inches."
        )
    elif "seats" in question or "plane" in question:
        return (
            "There are 120 seats on the plane. "
            "There are 22 business class seats and 98 economy seats. "
            "Exit rows are rows 4 and 16. "
            "Rows 5-8 are Economy Plus, with extra legroom. "
        )
    elif "wifi" in question:
        return "We have free wifi on the plane, join Airline-Wifi"
    return "I'm sorry, I don't know the answer to that question."


@function_tool
async def update_seat(
    context: RunContextWrapper[AirlineAgentContext], confirmation_number: str, new_seat: str
) -> str:
    """
    Update the seat for a given confirmation number.

    Args:
        confirmation_number: The confirmation number for the flight.
        new_seat: The new seat to update to.
    """
    # Update the context based on the customer's input
    context.context.confirmation_number = confirmation_number
    context.context.seat_number = new_seat
    # Ensure that the flight number has been set by the incoming handoff
    assert context.context.flight_number is not None, "Flight number is required"
    return f"Updated seat to {new_seat} for confirmation number {confirmation_number}"


### HOOKS


async def on_seat_booking_handoff(context: RunContextWrapper[AirlineAgentContext]) -> None:
    flight_number = f"FLT-{random.randint(100, 999)}"
    context.context.flight_number = flight_number


### AGENTS

faq_agent = Agent[AirlineAgentContext](
    name="FAQ Agent",
    handoff_description="A helpful agent that can answer questions about the airline.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are an FAQ agent. If you are speaking to a customer, you probably were transferred to from the triage agent.
    Use the following routine to support the customer.
    # Routine
    1. Identify the last question asked by the customer.
    2. Use the faq lookup tool to answer the question. Do not rely on your own knowledge.
    3. If you cannot answer the question, transfer back to the triage agent.""",
    tools=[faq_lookup_tool],
)

seat_booking_agent = Agent[AirlineAgentContext](
    name="Seat Booking Agent",
    handoff_description="A helpful agent that can update a seat on a flight.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are a seat booking agent. If you are speaking to a customer, you probably were transferred to from the triage agent.
    Use the following routine to support the customer.
    # Routine
    1. Ask for their confirmation number.
    2. Ask the customer what their desired seat number is.
    3. Use the update seat tool to update the seat on the flight.
    If the customer asks a question that is not related to the routine, transfer back to the triage agent. """,
    tools=[update_seat],
)

triage_agent = Agent[AirlineAgentContext](
    name="Triage Agent",
    handoff_description="A triage agent that can delegate a customer's request to the appropriate agent.",
    instructions=(
        f"{RECOMMENDED_PROMPT_PREFIX} "
        "You are a helpful triaging agent. You can use your tools to delegate questions to other appropriate agents."
    ),
    handoffs=[
        faq_agent,
        handoff(agent=seat_booking_agent, on_handoff=on_seat_booking_handoff),
    ],
)

faq_agent.handoffs.append(triage_agent)
seat_booking_agent.handoffs.append(triage_agent)


### RUN


async def main():
    current_agent: Agent[AirlineAgentContext] = triage_agent
    input_items: list[TResponseInputItem] = []
    context = AirlineAgentContext()

    # Normally, each input from the user would be an API request to your app, and you can wrap the request in a trace()
    # Here, we'll just use a random UUID for the conversation ID
    conversation_id = uuid.uuid4().hex[:16]

    while True:
        user_input = input("Enter your message: ")
        with trace("Customer service", group_id=conversation_id):
            input_items.append({"content": user_input, "role": "user"})
            result = await Runner.run(current_agent, input_items, context=context)

            for new_item in result.new_items:
                agent_name = new_item.agent.name
                if isinstance(new_item, MessageOutputItem):
                    print(f"{agent_name}: {ItemHelpers.text_message_output(new_item)}")
                elif isinstance(new_item, HandoffOutputItem):
                    print(
                        f"Handed off from {new_item.source_agent.name} to {new_item.target_agent.name}"
                    )
                elif isinstance(new_item, ToolCallItem):
                    print(f"{agent_name}: Calling a tool")
                elif isinstance(new_item, ToolCallOutputItem):
                    print(f"{agent_name}: Tool call output: {new_item.output}")
                else:
                    print(f"{agent_name}: Skipping item: {new_item.__class__.__name__}")
            input_items = result.to_input_list()
            current_agent = result.last_agent


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/model_providers/custom_example_global.py ---

import asyncio
import os

from openai import AsyncOpenAI

from agents import (
    Agent,
    Runner,
    function_tool,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)

BASE_URL = os.getenv("EXAMPLE_BASE_URL") or ""
API_KEY = os.getenv("EXAMPLE_API_KEY") or ""
MODEL_NAME = os.getenv("EXAMPLE_MODEL_NAME") or ""

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code."
    )


"""This example uses a custom provider for all requests by default. We do three things:
1. Create a custom client.
2. Set it as the default OpenAI client, and don't use it for tracing.
3. Set the default API as Chat Completions, as most LLM providers don't yet support Responses API.

Note that in this example, we disable tracing under the assumption that you don't have an API key
from platform.openai.com. If you do have one, you can either set the `OPENAI_API_KEY` env var
or call set_tracing_export_api_key() to set a tracing specific key.
"""

client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)
set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)


@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=MODEL_NAME,
        tools=[get_weather],
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/model_providers/custom_example_agent.py ---

import asyncio
import os

from openai import AsyncOpenAI

from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled

BASE_URL = os.getenv("EXAMPLE_BASE_URL") or ""
API_KEY = os.getenv("EXAMPLE_API_KEY") or ""
MODEL_NAME = os.getenv("EXAMPLE_MODEL_NAME") or ""

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code."
    )

"""This example uses a custom provider for a specific agent. Steps:
1. Create a custom OpenAI client.
2. Create a `Model` that uses the custom client.
3. Set the `model` on the Agent.

Note that in this example, we disable tracing under the assumption that you don't have an API key
from platform.openai.com. If you do have one, you can either set the `OPENAI_API_KEY` env var
or call set_tracing_export_api_key() to set a tracing specific key.
"""
client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)

# An alternate approach that would also work:
# PROVIDER = OpenAIProvider(openai_client=client)
# agent = Agent(..., model="some-custom-model")
# Runner.run(agent, ..., run_config=RunConfig(model_provider=PROVIDER))


@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
        tools=[get_weather],
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/model_providers/custom_example_provider.py ---

from __future__ import annotations

import asyncio
import os

from openai import AsyncOpenAI

from agents import (
    Agent,
    Model,
    ModelProvider,
    OpenAIChatCompletionsModel,
    RunConfig,
    Runner,
    function_tool,
    set_tracing_disabled,
)

BASE_URL = os.getenv("EXAMPLE_BASE_URL") or ""
API_KEY = os.getenv("EXAMPLE_API_KEY") or ""
MODEL_NAME = os.getenv("EXAMPLE_MODEL_NAME") or ""

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code."
    )


"""This example uses a custom provider for some calls to Runner.run(), and direct calls to OpenAI for
others. Steps:
1. Create a custom OpenAI client.
2. Create a ModelProvider that uses the custom client.
3. Use the ModelProvider in calls to Runner.run(), only when we want to use the custom LLM provider.

Note that in this example, we disable tracing under the assumption that you don't have an API key
from platform.openai.com. If you do have one, you can either set the `OPENAI_API_KEY` env var
or call set_tracing_export_api_key() to set a tracing specific key.
"""
client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)


class CustomModelProvider(ModelProvider):
    def get_model(self, model_name: str | None) -> Model:
        return OpenAIChatCompletionsModel(model=model_name or MODEL_NAME, openai_client=client)


CUSTOM_MODEL_PROVIDER = CustomModelProvider()


@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


async def main():
    agent = Agent(name="Assistant", instructions="You only respond in haikus.", tools=[get_weather])

    # This will use the custom model provider
    result = await Runner.run(
        agent,
        "What's the weather in Tokyo?",
        run_config=RunConfig(model_provider=CUSTOM_MODEL_PROVIDER),
    )
    print(result.final_output)

    # If you uncomment this, it will use OpenAI directly, not the custom provider
    # result = await Runner.run(
    #     agent,
    #     "What's the weather in Tokyo?",
    # )
    # print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/model_providers/README.md ---

# Custom LLM providers

The examples in this directory demonstrate how you might use a non-OpenAI LLM provider. To run them, first set a base URL, API key and model.

```bash
export EXAMPLE_BASE_URL="..."
export EXAMPLE_API_KEY="..."
export EXAMPLE_MODEL_NAME"..."
```

Then run the examples, e.g.:

```
python examples/model_providers/custom_example_provider.py

Loops within themselves,
Function calls its own being,
Depth without ending.
```



--- START OF FILE examples/basic/lifecycle_example.py ---

import asyncio
import random
from typing import Any

from pydantic import BaseModel

from agents import Agent, RunContextWrapper, RunHooks, Runner, Tool, Usage, function_tool


class ExampleHooks(RunHooks):
    def __init__(self):
        self.event_counter = 0

    def _usage_to_str(self, usage: Usage) -> str:
        return f"{usage.requests} requests, {usage.input_tokens} input tokens, {usage.output_tokens} output tokens, {usage.total_tokens} total tokens"

    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(
            f"### {self.event_counter}: Agent {agent.name} started. Usage: {self._usage_to_str(context.usage)}"
        )

    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(
            f"### {self.event_counter}: Agent {agent.name} ended with output {output}. Usage: {self._usage_to_str(context.usage)}"
        )

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
        self.event_counter += 1
        print(
            f"### {self.event_counter}: Tool {tool.name} started. Usage: {self._usage_to_str(context.usage)}"
        )

    async def on_tool_end(
        self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str
    ) -> None:
        self.event_counter += 1
        print(
            f"### {self.event_counter}: Tool {tool.name} ended with result {result}. Usage: {self._usage_to_str(context.usage)}"
        )

    async def on_handoff(
        self, context: RunContextWrapper, from_agent: Agent, to_agent: Agent
    ) -> None:
        self.event_counter += 1
        print(
            f"### {self.event_counter}: Handoff from {from_agent.name} to {to_agent.name}. Usage: {self._usage_to_str(context.usage)}"
        )


hooks = ExampleHooks()

###


@function_tool
def random_number(max: int) -> int:
    """Generate a random number up to the provided max."""
    return random.randint(0, max)


@function_tool
def multiply_by_two(x: int) -> int:
    """Return x times two."""
    return x * 2


class FinalResult(BaseModel):
    number: int


multiply_agent = Agent(
    name="Multiply Agent",
    instructions="Multiply the number by 2 and then return the final result.",
    tools=[multiply_by_two],
    output_type=FinalResult,
)

start_agent = Agent(
    name="Start Agent",
    instructions="Generate a random number. If it's even, stop. If it's odd, hand off to the multipler agent.",
    tools=[random_number],
    output_type=FinalResult,
    handoffs=[multiply_agent],
)


async def main() -> None:
    user_input = input("Enter a max number: ")
    await Runner.run(
        start_agent,
        hooks=hooks,
        input=f"Generate a random number between 0 and {user_input}.",
    )

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
"""
$ python examples/basic/lifecycle_example.py

Enter a max number: 250
### 1: Agent Start Agent started. Usage: 0 requests, 0 input tokens, 0 output tokens, 0 total tokens
### 2: Tool random_number started. Usage: 1 requests, 148 input tokens, 15 output tokens, 163 total tokens
### 3: Tool random_number ended with result 101. Usage: 1 requests, 148 input tokens, 15 output tokens, 163 total tokens
### 4: Agent Start Agent started. Usage: 1 requests, 148 input tokens, 15 output tokens, 163 total tokens
### 5: Handoff from Start Agent to Multiply Agent. Usage: 2 requests, 323 input tokens, 30 output tokens, 353 total tokens
### 6: Agent Multiply Agent started. Usage: 2 requests, 323 input tokens, 30 output tokens, 353 total tokens
### 7: Tool multiply_by_two started. Usage: 3 requests, 504 input tokens, 46 output tokens, 550 total tokens
### 8: Tool multiply_by_two ended with result 202. Usage: 3 requests, 504 input tokens, 46 output tokens, 550 total tokens
### 9: Agent Multiply Agent started. Usage: 3 requests, 504 input tokens, 46 output tokens, 550 total tokens
### 10: Agent Multiply Agent ended with output number=202. Usage: 4 requests, 714 input tokens, 63 output tokens, 777 total tokens
Done!

"""



--- START OF FILE examples/basic/hello_world.py ---

import asyncio

from agents import Agent, Runner


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
    )

    result = await Runner.run(agent, "Tell me about recursion in programming.")
    print(result.final_output)
    # Function calls itself,
    # Looping in smaller pieces,
    # Endless by design.


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/basic/dynamic_system_prompt.py ---

import asyncio
import random
from typing import Literal

from agents import Agent, RunContextWrapper, Runner


class CustomContext:
    def __init__(self, style: Literal["haiku", "pirate", "robot"]):
        self.style = style


def custom_instructions(
    run_context: RunContextWrapper[CustomContext], agent: Agent[CustomContext]
) -> str:
    context = run_context.context
    if context.style == "haiku":
        return "Only respond in haikus."
    elif context.style == "pirate":
        return "Respond as a pirate."
    else:
        return "Respond as a robot and say 'beep boop' a lot."


agent = Agent(
    name="Chat agent",
    instructions=custom_instructions,
)


async def main():
    choice: Literal["haiku", "pirate", "robot"] = random.choice(["haiku", "pirate", "robot"])
    context = CustomContext(style=choice)
    print(f"Using style: {choice}\n")

    user_message = "Tell me a joke."
    print(f"User: {user_message}")
    result = await Runner.run(agent, user_message, context=context)

    print(f"Assistant: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())

"""
$ python examples/basic/dynamic_system_prompt.py

Using style: haiku

User: Tell me a joke.
Assistant: Why don't eggs tell jokes?
They might crack each other's shells,
leaving yolk on face.

$ python examples/basic/dynamic_system_prompt.py
Using style: robot

User: Tell me a joke.
Assistant: Beep boop! Why was the robot so bad at soccer? Beep boop... because it kept kicking up a debug! Beep boop!

$ python examples/basic/dynamic_system_prompt.py
Using style: pirate

User: Tell me a joke.
Assistant: Why did the pirate go to school?

To improve his arrr-ticulation! Har har har! 🏴‍☠️
"""



--- START OF FILE examples/basic/stream_text.py ---

import asyncio

from openai.types.responses import ResponseTextDeltaEvent

from agents import Agent, Runner


async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
    )

    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/basic/hello_world_jupyter.py ---

from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

# Intended for Jupyter notebooks where there's an existing event loop
result = await Runner.run(agent, "Write a haiku about recursion in programming.") # type: ignore[top-level-await]  # noqa: F704
print(result.final_output)

# Code within code loops,
# Infinite mirrors reflect—
# Logic folds on self.



--- START OF FILE examples/basic/agent_lifecycle_example.py ---

import asyncio
import random
from typing import Any

from pydantic import BaseModel

from agents import Agent, AgentHooks, RunContextWrapper, Runner, Tool, function_tool


class CustomAgentHooks(AgentHooks):
    def __init__(self, display_name: str):
        self.event_counter = 0
        self.display_name = display_name

    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started")

    async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(
            f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended with output {output}"
        )

    async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent) -> None:
        self.event_counter += 1
        print(
            f"### ({self.display_name}) {self.event_counter}: Agent {source.name} handed off to {agent.name}"
        )

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
        self.event_counter += 1
        print(
            f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started tool {tool.name}"
        )

    async def on_tool_end(
        self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str
    ) -> None:
        self.event_counter += 1
        print(
            f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended tool {tool.name} with result {result}"
        )


###


@function_tool
def random_number(max: int) -> int:
    """
    Generate a random number up to the provided maximum.
    """
    return random.randint(0, max)


@function_tool
def multiply_by_two(x: int) -> int:
    """Simple multiplication by two."""
    return x * 2


class FinalResult(BaseModel):
    number: int


multiply_agent = Agent(
    name="Multiply Agent",
    instructions="Multiply the number by 2 and then return the final result.",
    tools=[multiply_by_two],
    output_type=FinalResult,
    hooks=CustomAgentHooks(display_name="Multiply Agent"),
)

start_agent = Agent(
    name="Start Agent",
    instructions="Generate a random number. If it's even, stop. If it's odd, hand off to the multipler agent.",
    tools=[random_number],
    output_type=FinalResult,
    handoffs=[multiply_agent],
    hooks=CustomAgentHooks(display_name="Start Agent"),
)


async def main() -> None:
    user_input = input("Enter a max number: ")
    await Runner.run(
        start_agent,
        input=f"Generate a random number between 0 and {user_input}.",
    )

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
"""
$ python examples/basic/agent_lifecycle_example.py

Enter a max number: 250
### (Start Agent) 1: Agent Start Agent started
### (Start Agent) 2: Agent Start Agent started tool random_number
### (Start Agent) 3: Agent Start Agent ended tool random_number with result 37
### (Start Agent) 4: Agent Start Agent started
### (Start Agent) 5: Agent Start Agent handed off to Multiply Agent
### (Multiply Agent) 1: Agent Multiply Agent started
### (Multiply Agent) 2: Agent Multiply Agent started tool multiply_by_two
### (Multiply Agent) 3: Agent Multiply Agent ended tool multiply_by_two with result 74
### (Multiply Agent) 4: Agent Multiply Agent started
### (Multiply Agent) 5: Agent Multiply Agent ended with output number=74
Done!
"""



--- START OF FILE examples/basic/stream_items.py ---

import asyncio
import random

from agents import Agent, ItemHelpers, Runner, function_tool


@function_tool
def how_many_jokes() -> int:
    return random.randint(1, 10)


async def main():
    agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes],
    )

    result = Runner.run_streamed(
        agent,
        input="Hello",
    )
    print("=== Run starting ===")
    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types

    print("=== Run complete ===")


if __name__ == "__main__":
    asyncio.run(main())

    # === Run starting ===
    # Agent updated: Joker
    # -- Tool was called
    # -- Tool output: 4
    # -- Message output:
    #  Sure, here are four jokes for you:

    # 1. **Why don't skeletons fight each other?**
    #    They don't have the guts!

    # 2. **What do you call fake spaghetti?**
    #    An impasta!

    # 3. **Why did the scarecrow win an award?**
    #    Because he was outstanding in his field!

    # 4. **Why did the bicycle fall over?**
    #    Because it was two-tired!
    # === Run complete ===



--- START OF FILE examples/research_bot/__init__.py ---





--- START OF FILE examples/research_bot/README.md ---

# Research bot

This is a simple example of a multi-agent research bot. To run it:

```bash
python -m examples.research_bot.main
```

## Architecture

The flow is:

1. User enters their research topic
2. `planner_agent` comes up with a plan to search the web for information. The plan is a list of search queries, with a search term and a reason for each query.
3. For each search item, we run a `search_agent`, which uses the Web Search tool to search for that term and summarize the results. These all run in parallel.
4. Finally, the `writer_agent` receives the search summaries, and creates a written report.

## Suggested improvements

If you're building your own research bot, some ideas to add to this are:

1. Retrieval: Add support for fetching relevant information from a vector store. You could use the File Search tool for this.
2. Image and file upload: Allow users to attach PDFs or other files, as baseline context for the research.
3. More planning and thinking: Models often produce better results given more time to think. Improve the planning process to come up with a better plan, and add an evaluation step so that the model can choose to improve its results, search for more stuff, etc.
4. Code execution: Allow running code, which is useful for data analysis.



--- START OF FILE examples/research_bot/main.py ---

import asyncio

from .manager import ResearchManager


async def main() -> None:
    query = input("What would you like to research? ")
    await ResearchManager().run(query)


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/research_bot/printer.py ---

from typing import Any

from rich.console import Console, Group
from rich.live import Live
from rich.spinner import Spinner


class Printer:
    def __init__(self, console: Console):
        self.live = Live(console=console)
        self.items: dict[str, tuple[str, bool]] = {}
        self.hide_done_ids: set[str] = set()
        self.live.start()

    def end(self) -> None:
        self.live.stop()

    def hide_done_checkmark(self, item_id: str) -> None:
        self.hide_done_ids.add(item_id)

    def update_item(
        self, item_id: str, content: str, is_done: bool = False, hide_checkmark: bool = False
    ) -> None:
        self.items[item_id] = (content, is_done)
        if hide_checkmark:
            self.hide_done_ids.add(item_id)
        self.flush()

    def mark_item_done(self, item_id: str) -> None:
        self.items[item_id] = (self.items[item_id][0], True)
        self.flush()

    def flush(self) -> None:
        renderables: list[Any] = []
        for item_id, (content, is_done) in self.items.items():
            if is_done:
                prefix = "✅ " if item_id not in self.hide_done_ids else ""
                renderables.append(prefix + content)
            else:
                renderables.append(Spinner("dots", text=content))
        self.live.update(Group(*renderables))



--- START OF FILE examples/research_bot/manager.py ---

from __future__ import annotations

import asyncio
import time

from rich.console import Console

from agents import Runner, custom_span, gen_trace_id, trace

from .agents.planner_agent import WebSearchItem, WebSearchPlan, planner_agent
from .agents.search_agent import search_agent
from .agents.writer_agent import ReportData, writer_agent
from .printer import Printer


class ResearchManager:
    def __init__(self):
        self.console = Console()
        self.printer = Printer(self.console)

    async def run(self, query: str) -> None:
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            self.printer.update_item(
                "trace_id",
                f"View trace: https://platform.openai.com/traces/{trace_id}",
                is_done=True,
                hide_checkmark=True,
            )

            self.printer.update_item(
                "starting",
                "Starting research...",
                is_done=True,
                hide_checkmark=True,
            )
            search_plan = await self._plan_searches(query)
            search_results = await self._perform_searches(search_plan)
            report = await self._write_report(query, search_results)

            final_report = f"Report summary\n\n{report.short_summary}"
            self.printer.update_item("final_report", final_report, is_done=True)

            self.printer.end()

        print("\n\n=====REPORT=====\n\n")
        print(f"Report: {report.markdown_report}")
        print("\n\n=====FOLLOW UP QUESTIONS=====\n\n")
        follow_up_questions = "\n".join(report.follow_up_questions)
        print(f"Follow up questions: {follow_up_questions}")

    async def _plan_searches(self, query: str) -> WebSearchPlan:
        self.printer.update_item("planning", "Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        self.printer.update_item(
            "planning",
            f"Will perform {len(result.final_output.searches)} searches",
            is_done=True,
        )
        return result.final_output_as(WebSearchPlan)

    async def _perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        with custom_span("Search the web"):
            self.printer.update_item("searching", "Searching...")
            num_completed = 0
            tasks = [asyncio.create_task(self._search(item)) for item in search_plan.searches]
            results = []
            for task in asyncio.as_completed(tasks):
                result = await task
                if result is not None:
                    results.append(result)
                num_completed += 1
                self.printer.update_item(
                    "searching", f"Searching... {num_completed}/{len(tasks)} completed"
                )
            self.printer.mark_item_done("searching")
            return results

    async def _search(self, item: WebSearchItem) -> str | None:
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def _write_report(self, query: str, search_results: list[str]) -> ReportData:
        self.printer.update_item("writing", "Thinking about report...")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = Runner.run_streamed(
            writer_agent,
            input,
        )
        update_messages = [
            "Thinking about report...",
            "Planning report structure...",
            "Writing outline...",
            "Creating sections...",
            "Cleaning up formatting...",
            "Finalizing report...",
            "Finishing report...",
        ]

        last_update = time.time()
        next_message = 0
        async for _ in result.stream_events():
            if time.time() - last_update > 5 and next_message < len(update_messages):
                self.printer.update_item("writing", update_messages[next_message])
                next_message += 1
                last_update = time.time()

        self.printer.mark_item_done("writing")
        return result.final_output_as(ReportData)



--- START OF FILE examples/research_bot/agents/planner_agent.py ---

from pydantic import BaseModel

from agents import Agent

PROMPT = (
    "You are a helpful research assistant. Given a query, come up with a set of web searches "
    "to perform to best answer the query. Output between 5 and 20 terms to query for."
)


class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best answer the query."""


planner_agent = Agent(
    name="PlannerAgent",
    instructions=PROMPT,
    model="gpt-4o",
    output_type=WebSearchPlan,
)



--- START OF FILE examples/research_bot/agents/__init__.py ---




--- START OF FILE examples/research_bot/agents/search_agent.py ---

from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and"
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300"
    "words. Capture the main points. Write succintly, no need to have complete sentences or good"
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the"
    "essence and ignore any fluff. Do not include any additional commentary other than the summary"
    "itself."
)

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
)



--- START OF FILE examples/research_bot/agents/writer_agent.py ---

# Agent used to synthesize a final report from the individual summaries.
from pydantic import BaseModel

from agents import Agent

PROMPT = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research "
    "assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words."
)


class ReportData(BaseModel):
    short_summary: str
    """A short 2-3 sentence summary of the findings."""

    markdown_report: str
    """The final report"""

    follow_up_questions: list[str]
    """Suggested topics to research further"""


writer_agent = Agent(
    name="WriterAgent",
    instructions=PROMPT,
    model="o3-mini",
    output_type=ReportData,
)



--- START OF FILE examples/research_bot/sample_outputs/vacation.md ---

Report: # Caribbean Adventure in April: Surfing, Hiking, and Water Sports Exploration

The Caribbean is renowned for its crystal-clear waters, vibrant culture, and diverse outdoor activities. April is an especially attractive month for visitors: warm temperatures, clear skies, and the promise of abundant activities. This report explores the best Caribbean destinations in April, with a focus on optimizing your vacation for surfing, hiking, and water sports.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Why April is the Perfect Time in the Caribbean](#why-april-is-the-perfect-time-in-the-caribbean)
3. [Surfing in the Caribbean](#surfing-in-the-caribbean)
    - 3.1 [Barbados: The Tale of Two Coasts](#barbados-the-tale-of-two-coasts)
    - 3.2 [Puerto Rico: Rincón and Beyond](#puerto-rico-rinc%C3%B3n-and-beyond)
    - 3.3 [Dominican Republic and Other Hotspots](#dominican-republic-and-other-hotspots)
4. [Hiking Adventures Across the Caribbean](#hiking-adventures-across-the-caribbean)
    - 4.1 [Trekking Through Tropical Rainforests](#trekking-through-tropical-rainforests)
    - 4.2 [Volcanic Peaks and Rugged Landscapes](#volcanic-peaks-and-rugged-landscapes)
5. [Diverse Water Sports Experiences](#diverse-water-sports-experiences)
    - 5.1 [Snorkeling, Diving, and Jet Skiing](#snorkeling-diving-and-jet-skiing)
    - 5.2 [Kiteboarding and Windsurfing](#kiteboarding-and-windsurfing)
6. [Combining Adventures: Multi-Activity Destinations](#combining-adventures-multi-activity-destinations)
7. [Practical Advice and Travel Tips](#practical-advice-and-travel-tips)
8. [Conclusion](#conclusion)

---

## Introduction

Caribbean vacations are much more than just beach relaxation; they offer adventure, exploration, and a lively cultural tapestry waiting to be discovered. For travelers seeking an adrenaline-filled getaway, April provides optimal conditions. This report synthesizes diverse research findings and travel insights to help you create an itinerary that combines the thrill of surfing, the challenge of hiking, and the excitement of water sports.

Whether you're standing on the edge of a powerful reef break or trekking through lush tropical landscapes, the Caribbean in April invites you to dive into nature, adventure, and culture. The following sections break down the best destinations and activities, ensuring that every aspect of your trip is meticulously planned for an unforgettable experience.

---

## Why April is the Perfect Time in the Caribbean

April stands at the crossroads of seasons in many Caribbean destinations. It marks the tail end of the dry season, ensuring:

-   **Consistent Warm Temperatures:** Average daytime highs around 29°C (84°F) foster comfortable conditions for both land and water activities.
-   **Pleasant Sea Temperatures:** With sea temperatures near 26°C (79°F), swimmers, surfers, and divers are treated to inviting waters.
-   **Clear Skies and Minimal Rainfall:** Crisp, blue skies make for excellent visibility during snorkeling and diving, as well as clear panoramic views while hiking.
-   **Festivals and Cultural Events:** Many islands host seasonal festivals such as Barbados' Fish Festival and Antigua's Sailing Week, adding a cultural layer to your vacation.

These factors create an ideal backdrop for balancing your outdoor pursuits, whether you’re catching epic waves, trekking rugged trails, or partaking in water sports.

---

## Surfing in the Caribbean

Surfing in the Caribbean offers diverse wave experiences, ranging from gentle, beginner-friendly rollers to powerful reef breaks that challenge even seasoned surfers. April, in particular, provides excellent conditions for those looking to ride its picturesque waves.

### Barbados: The Tale of Two Coasts

Barbados is a prime destination:

-   **Soup Bowl in Bathsheba:** On the east coast, the Soup Bowl is famous for its consistent, powerful waves. This spot attracts experienced surfers who appreciate its challenging right-hand reef break with steep drops, providing the kind of performance wave rarely found elsewhere.
-   **Freights Bay:** On the south coast, visitors find more forgiving, gentle wave conditions. Ideal for beginners and longboarders, this spot offers the perfect balance for those still mastering their craft.

Barbados not only excels in its surfing credentials but also complements the experience with a rich local culture and events in April, making it a well-rounded destination.

### Puerto Rico: Rincón and Beyond

Rincón in Puerto Rico is hailed as the Caribbean’s surfing capital:

-   **Diverse Breaks:** With spots ranging from challenging reef breaks such as Tres Palmas and Dogman's to more inviting waves at Domes and Maria's, Puerto Rico offers a spectrum for all surfing skill levels.
-   **Local Culture:** Aside from its surf culture, the island boasts vibrant local food scenes, historic sites, and exciting nightlife, enriching your overall travel experience.

In addition, Puerto Rico’s coasts often feature opportunities for hiking and other outdoor adventures, making it an attractive option for multi-activity travelers.

### Dominican Republic and Other Hotspots

Other islands such as the Dominican Republic, with Playa Encuentro on its north coast, provide consistent surf year-round. Highlights include:

-   **Playa Encuentro:** A hotspot known for its dependable breaks, ideal for both intermediate and advanced surfers during the cooler months of October to April.
-   **Jamaica and The Bahamas:** Jamaica’s Boston Bay offers a mix of beginner and intermediate waves, and The Bahamas’ Surfer’s Beach on Eleuthera draws parallels to the legendary surf spots of Hawaii, especially during the winter months.

These destinations not only spotlight surfing but also serve as gateways to additional outdoor activities, ensuring there's never a dull moment whether you're balancing waves with hikes or cultural exploration.

---

## Hiking Adventures Across the Caribbean

The Caribbean's topography is as varied as it is beautiful. Its network of hiking trails traverses volcanic peaks, ancient rainforests, and dramatic coastal cliffs, offering breathtaking vistas to intrepid explorers.

### Trekking Through Tropical Rainforests

For nature enthusiasts, the lush forests of the Caribbean present an immersive encounter with biodiversity:

-   **El Yunque National Forest, Puerto Rico:** The only tropical rainforest within the U.S. National Forest System, El Yunque is rich in endemic species such as the Puerto Rican parrot and the famous coquí frog. Trails like the El Yunque Peak Trail and La Mina Falls Trail provide both challenging hikes and scenic rewards.
-   **Virgin Islands National Park, St. John:** With over 20 well-defined trails, this park offers hikes that reveal historical petroglyphs, colonial ruins, and stunning coastal views along the Reef Bay Trail.

### Volcanic Peaks and Rugged Landscapes

For those seeking more rugged challenges, several destinations offer unforgettable adventures:

-   **Morne Trois Pitons National Park, Dominica:** A UNESCO World Heritage Site showcasing volcanic landscapes, hot springs, the famed Boiling Lake, and lush trails that lead to hidden waterfalls.
-   **Gros Piton, Saint Lucia:** The iconic hike up Gros Piton provides a moderately challenging trek that ends with panoramic views of the Caribbean Sea, a truly rewarding experience for hikers.
-   **La Soufrière, St. Vincent:** This active volcano not only offers a dynamic hiking environment but also the opportunity to observe the ongoing geological transformations up close.

Other noteworthy hiking spots include the Blue Mountains in Jamaica for coffee plantation tours and expansive views, as well as trails in Martinique around Montagne Pelée, which combine historical context with natural beauty.

---

## Diverse Water Sports Experiences

While surfing and hiking attract a broad range of adventurers, the Caribbean also scores high on other water sports. Whether you're drawn to snorkeling, jet skiing, or wind- and kiteboarding, the islands offer a plethora of aquatic activities.

### Snorkeling, Diving, and Jet Skiing

Caribbean waters teem with life and color, making them ideal for underwater exploration:

-   **Bonaire:** Its protected marine parks serve as a magnet for divers and snorkelers. With vibrant coral reefs and diverse marine species, Bonaire is a top destination for those who appreciate the underwater world.
-   **Cayman Islands:** Unique attractions such as Stingray City provide opportunities to interact with friendly stingrays in clear, calm waters. Additionally, the Underwater Sculpture Park is an innovative blend of art and nature.
-   **The Bahamas:** In places like Eleuthera, excursions often cater to families and thrill-seekers alike. Options include jet ski rentals, where groups can explore hidden beaches and pristine coves while enjoying the vibrant marine life.

### Kiteboarding and Windsurfing

Harnessing the steady trade winds and warm Caribbean waters, several islands have become hubs for kiteboarding and windsurfing:

-   **Aruba:** Known as "One Happy Island," Aruba’s Fisherman's Huts area provides consistent winds, perfect for enthusiasts of windsurfing and kiteboarding alike.
-   **Cabarete, Dominican Republic and Silver Rock, Barbados:** Both destinations benefit from reliable trade winds, making them popular among kitesurfers. These spots often combine water sports with a lively beach culture, ensuring that the fun continues on land as well.

Local operators provide equipment rental and lessons, ensuring that even first-time adventurers can safely and confidently enjoy these exciting sports.

---

## Combining Adventures: Multi-Activity Destinations

For travelers seeking a comprehensive vacation where surfing, hiking, and water sports converge, several Caribbean destinations offer the best of all worlds.

-   **Puerto Rico:** With its robust surf scene in Rincón, world-class hiking in El Yunque, and opportunities for snorkeling and jet skiing in San Juan Bay, Puerto Rico is a true multi-adventure destination.
-   **Barbados:** In addition to the surf breaks along its coasts, Barbados offers a mix of cultural events, local cuisine, and even hiking excursions to scenic rural areas, making for a well-rounded experience.
-   **Dominican Republic and Jamaica:** Both are renowned not only for their consistent surf conditions but also for expansive hiking trails and water sports. From the rugged landscapes of the Dominican Republic to Jamaica’s blend of cultural history and natural exploration, these islands allow travelers to mix and match activities seamlessly.

Group tours and local guides further enhance these experiences, providing insider tips, safe excursions, and personalized itineraries that cater to multiple interests within one trip.

---

## Practical Advice and Travel Tips

### Weather and Timing

-   **Optimal Climate:** April offers ideal weather conditions across the Caribbean. With minimal rainfall and warm temperatures, it is a great time to schedule outdoor activities.
-   **Surfing Seasons:** While April marks the end of the prime surf season in some areas (like Rincón in Puerto Rico), many destinations maintain consistent conditions during this month.

### Booking and Costs

-   **Surfing Lessons:** Expect to pay between $40 and $110 per session depending on the location. For instance, Puerto Rico typically charges around $75 for beginner lessons, while group lessons in the Dominican Republic average approximately $95.
-   **Equipment Rentals:** Pricing for jet ski, surfboard, and snorkeling equipment may vary. In the Bahamas, an hour-long jet ski tour might cost about $120 per group, whereas a similar experience might be available at a lower cost in other regions.
-   **Accommodations:** Prices also vary by island. Many travelers find that even affordable stays do not skimp on amenities, allowing you to invest more in guided excursions and local experiences.

### Cultural Considerations

-   **Festivals and Events:** Check local event calendars. Destinations like Barbados and Antigua host festivals in April that combine cultural heritage with festive outdoor activities.
-   **Local Cuisine:** Incorporate food tours into your itinerary. Caribbean cuisine—with its fusion of flavors—can be as adventurous as the outdoor activities.

### Health and Safety

-   **Staying Hydrated:** The warm temperatures demand that you stay properly hydrated. Always carry water, especially during long hikes.
-   **Sun Protection:** Use sunscreen, hats, and sunglasses to protect yourself during extended periods outdoors on both land and water.
-   **Local Guides:** Utilize local tour operators for both hiking and water sports. Their expertise not only enriches your experience but also ensures safety in unfamiliar terrain or water bodies.

---

## Conclusion

The Caribbean in April is a haven for adventure seekers. With its pristine beaches, diverse ecosystems, and rich cultural tapestry, it offers something for every type of traveler. Whether you're chasing the perfect wave along the shores of Barbados and Puerto Rico, trekking through the lush landscapes of El Yunque or Morne Trois Pitons, or engaging in an array of water sports from snorkeling to kiteboarding, your ideal vacation is only a booking away.

This report has outlined the best destinations and provided practical advice to optimize your vacation for surfing, hiking, and water sports. By considering the diverse offerings—from epic surf breaks and challenging hiking trails to vibrant water sports—the Caribbean stands out as a multi-adventure destination where every day brings a new experience.

Plan carefully, pack wisely, and get ready to explore the vibrant mosaic of landscapes and activities that make the Caribbean in April a truly unforgettable adventure.

Happy travels!

---

_References available upon request. Many insights were drawn from trusted sources including Lonely Planet, TravelPug, and various Caribbean-centric exploration sites, ensuring a well-rounded and practical guide for your vacation planning._



--- START OF FILE examples/research_bot/sample_outputs/product_recs.md ---

# Comprehensive Guide on Best Surfboards for Beginners: Transitioning, Features, and Budget Options

Surfing is not only a sport but a lifestyle that hooks its enthusiasts with the allure of riding waves and connecting with nature. For beginners, selecting the right surfboard is critical to safety, learning, and performance. This comprehensive guide has been crafted to walk through the essential aspects of choosing the ideal surfboard for beginners, especially those looking to transition from an 11-foot longboard to a shorter, more dynamic board. We discuss various board types, materials, design elements, and budget ranges, providing a detailed road map for both new surfers and those in the process of progression.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Board Types and Design Considerations](#board-types-and-design-considerations)
3. [Key Board Dimensions and Features](#key-board-dimensions-and-features)
4. [Materials: Soft-Top vs. Hard-Top Boards](#materials-soft-top-vs-hard-top-boards)
5. [Tips for Transitioning from Longboards to Shorter Boards](#tips-for-transitioning-from-longboards-to-shorter-boards)
6. [Budget and Pricing Options](#budget-and-pricing-options)
7. [Recommended Models and Buying Options](#recommended-models-and-buying-options)
8. [Conclusion](#conclusion)
9. [Follow-up Questions](#follow-up-questions)

---

## Introduction

Surfing is a dynamic sport that requires not only skill and technique but also the proper equipment. For beginners, the right surfboard can make the difference between a frustrating experience and one that builds confidence and enthusiasm. Many newcomers start with longboards due to their stability and ease of paddling; however, as skills develop, transitioning to a shorter board might be desirable for enhancing maneuverability and performance. This guide is designed for surfers who can already catch waves on an 11-foot board and are now considering stepping down to a more versatile option.

The overarching goal of this document is to help beginners identify which surfboard characteristics are most important, including board length, width, thickness, volume, and materials, while also considering factors like weight distribution, buoyancy, and control. We will also take a look at board types that are particularly welcoming for beginners and discuss gradual transitioning strategies.

---

## Board Types and Design Considerations

Choosing a board involves understanding the variety of designs available. Below are the main types of surfboards that cater to beginners and transitional surfers:

### Longboards and Mini-Mals

Longboards, typically 8 to 11 feet in length, provide ample stability, smoother paddling, and are well-suited for wave-catching. Their generous volume and width allow beginners to build confidence when standing up and riding waves. Mini-mal or mini-malibus (often around 8 to 9 feet) are a popular bridge between the longboard and the more agile shortboard, offering both stability and moderate maneuverability, which makes them excellent for gradual progress.

### Funboards and Hybrids

Funboards and hybrid boards blend the benefits of longboards and shortboards. They typically range from 6’6" to 8’0" in length, with extra volume and width that help preserve stability while introducing elements of sharper turning and improved agility. Hybrids are particularly helpful for surfers transitioning from longboards, as they maintain some of the buoyancy and ease of catching waves, yet offer a taste of the performance found in smaller boards.

### Shortboards

Shortboards emphasize performance, maneuverability, and a more responsive ride. However, they have less volume and require stronger paddling, quicker pop-up techniques, and more refined balance. For beginners, moving to a traditional shortboard immediately can be challenging. It is generally advised to make a gradual transition, potentially starting with a funboard or hybrid before making a direct leap to a performance shortboard.

---

## Key Board Dimensions and Features

When selecting a beginner surfboard, several key dimensions and features drastically affect performance, ease of learning, and safety:

### Length and Width

-   **Length**: Starting with an 8 to 9-foot board is ideal. Longer boards offer enhanced stability and improved paddling capabilities. Gradual downsizing is recommended if you plan to move from an 11-foot board.
-   **Width**: A board with a width over 20 inches provides greater stability and facilitates balance, especially vital for beginners.

### Thickness and Volume

-   **Thickness**: Typically around 2.5 to 3 inches. Thicker decks increase buoyancy, allowing the surfer to paddle easier while catching waves.
-   **Volume**: Measured in liters, volume is critical in understanding a board's flotation capacity. Higher volumes (e.g., 60-100 liters) are essential for beginners as they make the board more forgiving and stable. Suitable volumes might vary according to the surfer’s weight and experience level.

### Nose and Tail Shape

-   **Nose Shape**: A wide, rounded nose expands the board’s planing surface, which can help in catching waves sooner and maintaining stability as you ride.
-   **Tail Design**: Square or rounded tails are generally recommended as they enhance stability and allow for controlled turns, essential during the learning phase.

### Rocker

-   **Rocker**: This is the curvature of the board from nose to tail. For beginners, a minimal or relaxed rocker provides better stability and ease during paddling. A steeper rocker might be introduced progressively as the surfer’s skills improve.

---

## Materials: Soft-Top vs. Hard-Top Boards

The material composition of a surfboard is a crucial factor in determining its performance, durability, and safety. Beginners have two primary choices:

### Soft-Top (Foam) Boards

Soft-top boards are constructed almost entirely from foam. Their attributes include:

-   **Safety and Forgiveness**: The foam construction minimizes injury upon impact which is advantageous for beginners who might fall frequently.
-   **Stability and Buoyancy**: These boards typically offer greater buoyancy due to their softer material and thicker construction, easing the initial learning process.
-   **Maintenance**: They often require less maintenance—there is typically no need for waxing and they are more resistant to dings and scratches.

However, as a surfer’s skills progress, a soft-top might limit maneuverability and overall performance.

### Hard-Top Boards

Hard-tops, in contrast, offer a more traditional surfboard feel. They generally rely on a foam core encased in resin, with two prevalent combinations:

-   **PU (Polyurethane) Core with Polyester Resin**: This combination gives a classic feel and is relatively economical; however, these boards can be heavier and, as they age, more prone to damage.
-   **EPS (Expanded Polystyrene) Core with Epoxy Resin**: Lightweight and durable, EPS boards are often more buoyant and resistant to damage, although they usually carry a higher price tag and may be less forgiving.

Deciding between soft-top and hard-top boards often depends on a beginner’s progression goals, overall comfort, and budget constraints.

---

## Tips for Transitioning from Longboards to Shorter Boards

For surfers who have mastered the basics on an 11-foot board, the transition to a shorter board requires careful consideration, patience, and incremental changes. Here are some key tips:

### Gradual Downsizing

Experts recommend reducing the board length gradually—by about a foot at a time—to allow the body to adjust slowly to a board with less buoyancy and more responsiveness. This process helps maintain wave-catching ability and reduces the shock of transitioning to a very different board feel.

### Strengthening Core Skills

Before transitioning, make sure your surfing fundamentals are solid. Focus on practicing:

-   **Steep Take-offs**: Ensure that your pop-up is swift and robust to keep pace with shorter boards that demand a rapid transition from paddling to standing.
-   **Angling and Paddling Techniques**: Learn to angle your takeoffs properly to compensate for the lower buoyancy and increased maneuverability of shorter boards.

### Experimenting with Rentals or Borrowed Boards

If possible, try out a friend’s shorter board or rent one for a day to experience firsthand the differences in performance. This practical trial can provide valuable insights and inform your decision before making a purchase.

---

## Budget and Pricing Options

Surfboards are available across a range of prices to match different budgets. Whether you are looking for an affordable beginner board or a more expensive model that grows with your skills, it’s important to understand what features you can expect at different price points.

### Budget-Friendly Options

For those on a tight budget, several entry-level models offer excellent value. Examples include:

-   **Wavestorm 8' Classic Pinline Surfboard**: Priced affordably, this board is popular for its ease of use, ample volume, and forgiving nature. Despite its low cost, it delivers the stability needed to get started.
-   **Liquid Shredder EZ Slider Foamie**: A smaller board catering to younger or lighter surfers, this budget option provides easy paddling and a minimal risk of injury due to its soft construction.

### Moderate Price Range

As you move into the intermediate range, boards typically become slightly more specialized in their design, offering features such as improved stringer systems or versatile fin setups. These are excellent for surfers who wish to continue progressing their skills without compromising stability. Many surfboard packages from retailers also bundle a board with essential accessories like board bags, leashes, and wax for additional savings.

### Higher-End Models and Transitional Packages

For surfers looking for durability, performance, and advanced design features, investing in an EPS/epoxy board might be ideal. Although they come at a premium, these boards are lightweight, strong, and customizable with various fin configurations. Some options include boards from brands like South Bay Board Co. and ISLE, which combine high-quality construction with beginner-friendly features that help mediate the transition from longboard to shortboard performance.

---

## Recommended Models and Buying Options

Based on extensive research and community recommendations, here are some standout models and tips on where to buy:

### Recommended Models

-   **South Bay Board Co. 8'8" Heritage**: Combining foam and resin construction, this board is ideal for beginners who need stability and a forgiving surface. Its 86-liter volume suits both lightweight and somewhat heavier surfers.
-   **Rock-It 8' Big Softy**: With a high volume and an easy paddling profile, this board is designed for beginners, offering ample buoyancy to smooth out the learning curve.
-   **Wave Bandit EZ Rider Series**: Available in multiple lengths (7', 8', 9'), these boards offer versatility, with construction features that balance the stability of longboards and the agility required for shorter boards.
-   **Hybrid/Funboards Like the Poacher Funboard**: Perfect for transitioning surfers, these boards blend the ease of catching waves with the capability for more dynamic maneuvers.

### Buying Options

-   **Surf Shops and Local Retailers**: Traditional surf shops allow you to test different boards, which is ideal for assessing the board feel and condition—especially if you are considering a used board.
-   **Online Retailers and Marketplaces**: Websites like Evo, Surfboards Direct, and even local online marketplaces like Craigslist and Facebook Marketplace provide options that range from new to gently used boards. Always inspect reviews and verify seller policies before purchase.
-   **Package Deals and Bundles**: Many retailers offer bundled packages that include not just the board, but also essentials like a leash, wax, fins, and board bags. These packages can be more cost-effective and are great for beginners who need a complete surf kit.

---

## Conclusion

Selecting the right surfboard as a beginner is about balancing various factors: stability, buoyancy, maneuverability, and budget.

For those who have honed the basics using an 11-foot longboard, the transition to a shorter board should be gradual. Start by focusing on boards that preserve stability—such as funboards and hybrids—before moving to the more performance-oriented shortboards. Key characteristics like board length, width, thickness, volume, and material profoundly influence your surfing experience. Soft-top boards provide a forgiving entry point, while hard-top boards, especially those with EPS cores and epoxy resin, offer benefits for more advanced progression despite the increased learning curve.

Emphasizing fundamentals like proper pop-up technique and effective paddle work will ease the transition and ensure that the new board complements your evolving skills. Additionally, understanding the pricing spectrum—from budget-friendly models to premium options—allows you to make an informed purchase that suits both your financial and performance needs.

With a thoughtful approach to board selection, you can enhance your learning curve, enjoy safer sessions in the water, and ultimately develop the skills necessary to master the diverse challenges surfing presents. Whether your goal is to ride gentle waves or eventually experiment with sharper turns and dynamic maneuvers, choosing the right board is your first step towards a rewarding and sustainable surfing journey.

---

## Follow-up Questions

1. What is your current budget range for a new surfboard, or are you considering buying used?
2. How frequently do you plan to surf, and in what type of wave conditions?
3. Are you interested in a board that you can grow into as your skills progress, or do you prefer one that is more specialized for certain conditions?
4. Would you be interested in additional equipment bundles (like fins, leashes, boards bags) offered by local retailers or online shops?
5. Have you had the opportunity to test ride any boards before, and what feedback did you gather from that experience?

---

With this detailed guide, beginners should now have a comprehensive understanding of the surfboard market and the key factors influencing board performance, safety, and ease of progression. Happy surfing, and may you find the perfect board that rides the waves as beautifully as your passion for the sport!



--- START OF FILE examples/research_bot/sample_outputs/vacation.txt ---

# Terminal output for a vacation related query. See vacation.md for final report.

$ uv run python -m examples.research_bot.main
What would you like to research? Caribbean vacation spots in April, optimizing for surfing, hiking and water sports
View trace: https://platform.openai.com/traces/trace_....
Starting research...
✅ Will perform 15 searches
✅ Searching... 15/15 completed
✅ Finishing report...
✅ Report summary

This report provides an in-depth exploration of selected Caribbean vacation spots in April that are ideal for surfing, hiking, and water sports. Covering
destinations from Barbados and Puerto Rico to the Bahamas and Jamaica, it examines favorable weather conditions, recommended surf breaks, scenic hiking
trails, and various water sports activities. Detailed destination profiles, activity highlights, and travel tips are integrated to help travelers design a
multi-adventure itinerary in the Caribbean during April.


=====REPORT=====


Report: # Caribbean Adventure in April: Surfing, Hiking, and Water Sports Exploration

The Caribbean is renowned for its crystal-clear waters, vibrant culture, and diverse outdoor activities. April is an especially attractive month for visitors: warm temperatures, clear skies, and the promise of abundant activities. This report explores the best Caribbean destinations in April, with a focus on optimizing your vacation for surfing, hiking, and water sports.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Why April is the Perfect Time in the Caribbean](#why-april-is-the-perfect-time-in-the-caribbean)
3. [Surfing in the Caribbean](#surfing-in-the-caribbean)
    - 3.1 [Barbados: The Tale of Two Coasts](#barbados-the-tale-of-two-coasts)
    - 3.2 [Puerto Rico: Rincón and Beyond](#puerto-rico-rinc%C3%B3n-and-beyond)
    - 3.3 [Dominican Republic and Other Hotspots](#dominican-republic-and-other-hotspots)
4. [Hiking Adventures Across the Caribbean](#hiking-adventures-across-the-caribbean)
    - 4.1 [Trekking Through Tropical Rainforests](#trekking-through-tropical-rainforests)
    - 4.2 [Volcanic Peaks and Rugged Landscapes](#volcanic-peaks-and-rugged-landscapes)
5. [Diverse Water Sports Experiences](#diverse-water-sports-experiences)
    - 5.1 [Snorkeling, Diving, and Jet Skiing](#snorkeling-diving-and-jet-skiing)
    - 5.2 [Kiteboarding and Windsurfing](#kiteboarding-and-windsurfing)
6. [Combining Adventures: Multi-Activity Destinations](#combining-adventures-multi-activity-destinations)
7. [Practical Advice and Travel Tips](#practical-advice-and-travel-tips)
8. [Conclusion](#conclusion)

---

## Introduction

Caribbean vacations are much more than just beach relaxation; they offer adventure, exploration, and a lively cultural tapestry waiting to be discovered. For travelers seeking an adrenaline-filled getaway, April provides optimal conditions. This report synthesizes diverse research findings and travel insights to help you create an itinerary that combines the thrill of surfing, the challenge of hiking, and the excitement of water sports.

Whether you're standing on the edge of a powerful reef break or trekking through lush tropical landscapes, the Caribbean in April invites you to dive into nature, adventure, and culture. The following sections break down the best destinations and activities, ensuring that every aspect of your trip is meticulously planned for an unforgettable experience.

---

## Why April is the Perfect Time in the Caribbean

April stands at the crossroads of seasons in many Caribbean destinations. It marks the tail end of the dry season, ensuring:

- **Consistent Warm Temperatures:** Average daytime highs around 29°C (84°F) foster comfortable conditions for both land and water activities.
- **Pleasant Sea Temperatures:** With sea temperatures near 26°C (79°F), swimmers, surfers, and divers are treated to inviting waters.
- **Clear Skies and Minimal Rainfall:** Crisp, blue skies make for excellent visibility during snorkeling and diving, as well as clear panoramic views while hiking.
- **Festivals and Cultural Events:** Many islands host seasonal festivals such as Barbados' Fish Festival and Antigua's Sailing Week, adding a cultural layer to your vacation.

These factors create an ideal backdrop for balancing your outdoor pursuits, whether you’re catching epic waves, trekking rugged trails, or partaking in water sports.

---

## Surfing in the Caribbean

Surfing in the Caribbean offers diverse wave experiences, ranging from gentle, beginner-friendly rollers to powerful reef breaks that challenge even seasoned surfers. April, in particular, provides excellent conditions for those looking to ride its picturesque waves.

### Barbados: The Tale of Two Coasts

Barbados is a prime destination:

- **Soup Bowl in Bathsheba:** On the east coast, the Soup Bowl is famous for its consistent, powerful waves. This spot attracts experienced surfers who appreciate its challenging right-hand reef break with steep drops, providing the kind of performance wave rarely found elsewhere.
- **Freights Bay:** On the south coast, visitors find more forgiving, gentle wave conditions. Ideal for beginners and longboarders, this spot offers the perfect balance for those still mastering their craft.

Barbados not only excels in its surfing credentials but also complements the experience with a rich local culture and events in April, making it a well-rounded destination.

### Puerto Rico: Rincón and Beyond

Rincón in Puerto Rico is hailed as the Caribbean’s surfing capital:

- **Diverse Breaks:** With spots ranging from challenging reef breaks such as Tres Palmas and Dogman's to more inviting waves at Domes and Maria's, Puerto Rico offers a spectrum for all surfing skill levels.
- **Local Culture:** Aside from its surf culture, the island boasts vibrant local food scenes, historic sites, and exciting nightlife, enriching your overall travel experience.

In addition, Puerto Rico’s coasts often feature opportunities for hiking and other outdoor adventures, making it an attractive option for multi-activity travelers.

### Dominican Republic and Other Hotspots

Other islands such as the Dominican Republic, with Playa Encuentro on its north coast, provide consistent surf year-round. Highlights include:

- **Playa Encuentro:** A hotspot known for its dependable breaks, ideal for both intermediate and advanced surfers during the cooler months of October to April.
- **Jamaica and The Bahamas:** Jamaica’s Boston Bay offers a mix of beginner and intermediate waves, and The Bahamas’ Surfer’s Beach on Eleuthera draws parallels to the legendary surf spots of Hawaii, especially during the winter months.

These destinations not only spotlight surfing but also serve as gateways to additional outdoor activities, ensuring there's never a dull moment whether you're balancing waves with hikes or cultural exploration.

---

## Hiking Adventures Across the Caribbean

The Caribbean's topography is as varied as it is beautiful. Its network of hiking trails traverses volcanic peaks, ancient rainforests, and dramatic coastal cliffs, offering breathtaking vistas to intrepid explorers.

### Trekking Through Tropical Rainforests

For nature enthusiasts, the lush forests of the Caribbean present an immersive encounter with biodiversity:

- **El Yunque National Forest, Puerto Rico:** The only tropical rainforest within the U.S. National Forest System, El Yunque is rich in endemic species such as the Puerto Rican parrot and the famous coquí frog. Trails like the El Yunque Peak Trail and La Mina Falls Trail provide both challenging hikes and scenic rewards.
- **Virgin Islands National Park, St. John:** With over 20 well-defined trails, this park offers hikes that reveal historical petroglyphs, colonial ruins, and stunning coastal views along the Reef Bay Trail.

### Volcanic Peaks and Rugged Landscapes

For those seeking more rugged challenges, several destinations offer unforgettable adventures:

- **Morne Trois Pitons National Park, Dominica:** A UNESCO World Heritage Site showcasing volcanic landscapes, hot springs, the famed Boiling Lake, and lush trails that lead to hidden waterfalls.
- **Gros Piton, Saint Lucia:** The iconic hike up Gros Piton provides a moderately challenging trek that ends with panoramic views of the Caribbean Sea, a truly rewarding experience for hikers.
- **La Soufrière, St. Vincent:** This active volcano not only offers a dynamic hiking environment but also the opportunity to observe the ongoing geological transformations up close.

Other noteworthy hiking spots include the Blue Mountains in Jamaica for coffee plantation tours and expansive views, as well as trails in Martinique around Montagne Pelée, which combine historical context with natural beauty.

---

## Diverse Water Sports Experiences

While surfing and hiking attract a broad range of adventurers, the Caribbean also scores high on other water sports. Whether you're drawn to snorkeling, jet skiing, or wind- and kiteboarding, the islands offer a plethora of aquatic activities.

### Snorkeling, Diving, and Jet Skiing

Caribbean waters teem with life and color, making them ideal for underwater exploration:

- **Bonaire:** Its protected marine parks serve as a magnet for divers and snorkelers. With vibrant coral reefs and diverse marine species, Bonaire is a top destination for those who appreciate the underwater world.
- **Cayman Islands:** Unique attractions such as Stingray City provide opportunities to interact with friendly stingrays in clear, calm waters. Additionally, the Underwater Sculpture Park is an innovative blend of art and nature.
- **The Bahamas:** In places like Eleuthera, excursions often cater to families and thrill-seekers alike. Options include jet ski rentals, where groups can explore hidden beaches and pristine coves while enjoying the vibrant marine life.

### Kiteboarding and Windsurfing

Harnessing the steady trade winds and warm Caribbean waters, several islands have become hubs for kiteboarding and windsurfing:

- **Aruba:** Known as "One Happy Island," Aruba’s Fisherman's Huts area provides consistent winds, perfect for enthusiasts of windsurfing and kiteboarding alike.
- **Cabarete, Dominican Republic and Silver Rock, Barbados:** Both destinations benefit from reliable trade winds, making them popular among kitesurfers. These spots often combine water sports with a lively beach culture, ensuring that the fun continues on land as well.

Local operators provide equipment rental and lessons, ensuring that even first-time adventurers can safely and confidently enjoy these exciting sports.

---

## Combining Adventures: Multi-Activity Destinations

For travelers seeking a comprehensive vacation where surfing, hiking, and water sports converge, several Caribbean destinations offer the best of all worlds.

- **Puerto Rico:** With its robust surf scene in Rincón, world-class hiking in El Yunque, and opportunities for snorkeling and jet skiing in San Juan Bay, Puerto Rico is a true multi-adventure destination.
- **Barbados:** In addition to the surf breaks along its coasts, Barbados offers a mix of cultural events, local cuisine, and even hiking excursions to scenic rural areas, making for a well-rounded experience.
- **Dominican Republic and Jamaica:** Both are renowned not only for their consistent surf conditions but also for expansive hiking trails and water sports. From the rugged landscapes of the Dominican Republic to Jamaica’s blend of cultural history and natural exploration, these islands allow travelers to mix and match activities seamlessly.

Group tours and local guides further enhance these experiences, providing insider tips, safe excursions, and personalized itineraries that cater to multiple interests within one trip.

---

## Practical Advice and Travel Tips

### Weather and Timing

- **Optimal Climate:** April offers ideal weather conditions across the Caribbean. With minimal rainfall and warm temperatures, it is a great time to schedule outdoor activities.
- **Surfing Seasons:** While April marks the end of the prime surf season in some areas (like Rincón in Puerto Rico), many destinations maintain consistent conditions during this month.

### Booking and Costs

- **Surfing Lessons:** Expect to pay between $40 and $110 per session depending on the location. For instance, Puerto Rico typically charges around $75 for beginner lessons, while group lessons in the Dominican Republic average approximately $95.
- **Equipment Rentals:** Pricing for jet ski, surfboard, and snorkeling equipment may vary. In the Bahamas, an hour-long jet ski tour might cost about $120 per group, whereas a similar experience might be available at a lower cost in other regions.
- **Accommodations:** Prices also vary by island. Many travelers find that even affordable stays do not skimp on amenities, allowing you to invest more in guided excursions and local experiences.

### Cultural Considerations

- **Festivals and Events:** Check local event calendars. Destinations like Barbados and Antigua host festivals in April that combine cultural heritage with festive outdoor activities.
- **Local Cuisine:** Incorporate food tours into your itinerary. Caribbean cuisine—with its fusion of flavors—can be as adventurous as the outdoor activities.

### Health and Safety

- **Staying Hydrated:** The warm temperatures demand that you stay properly hydrated. Always carry water, especially during long hikes.
- **Sun Protection:** Use sunscreen, hats, and sunglasses to protect yourself during extended periods outdoors on both land and water.
- **Local Guides:** Utilize local tour operators for both hiking and water sports. Their expertise not only enriches your experience but also ensures safety in unfamiliar terrain or water bodies.

---

## Conclusion

The Caribbean in April is a haven for adventure seekers. With its pristine beaches, diverse ecosystems, and rich cultural tapestry, it offers something for every type of traveler. Whether you're chasing the perfect wave along the shores of Barbados and Puerto Rico, trekking through the lush landscapes of El Yunque or Morne Trois Pitons, or engaging in an array of water sports from snorkeling to kiteboarding, your ideal vacation is only a booking away.

This report has outlined the best destinations and provided practical advice to optimize your vacation for surfing, hiking, and water sports. By considering the diverse offerings—from epic surf breaks and challenging hiking trails to vibrant water sports—the Caribbean stands out as a multi-adventure destination where every day brings a new experience.

Plan carefully, pack wisely, and get ready to explore the vibrant mosaic of landscapes and activities that make the Caribbean in April a truly unforgettable adventure.

Happy travels!

---

*References available upon request. Many insights were drawn from trusted sources including Lonely Planet, TravelPug, and various Caribbean-centric exploration sites, ensuring a well-rounded and practical guide for your vacation planning.*



=====FOLLOW UP QUESTIONS=====


Follow up questions: Would you like detailed profiles for any of the highlighted destinations (e.g., Puerto Rico or Barbados)?
Are you interested in more information about booking details and local tour operators in specific islands?
Do you need guidance on combining cultural events with outdoor adventures during your Caribbean vacation?


--- START OF FILE examples/research_bot/sample_outputs/product_recs.txt ---

# Terminal output for a product recommendation related query. See product_recs.md for final report.

$ uv run python -m examples.research_bot.main

What would you like to research? Best surfboards for beginners. I can catch my own waves, but previously used an 11ft board. What should I look for, what are my options? Various budget ranges.
View trace: https://platform.openai.com/traces/trace_...
Starting research...
✅ Will perform 15 searches
✅ Searching... 15/15 completed
✅ Finishing report...
✅ Report summary

This report provides a detailed guide on selecting the best surfboards for beginners, especially for those transitioning from an 11-foot longboard to a
shorter board. It covers design considerations such as board dimensions, shape, materials, and volume, while comparing soft-top and hard-top boards. In
addition, the report discusses various budget ranges, recommended board models, buying options (both new and used), and techniques to ease the transition to
more maneuverable boards. By understanding these factors, beginner surfers can select a board that not only enhances their skills but also suits their
individual needs.


=====REPORT=====


Report: # Comprehensive Guide on Best Surfboards for Beginners: Transitioning, Features, and Budget Options

Surfing is not only a sport but a lifestyle that hooks its enthusiasts with the allure of riding waves and connecting with nature. For beginners, selecting the right surfboard is critical to safety, learning, and performance. This comprehensive guide has been crafted to walk through the essential aspects of choosing the ideal surfboard for beginners, especially those looking to transition from an 11-foot longboard to a shorter, more dynamic board. We discuss various board types, materials, design elements, and budget ranges, providing a detailed road map for both new surfers and those in the process of progression.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Board Types and Design Considerations](#board-types-and-design-considerations)
3. [Key Board Dimensions and Features](#key-board-dimensions-and-features)
4. [Materials: Soft-Top vs. Hard-Top Boards](#materials-soft-top-vs-hard-top-boards)
5. [Tips for Transitioning from Longboards to Shorter Boards](#tips-for-transitioning-from-longboards-to-shorter-boards)
6. [Budget and Pricing Options](#budget-and-pricing-options)
7. [Recommended Models and Buying Options](#recommended-models-and-buying-options)
8. [Conclusion](#conclusion)
9. [Follow-up Questions](#follow-up-questions)

---

## Introduction

Surfing is a dynamic sport that requires not only skill and technique but also the proper equipment. For beginners, the right surfboard can make the difference between a frustrating experience and one that builds confidence and enthusiasm. Many newcomers start with longboards due to their stability and ease of paddling; however, as skills develop, transitioning to a shorter board might be desirable for enhancing maneuverability and performance. This guide is designed for surfers who can already catch waves on an 11-foot board and are now considering stepping down to a more versatile option.

The overarching goal of this document is to help beginners identify which surfboard characteristics are most important, including board length, width, thickness, volume, and materials, while also considering factors like weight distribution, buoyancy, and control. We will also take a look at board types that are particularly welcoming for beginners and discuss gradual transitioning strategies.

---

## Board Types and Design Considerations

Choosing a board involves understanding the variety of designs available. Below are the main types of surfboards that cater to beginners and transitional surfers:

### Longboards and Mini-Mals

Longboards, typically 8 to 11 feet in length, provide ample stability, smoother paddling, and are well-suited for wave-catching. Their generous volume and width allow beginners to build confidence when standing up and riding waves. Mini-mal or mini-malibus (often around 8 to 9 feet) are a popular bridge between the longboard and the more agile shortboard, offering both stability and moderate maneuverability, which makes them excellent for gradual progress.

### Funboards and Hybrids

Funboards and hybrid boards blend the benefits of longboards and shortboards. They typically range from 6’6" to 8’0" in length, with extra volume and width that help preserve stability while introducing elements of sharper turning and improved agility. Hybrids are particularly helpful for surfers transitioning from longboards, as they maintain some of the buoyancy and ease of catching waves, yet offer a taste of the performance found in smaller boards.

### Shortboards

Shortboards emphasize performance, maneuverability, and a more responsive ride. However, they have less volume and require stronger paddling, quicker pop-up techniques, and more refined balance. For beginners, moving to a traditional shortboard immediately can be challenging. It is generally advised to make a gradual transition, potentially starting with a funboard or hybrid before making a direct leap to a performance shortboard.

---

## Key Board Dimensions and Features

When selecting a beginner surfboard, several key dimensions and features drastically affect performance, ease of learning, and safety:

### Length and Width

- **Length**: Starting with an 8 to 9-foot board is ideal. Longer boards offer enhanced stability and improved paddling capabilities. Gradual downsizing is recommended if you plan to move from an 11-foot board.
- **Width**: A board with a width over 20 inches provides greater stability and facilitates balance, especially vital for beginners.

### Thickness and Volume

- **Thickness**: Typically around 2.5 to 3 inches. Thicker decks increase buoyancy, allowing the surfer to paddle easier while catching waves.
- **Volume**: Measured in liters, volume is critical in understanding a board's flotation capacity. Higher volumes (e.g., 60-100 liters) are essential for beginners as they make the board more forgiving and stable. Suitable volumes might vary according to the surfer’s weight and experience level.

### Nose and Tail Shape

- **Nose Shape**: A wide, rounded nose expands the board’s planing surface, which can help in catching waves sooner and maintaining stability as you ride.
- **Tail Design**: Square or rounded tails are generally recommended as they enhance stability and allow for controlled turns, essential during the learning phase.

### Rocker

- **Rocker**: This is the curvature of the board from nose to tail. For beginners, a minimal or relaxed rocker provides better stability and ease during paddling. A steeper rocker might be introduced progressively as the surfer’s skills improve.

---

## Materials: Soft-Top vs. Hard-Top Boards

The material composition of a surfboard is a crucial factor in determining its performance, durability, and safety. Beginners have two primary choices:

### Soft-Top (Foam) Boards

Soft-top boards are constructed almost entirely from foam. Their attributes include:

- **Safety and Forgiveness**: The foam construction minimizes injury upon impact which is advantageous for beginners who might fall frequently.
- **Stability and Buoyancy**: These boards typically offer greater buoyancy due to their softer material and thicker construction, easing the initial learning process.
- **Maintenance**: They often require less maintenance—there is typically no need for waxing and they are more resistant to dings and scratches.

However, as a surfer’s skills progress, a soft-top might limit maneuverability and overall performance.

### Hard-Top Boards

Hard-tops, in contrast, offer a more traditional surfboard feel. They generally rely on a foam core encased in resin, with two prevalent combinations:

- **PU (Polyurethane) Core with Polyester Resin**: This combination gives a classic feel and is relatively economical; however, these boards can be heavier and, as they age, more prone to damage.
- **EPS (Expanded Polystyrene) Core with Epoxy Resin**: Lightweight and durable, EPS boards are often more buoyant and resistant to damage, although they usually carry a higher price tag and may be less forgiving.

Deciding between soft-top and hard-top boards often depends on a beginner’s progression goals, overall comfort, and budget constraints.

---

## Tips for Transitioning from Longboards to Shorter Boards

For surfers who have mastered the basics on an 11-foot board, the transition to a shorter board requires careful consideration, patience, and incremental changes. Here are some key tips:

### Gradual Downsizing

Experts recommend reducing the board length gradually—by about a foot at a time—to allow the body to adjust slowly to a board with less buoyancy and more responsiveness. This process helps maintain wave-catching ability and reduces the shock of transitioning to a very different board feel.

### Strengthening Core Skills

Before transitioning, make sure your surfing fundamentals are solid. Focus on practicing:

- **Steep Take-offs**: Ensure that your pop-up is swift and robust to keep pace with shorter boards that demand a rapid transition from paddling to standing.
- **Angling and Paddling Techniques**: Learn to angle your takeoffs properly to compensate for the lower buoyancy and increased maneuverability of shorter boards.

### Experimenting with Rentals or Borrowed Boards

If possible, try out a friend’s shorter board or rent one for a day to experience firsthand the differences in performance. This practical trial can provide valuable insights and inform your decision before making a purchase.

---

## Budget and Pricing Options

Surfboards are available across a range of prices to match different budgets. Whether you are looking for an affordable beginner board or a more expensive model that grows with your skills, it’s important to understand what features you can expect at different price points.

### Budget-Friendly Options

For those on a tight budget, several entry-level models offer excellent value. Examples include:

- **Wavestorm 8' Classic Pinline Surfboard**: Priced affordably, this board is popular for its ease of use, ample volume, and forgiving nature. Despite its low cost, it delivers the stability needed to get started.
- **Liquid Shredder EZ Slider Foamie**: A smaller board catering to younger or lighter surfers, this budget option provides easy paddling and a minimal risk of injury due to its soft construction.

### Moderate Price Range

As you move into the intermediate range, boards typically become slightly more specialized in their design, offering features such as improved stringer systems or versatile fin setups. These are excellent for surfers who wish to continue progressing their skills without compromising stability. Many surfboard packages from retailers also bundle a board with essential accessories like board bags, leashes, and wax for additional savings.

### Higher-End Models and Transitional Packages

For surfers looking for durability, performance, and advanced design features, investing in an EPS/epoxy board might be ideal. Although they come at a premium, these boards are lightweight, strong, and customizable with various fin configurations. Some options include boards from brands like South Bay Board Co. and ISLE, which combine high-quality construction with beginner-friendly features that help mediate the transition from longboard to shortboard performance.

---

## Recommended Models and Buying Options

Based on extensive research and community recommendations, here are some standout models and tips on where to buy:

### Recommended Models

- **South Bay Board Co. 8'8" Heritage**: Combining foam and resin construction, this board is ideal for beginners who need stability and a forgiving surface. Its 86-liter volume suits both lightweight and somewhat heavier surfers.
- **Rock-It 8' Big Softy**: With a high volume and an easy paddling profile, this board is designed for beginners, offering ample buoyancy to smooth out the learning curve.
- **Wave Bandit EZ Rider Series**: Available in multiple lengths (7', 8', 9'), these boards offer versatility, with construction features that balance the stability of longboards and the agility required for shorter boards.
- **Hybrid/Funboards Like the Poacher Funboard**: Perfect for transitioning surfers, these boards blend the ease of catching waves with the capability for more dynamic maneuvers.

### Buying Options

- **Surf Shops and Local Retailers**: Traditional surf shops allow you to test different boards, which is ideal for assessing the board feel and condition—especially if you are considering a used board.
- **Online Retailers and Marketplaces**: Websites like Evo, Surfboards Direct, and even local online marketplaces like Craigslist and Facebook Marketplace provide options that range from new to gently used boards. Always inspect reviews and verify seller policies before purchase.
- **Package Deals and Bundles**: Many retailers offer bundled packages that include not just the board, but also essentials like a leash, wax, fins, and board bags. These packages can be more cost-effective and are great for beginners who need a complete surf kit.

---

## Conclusion

Selecting the right surfboard as a beginner is about balancing various factors: stability, buoyancy, maneuverability, and budget.

For those who have honed the basics using an 11-foot longboard, the transition to a shorter board should be gradual. Start by focusing on boards that preserve stability—such as funboards and hybrids—before moving to the more performance-oriented shortboards. Key characteristics like board length, width, thickness, volume, and material profoundly influence your surfing experience. Soft-top boards provide a forgiving entry point, while hard-top boards, especially those with EPS cores and epoxy resin, offer benefits for more advanced progression despite the increased learning curve.

Emphasizing fundamentals like proper pop-up technique and effective paddle work will ease the transition and ensure that the new board complements your evolving skills. Additionally, understanding the pricing spectrum—from budget-friendly models to premium options—allows you to make an informed purchase that suits both your financial and performance needs.

With a thoughtful approach to board selection, you can enhance your learning curve, enjoy safer sessions in the water, and ultimately develop the skills necessary to master the diverse challenges surfing presents. Whether your goal is to ride gentle waves or eventually experiment with sharper turns and dynamic maneuvers, choosing the right board is your first step towards a rewarding and sustainable surfing journey.

---

## Follow-up Questions

1. What is your current budget range for a new surfboard, or are you considering buying used?
2. How frequently do you plan to surf, and in what type of wave conditions?
3. Are you interested in a board that you can grow into as your skills progress, or do you prefer one that is more specialized for certain conditions?
4. Would you be interested in additional equipment bundles (like fins, leashes, boards bags) offered by local retailers or online shops?
5. Have you had the opportunity to test ride any boards before, and what feedback did you gather from that experience?

---

With this detailed guide, beginners should now have a comprehensive understanding of the surfboard market and the key factors influencing board performance, safety, and ease of progression. Happy surfing, and may you find the perfect board that rides the waves as beautifully as your passion for the sport!


=====FOLLOW UP QUESTIONS=====


Follow up questions: What is your current budget range for a new surfboard, or are you considering a used board?
What types of waves do you typically surf, and how might that affect your board choice?
Would you be interested in a transitional board that grows with your skills, or are you looking for a more specialized design?
Have you had experience with renting or borrowing boards to try different sizes before making a purchase?
Do you require additional equipment bundles (like fins, leash, or wax), or do you already have those?



--- START OF FILE examples/agent_patterns/deterministic.py ---

import asyncio

from pydantic import BaseModel

from agents import Agent, Runner, trace

"""
This example demonstrates a deterministic flow, where each step is performed by an agent.
1. The first agent generates a story outline
2. We feed the outline into the second agent
3. The second agent checks if the outline is good quality and if it is a scifi story
4. If the outline is not good quality or not a scifi story, we stop here
5. If the outline is good quality and a scifi story, we feed the outline into the third agent
6. The third agent writes the story
"""

story_outline_agent = Agent(
    name="story_outline_agent",
    instructions="Generate a very short story outline based on the user's input.",
)


class OutlineCheckerOutput(BaseModel):
    good_quality: bool
    is_scifi: bool


outline_checker_agent = Agent(
    name="outline_checker_agent",
    instructions="Read the given story outline, and judge the quality. Also, determine if it is a scifi story.",
    output_type=OutlineCheckerOutput,
)

story_agent = Agent(
    name="story_agent",
    instructions="Write a short story based on the given outline.",
    output_type=str,
)


async def main():
    input_prompt = input("What kind of story do you want? ")

    # Ensure the entire workflow is a single trace
    with trace("Deterministic story flow"):
        # 1. Generate an outline
        outline_result = await Runner.run(
            story_outline_agent,
            input_prompt,
        )
        print("Outline generated")

        # 2. Check the outline
        outline_checker_result = await Runner.run(
            outline_checker_agent,
            outline_result.final_output,
        )

        # 3. Add a gate to stop if the outline is not good quality or not a scifi story
        assert isinstance(outline_checker_result.final_output, OutlineCheckerOutput)
        if not outline_checker_result.final_output.good_quality:
            print("Outline is not good quality, so we stop here.")
            exit(0)

        if not outline_checker_result.final_output.is_scifi:
            print("Outline is not a scifi story, so we stop here.")
            exit(0)

        print("Outline is good quality and a scifi story, so we continue to write the story.")

        # 4. Write the story
        story_result = await Runner.run(
            story_agent,
            outline_result.final_output,
        )
        print(f"Story: {story_result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/agent_patterns/input_guardrails.py ---

from __future__ import annotations

import asyncio

from pydantic import BaseModel

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)

"""
This example shows how to use guardrails.

Guardrails are checks that run in parallel to the agent's execution.
They can be used to do things like:
- Check if input messages are off-topic
- Check that output messages don't violate any policies
- Take over control of the agent's execution if an unexpected input is detected

In this example, we'll setup an input guardrail that trips if the user is asking to do math homework.
If the guardrail trips, we'll respond with a refusal message.
"""


### 1. An agent-based guardrail that is triggered if the user is asking to do math homework
class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str


guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
)


@input_guardrail
async def math_guardrail(
    context: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """This is an input guardrail function, which happens to call an agent to check if the input
    is a math homework question.
    """
    result = await Runner.run(guardrail_agent, input, context=context.context)
    final_output = result.final_output_as(MathHomeworkOutput)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_math_homework,
    )


### 2. The run loop


async def main():
    agent = Agent(
        name="Customer support agent",
        instructions="You are a customer support agent. You help customers with their questions.",
        input_guardrails=[math_guardrail],
    )

    input_data: list[TResponseInputItem] = []

    while True:
        user_input = input("Enter a message: ")
        input_data.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        try:
            result = await Runner.run(agent, input_data)
            print(result.final_output)
            # If the guardrail didn't trigger, we use the result as the input for the next run
            input_data = result.to_input_list()
        except InputGuardrailTripwireTriggered:
            # If the guardrail triggered, we instead add a refusal message to the input
            message = "Sorry, I can't help you with your math homework."
            print(message)
            input_data.append(
                {
                    "role": "assistant",
                    "content": message,
                }
            )

    # Sample run:
    # Enter a message: What's the capital of California?
    # The capital of California is Sacramento.
    # Enter a message: Can you help me solve for x: 2x + 5 = 11
    # Sorry, I can't help you with your math homework.


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/agent_patterns/agents_as_tools.py ---

import asyncio

from agents import Agent, ItemHelpers, MessageOutputItem, Runner, trace

"""
This example shows the agents-as-tools pattern. The frontline agent receives a user message and
then picks which agents to call, as tools. In this case, it picks from a set of translation
agents.
"""

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    handoff_description="An english to spanish translator",
)

french_agent = Agent(
    name="french_agent",
    instructions="You translate the user's message to French",
    handoff_description="An english to french translator",
)

italian_agent = Agent(
    name="italian_agent",
    instructions="You translate the user's message to Italian",
    handoff_description="An english to italian translator",
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools in order."
        "You never translate on your own, you always use the provided tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="Translate the user's message to Italian",
        ),
    ],
)

synthesizer_agent = Agent(
    name="synthesizer_agent",
    instructions="You inspect translations, correct them if needed, and produce a final concatenated response.",
)


async def main():
    msg = input("Hi! What would you like translated, and to which languages? ")

    # Run the entire orchestration in a single trace
    with trace("Orchestrator evaluator"):
        orchestrator_result = await Runner.run(orchestrator_agent, msg)

        for item in orchestrator_result.new_items:
            if isinstance(item, MessageOutputItem):
                text = ItemHelpers.text_message_output(item)
                if text:
                    print(f"  - Translation step: {text}")

        synthesizer_result = await Runner.run(
            synthesizer_agent, orchestrator_result.to_input_list()
        )

    print(f"\n\nFinal response:\n{synthesizer_result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/agent_patterns/output_guardrails.py ---

from __future__ import annotations

import asyncio
import json

from pydantic import BaseModel, Field

from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
)

"""
This example shows how to use output guardrails.

Output guardrails are checks that run on the final output of an agent.
They can be used to do things like:
- Check if the output contains sensitive data
- Check if the output is a valid response to the user's message

In this example, we'll use a (contrived) example where we check if the agent's response contains
a phone number.
"""


# The agent's output type
class MessageOutput(BaseModel):
    reasoning: str = Field(description="Thoughts on how to respond to the user's message")
    response: str = Field(description="The response to the user's message")
    user_name: str | None = Field(description="The name of the user who sent the message, if known")


@output_guardrail
async def sensitive_data_check(
    context: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    phone_number_in_response = "650" in output.response
    phone_number_in_reasoning = "650" in output.reasoning

    return GuardrailFunctionOutput(
        output_info={
            "phone_number_in_response": phone_number_in_response,
            "phone_number_in_reasoning": phone_number_in_reasoning,
        },
        tripwire_triggered=phone_number_in_response or phone_number_in_reasoning,
    )


agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    output_type=MessageOutput,
    output_guardrails=[sensitive_data_check],
)


async def main():
    # This should be ok
    await Runner.run(agent, "What's the capital of California?")
    print("First message passed")

    # This should trip the guardrail
    try:
        result = await Runner.run(
            agent, "My phone number is 650-123-4567. Where do you think I live?"
        )
        print(
            f"Guardrail didn't trip - this is unexpected. Output: {json.dumps(result.final_output.model_dump(), indent=2)}"
        )

    except OutputGuardrailTripwireTriggered as e:
        print(f"Guardrail tripped. Info: {e.guardrail_result.output.output_info}")


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/agent_patterns/README.md ---

# Common agentic patterns

This folder contains examples of different common patterns for agents.

## Deterministic flows

A common tactic is to break down a task into a series of smaller steps. Each task can be performed by an agent, and the output of one agent is used as input to the next. For example, if your task was to generate a story, you could break it down into the following steps:

1. Generate an outline
2. Generate the story
3. Generate the ending

Each of these steps can be performed by an agent. The output of one agent is used as input to the next.

See the [`deterministic.py`](./deterministic.py) file for an example of this.

## Handoffs and routing

In many situations, you have specialized sub-agents that handle specific tasks. You can use handoffs to route the task to the right agent.

For example, you might have a frontline agent that receives a request, and then hands off to a specialized agent based on the language of the request.
See the [`routing.py`](./routing.py) file for an example of this.

## Agents as tools

The mental model for handoffs is that the new agent "takes over". It sees the previous conversation history, and owns the conversation from that point onwards. However, this is not the only way to use agents. You can also use agents as a tool - the tool agent goes off and runs on its own, and then returns the result to the original agent.

For example, you could model the translation task above as tool calls instead: rather than handing over to the language-specific agent, you could call the agent as a tool, and then use the result in the next step. This enables things like translating multiple languages at once.

See the [`agents_as_tools.py`](./agents_as_tools.py) file for an example of this.

## LLM-as-a-judge

LLMs can often improve the quality of their output if given feedback. A common pattern is to generate a response using a model, and then use a second model to provide feedback. You can even use a small model for the initial generation and a larger model for the feedback, to optimize cost.

For example, you could use an LLM to generate an outline for a story, and then use a second LLM to evaluate the outline and provide feedback. You can then use the feedback to improve the outline, and repeat until the LLM is satisfied with the outline.

See the [`llm_as_a_judge.py`](./llm_as_a_judge.py) file for an example of this.

## Parallelization

Running multiple agents in parallel is a common pattern. This can be useful for both latency (e.g. if you have multiple steps that don't depend on each other) and also for other reasons e.g. generating multiple responses and picking the best one.

See the [`parallelization.py`](./parallelization.py) file for an example of this. It runs a translation agent multiple times in parallel, and then picks the best translation.

## Guardrails

Related to parallelization, you often want to run input guardrails to make sure the inputs to your agents are valid. For example, if you have a customer support agent, you might want to make sure that the user isn't trying to ask for help with a math problem.

You can definitely do this without any special Agents SDK features by using parallelization, but we support a special guardrail primitive. Guardrails can have a "tripwire" - if the tripwire is triggered, the agent execution will immediately stop and a `GuardrailTripwireTriggered` exception will be raised.

This is really useful for latency: for example, you might have a very fast model that runs the guardrail and a slow model that runs the actual agent. You wouldn't want to wait for the slow model to finish, so guardrails let you quickly reject invalid inputs.

See the [`input_guardrails.py`](./input_guardrails.py) and [`output_guardrails.py`](./output_guardrails.py) files for examples.



--- START OF FILE examples/agent_patterns/parallelization.py ---

import asyncio

from agents import Agent, ItemHelpers, Runner, trace

"""
This example shows the parallelization pattern. We run the agent three times in parallel, and pick
the best result.
"""

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
)

translation_picker = Agent(
    name="translation_picker",
    instructions="You pick the best Spanish translation from the given options.",
)


async def main():
    msg = input("Hi! Enter a message, and we'll translate it to Spanish.\n\n")

    # Ensure the entire workflow is a single trace
    with trace("Parallel translation"):
        res_1, res_2, res_3 = await asyncio.gather(
            Runner.run(
                spanish_agent,
                msg,
            ),
            Runner.run(
                spanish_agent,
                msg,
            ),
            Runner.run(
                spanish_agent,
                msg,
            ),
        )

        outputs = [
            ItemHelpers.text_message_outputs(res_1.new_items),
            ItemHelpers.text_message_outputs(res_2.new_items),
            ItemHelpers.text_message_outputs(res_3.new_items),
        ]

        translations = "\n\n".join(outputs)
        print(f"\n\nTranslations:\n\n{translations}")

        best_translation = await Runner.run(
            translation_picker,
            f"Input: {msg}\n\nTranslations:\n{translations}",
        )

    print("\n\n-----")

    print(f"Best translation: {best_translation.final_output}")


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/agent_patterns/routing.py ---

import asyncio
import uuid

from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent

from agents import Agent, RawResponsesStreamEvent, Runner, TResponseInputItem, trace

"""
This example shows the handoffs/routing pattern. The triage agent receives the first message, and
then hands off to the appropriate agent based on the language of the request. Responses are
streamed to the user.
"""

french_agent = Agent(
    name="french_agent",
    instructions="You only speak French",
)

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You only speak Spanish",
)

english_agent = Agent(
    name="english_agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="triage_agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[french_agent, spanish_agent, english_agent],
)


async def main():
    # We'll create an ID for this conversation, so we can link each trace
    conversation_id = str(uuid.uuid4().hex[:16])

    msg = input("Hi! We speak French, Spanish and English. How can I help? ")
    agent = triage_agent
    inputs: list[TResponseInputItem] = [{"content": msg, "role": "user"}]

    while True:
        # Each conversation turn is a single trace. Normally, each input from the user would be an
        # API request to your app, and you can wrap the request in a trace()
        with trace("Routing example", group_id=conversation_id):
            result = Runner.run_streamed(
                agent,
                input=inputs,
            )
            async for event in result.stream_events():
                if not isinstance(event, RawResponsesStreamEvent):
                    continue
                data = event.data
                if isinstance(data, ResponseTextDeltaEvent):
                    print(data.delta, end="", flush=True)
                elif isinstance(data, ResponseContentPartDoneEvent):
                    print("\n")

        inputs = result.to_input_list()
        print("\n")

        user_msg = input("Enter a message: ")
        inputs.append({"content": user_msg, "role": "user"})
        agent = result.current_agent


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/agent_patterns/llm_as_a_judge.py ---

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Literal

from agents import Agent, ItemHelpers, Runner, TResponseInputItem, trace

"""
This example shows the LLM as a judge pattern. The first agent generates an outline for a story.
The second agent judges the outline and provides feedback. We loop until the judge is satisfied
with the outline.
"""

story_outline_generator = Agent(
    name="story_outline_generator",
    instructions=(
        "You generate a very short story outline based on the user's input."
        "If there is any feedback provided, use it to improve the outline."
    ),
)


@dataclass
class EvaluationFeedback:
    score: Literal["pass", "needs_improvement", "fail"]
    feedback: str


evaluator = Agent[None](
    name="evaluator",
    instructions=(
        "You evaluate a story outline and decide if it's good enough."
        "If it's not good enough, you provide feedback on what needs to be improved."
        "Never give it a pass on the first try."
    ),
    output_type=EvaluationFeedback,
)


async def main() -> None:
    msg = input("What kind of story would you like to hear? ")
    input_items: list[TResponseInputItem] = [{"content": msg, "role": "user"}]

    latest_outline: str | None = None

    # We'll run the entire workflow in a single trace
    with trace("LLM as a judge"):
        while True:
            story_outline_result = await Runner.run(
                story_outline_generator,
                input_items,
            )

            input_items = story_outline_result.to_input_list()
            latest_outline = ItemHelpers.text_message_outputs(story_outline_result.new_items)
            print("Story outline generated")

            evaluator_result = await Runner.run(evaluator, input_items)
            result: EvaluationFeedback = evaluator_result.final_output

            print(f"Evaluator score: {result.score}")

            if result.score == "pass":
                print("Story outline is good enough, exiting.")
                break

            print("Re-running with feedback")

            input_items.append({"content": f"Feedback: {result.feedback}", "role": "user"})

    print(f"Final story outline: {latest_outline}")


if __name__ == "__main__":
    asyncio.run(main())



--- START OF FILE examples/handoffs/message_filter_streaming.py ---

from __future__ import annotations

import json
import random

from agents import Agent, HandoffInputData, Runner, function_tool, handoff, trace
from agents.extensions import handoff_filters


@function_tool
def random_number_tool(max: int) -> int:
    """Return a random integer between 0 and the given maximum."""
    return random.randint(0, max)


def spanish_handoff_message_filter(handoff_message_data: HandoffInputData) -> HandoffInputData:
    # First, we'll remove any tool-related messages from the message history
    handoff_message_data = handoff_filters.remove_all_tools(handoff_message_data)

    # Second, we'll also remove the first two items from the history, just for demonstration
    history = (
        tuple(handoff_message_data.input_history[2:])
        if isinstance(handoff_message_data.input_history, tuple)
        else handoff_message_data.input_history
    )

    return HandoffInputData(
        input_history=history,
        pre_handoff_items=tuple(handoff_message_data.pre_handoff_items),
        new_items=tuple(handoff_message_data.new_items),
    )


first_agent = Agent(
    name="Assistant",
    instructions="Be extremely concise.",
    tools=[random_number_tool],
)

spanish_agent = Agent(
    name="Spanish Assistant",
    instructions="You only speak Spanish and are extremely concise.",
    handoff_description="A Spanish-speaking assistant.",
)

second_agent = Agent(
    name="Assistant",
    instructions=(
        "Be a helpful assistant. If the user speaks Spanish, handoff to the Spanish assistant."
    ),
    handoffs=[handoff(spanish_agent, input_filter=spanish_handoff_message_filter)],
)


async def main():
    # Trace the entire run as a single workflow
    with trace(workflow_name="Streaming message filter"):
        # 1. Send a regular message to the first agent
        result = await Runner.run(first_agent, input="Hi, my name is Sora.")

        print("Step 1 done")

        # 2. Ask it to square a number
        result = await Runner.run(
            second_agent,
            input=result.to_input_list()
            + [{"content": "Can you generate a random number between 0 and 100?", "role": "user"}],
        )

        print("Step 2 done")

        # 3. Call the second agent
        result = await Runner.run(
            second_agent,
            input=result.to_input_list()
            + [
                {
                    "content": "I live in New York City. Whats the population of the city?",
                    "role": "user",
                }
            ],
        )

        print("Step 3 done")

        # 4. Cause a handoff to occur
        stream_result = Runner.run_streamed(
            second_agent,
            input=result.to_input_list()
            + [
                {
                    "content": "Por favor habla en español. ¿Cuál es mi nombre y dónde vivo?",
                    "role": "user",
                }
            ],
        )
        async for _ in stream_result.stream_events():
            pass

        print("Step 4 done")

    print("\n===Final messages===\n")

    # 5. That should have caused spanish_handoff_message_filter to be called, which means the
    # output should be missing the first two messages, and have no tool calls.
    # Let's print the messages to see what happened
    for item in stream_result.to_input_list():
        print(json.dumps(item, indent=2))
        """
        $python examples/handoffs/message_filter_streaming.py
        Step 1 done
        Step 2 done
        Step 3 done
        Tu nombre y lugar de residencia no los tengo disponibles. Solo sé que mencionaste vivir en la ciudad de Nueva York.
        Step 4 done

        ===Final messages===

        {
            "content": "Can you generate a random number between 0 and 100?",
            "role": "user"
            }
            {
            "id": "...",
            "content": [
                {
                "annotations": [],
                "text": "Sure! Here's a random number between 0 and 100: **37**.",
                "type": "output_text"
                }
            ],
            "role": "assistant",
            "status": "completed",
            "type": "message"
            }
            {
            "content": "I live in New York City. Whats the population of the city?",
            "role": "user"
            }
            {
            "id": "...",
            "content": [
                {
                "annotations": [],
                "text": "As of the latest estimates, New York City's population is approximately 8.5 million people. Would you like more information about the city?",
                "type": "output_text"
                }
            ],
            "role": "assistant",
            "status": "completed",
            "type": "message"
            }
            {
            "content": "Por favor habla en espa\u00f1ol. \u00bfCu\u00e1l es mi nombre y d\u00f3nde vivo?",
            "role": "user"
            }
            {
            "id": "...",
            "content": [
                {
                "annotations": [],
                "text": "No s\u00e9 tu nombre, pero me dijiste que vives en Nueva York.",
                "type": "output_text"
                }
            ],
            "role": "assistant",
            "status": "completed",
            "type": "message"
            }
        """


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())



--- START OF FILE examples/handoffs/message_filter.py ---

from __future__ import annotations

import json
import random

from agents import Agent, HandoffInputData, Runner, function_tool, handoff, trace
from agents.extensions import handoff_filters


@function_tool
def random_number_tool(max: int) -> int:
    """Return a random integer between 0 and the given maximum."""
    return random.randint(0, max)


def spanish_handoff_message_filter(handoff_message_data: HandoffInputData) -> HandoffInputData:
    # First, we'll remove any tool-related messages from the message history
    handoff_message_data = handoff_filters.remove_all_tools(handoff_message_data)

    # Second, we'll also remove the first two items from the history, just for demonstration
    history = (
        tuple(handoff_message_data.input_history[2:])
        if isinstance(handoff_message_data.input_history, tuple)
        else handoff_message_data.input_history
    )

    return HandoffInputData(
        input_history=history,
        pre_handoff_items=tuple(handoff_message_data.pre_handoff_items),
        new_items=tuple(handoff_message_data.new_items),
    )


first_agent = Agent(
    name="Assistant",
    instructions="Be extremely concise.",
    tools=[random_number_tool],
)

spanish_agent = Agent(
    name="Spanish Assistant",
    instructions="You only speak Spanish and are extremely concise.",
    handoff_description="A Spanish-speaking assistant.",
)

second_agent = Agent(
    name="Assistant",
    instructions=(
        "Be a helpful assistant. If the user speaks Spanish, handoff to the Spanish assistant."
    ),
    handoffs=[handoff(spanish_agent, input_filter=spanish_handoff_message_filter)],
)


async def main():
    # Trace the entire run as a single workflow
    with trace(workflow_name="Message filtering"):
        # 1. Send a regular message to the first agent
        result = await Runner.run(first_agent, input="Hi, my name is Sora.")

        print("Step 1 done")

        # 2. Ask it to square a number
        result = await Runner.run(
            second_agent,
            input=result.to_input_list()
            + [{"content": "Can you generate a random number between 0 and 100?", "role": "user"}],
        )

        print("Step 2 done")

        # 3. Call the second agent
        result = await Runner.run(
            second_agent,
            input=result.to_input_list()
            + [
                {
                    "content": "I live in New York City. Whats the population of the city?",
                    "role": "user",
                }
            ],
        )

        print("Step 3 done")

        # 4. Cause a handoff to occur
        result = await Runner.run(
            second_agent,
            input=result.to_input_list()
            + [
                {
                    "content": "Por favor habla en español. ¿Cuál es mi nombre y dónde vivo?",
                    "role": "user",
                }
            ],
        )

        print("Step 4 done")

    print("\n===Final messages===\n")

    # 5. That should have caused spanish_handoff_message_filter to be called, which means the
    # output should be missing the first two messages, and have no tool calls.
    # Let's print the messages to see what happened
    for message in result.to_input_list():
        print(json.dumps(message, indent=2))
        # tool_calls = message.tool_calls if isinstance(message, AssistantMessage) else None

        # print(f"{message.role}: {message.content}\n  - Tool calls: {tool_calls or 'None'}")
        """
        $python examples/handoffs/message_filter.py
        Step 1 done
        Step 2 done
        Step 3 done
        Step 4 done

        ===Final messages===

        {
            "content": "Can you generate a random number between 0 and 100?",
            "role": "user"
        }
        {
        "id": "...",
        "content": [
            {
            "annotations": [],
            "text": "Sure! Here's a random number between 0 and 100: **42**.",
            "type": "output_text"
            }
        ],
        "role": "assistant",
        "status": "completed",
        "type": "message"
        }
        {
        "content": "I live in New York City. Whats the population of the city?",
        "role": "user"
        }
        {
        "id": "...",
        "content": [
            {
            "annotations": [],
            "text": "As of the most recent estimates, the population of New York City is approximately 8.6 million people. However, this number is constantly changing due to various factors such as migration and birth rates. For the latest and most accurate information, it's always a good idea to check the official data from sources like the U.S. Census Bureau.",
            "type": "output_text"
            }
        ],
        "role": "assistant",
        "status": "completed",
        "type": "message"
        }
        {
        "content": "Por favor habla en espa\u00f1ol. \u00bfCu\u00e1l es mi nombre y d\u00f3nde vivo?",
        "role": "user"
        }
        {
        "id": "...",
        "content": [
            {
            "annotations": [],
            "text": "No tengo acceso a esa informaci\u00f3n personal, solo s\u00e9 lo que me has contado: vives en Nueva York.",
            "type": "output_text"
            }
        ],
        "role": "assistant",
        "status": "completed",
        "type": "message"
        }
        """


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())


