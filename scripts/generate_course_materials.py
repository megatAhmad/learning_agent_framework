#!/usr/bin/env python3
"""Generate course notebooks, mirrored solutions, and sample assets."""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
SOLUTIONS_DIR = REPO_ROOT / "solutions"
SUPPLEMENTAL_NOTEBOOKS_DIR = NOTEBOOKS_DIR / "supplemental"
SUPPLEMENTAL_SOLUTIONS_DIR = SOLUTIONS_DIR / "supplemental"
DATA_DIR = REPO_ROOT / "data"


def markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.strip() + "\n",
    }


def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": dedent(source).strip() + "\n",
    }


NOTEBOOK_METADATA = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    },
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.12.3",
    },
}


COMMON_SETUP_CODE = """
from pathlib import Path
import sys

PROJECT_ROOT = Path.cwd()
if not (PROJECT_ROOT / "helpers").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT))

from helpers import (
    LocalTfidfVectorStore,
    SQLiteConversationMemory,
    assert_minimum_python,
    chunk_documents,
    create_agent,
    create_chat_client,
    describe_response,
    load_settings,
    load_text_documents,
    print_banner,
    print_json,
    resolve_notebook_root,
    summarize_session,
    validate_provider_configuration,
)
"""


STEP_DEFINITIONS = [
    {
        "number": 1,
        "slug": "01_setup_and_environment.ipynb",
        "title": "Setup & Environment Configuration",
        "duration": "30 minutes",
        "difficulty": "Beginner",
        "objectives": [
            "Verify the local Python and notebook environment.",
            "Load the course settings from `.env`.",
            "Confirm OpenRouter or Azure OpenAI configuration.",
            "Understand the repo layout before writing code.",
        ],
        "prerequisites": [
            "Python 3.10 or newer installed locally.",
            "A virtual environment with requirements installed.",
            "An OpenRouter or Azure OpenAI account.",
        ],
        "intro": dedent(
            """
            This notebook grounds the rest of the course. We confirm the interpreter version,
            inspect the generated repo layout, and validate provider settings before we ask the
            framework to make live calls.
            """
        ),
        "implementation": [
            (
                "Environment verification",
                """
                assert_minimum_python()

                settings = load_settings()
                print_json(
                    {
                        "provider": settings.provider,
                        "log_level": settings.log_level,
                        "debug": settings.debug,
                    },
                    title="Resolved course settings",
                )

                print_json(validate_provider_configuration(), title="Provider configuration check")
                """,
            ),
            (
                "Repo layout preview",
                """
                root = resolve_notebook_root()
                important_paths = [
                    root / "helpers",
                    root / "notebooks",
                    root / "solutions",
                    root / "docs",
                    root / "data",
                ]
                print_json({str(path.relative_to(root)): path.exists() for path in important_paths}, title="Repo layout")
                """,
            ),
        ],
        "exercise_prompt": "Write a small helper that prints which provider is active and whether the required credentials appear to be present.",
        "exercise_starter": """
        settings = load_settings()

        def show_provider_status():
            # TODO: return a small dictionary with provider status details
            return {}

        print_json(show_provider_status(), title="Exercise output")
        """,
        "exercise_solution": """
        settings = load_settings()

        def show_provider_status():
            checks = validate_provider_configuration(settings.provider)
            return {
                "provider": settings.provider_label(),
                "checks": checks,
                "ready_for_live_calls": all(checks.values()),
            }

        print_json(show_provider_status(), title="Exercise output")
        """,
        "best_practices": [
            "Keep `.env` out of version control and use `.env.example` as the contract.",
            "Prefer one provider for the first few notebooks so behavior is easier to compare.",
            "Run the smoke test script after changing credentials or model names.",
        ],
        "summary": "You now have a validated local environment and a clear picture of the generated course structure.",
        "resources": [
            "SETUP.md",
            "docs/llm_providers.md",
            "scripts/smoke_live.py",
        ],
        "expected_output": """
        Expected output snapshot:

        - Python version check passes
        - Provider configuration dictionary is displayed
        - Required repo folders are confirmed present
        """,
    },
    {
        "number": 2,
        "slug": "02_your_first_agent.ipynb",
        "title": "Your First Agent",
        "duration": "45 minutes",
        "difficulty": "Beginner",
        "objectives": [
            "Create a live chat client.",
            "Instantiate an `Agent` with clear instructions.",
            "Run a first prompt and inspect the response object.",
            "See how provider switching stays behind the helper layer.",
        ],
        "prerequisites": [
            "Step 1 completed.",
            "Live provider credentials available.",
        ],
        "intro": "This notebook introduces the smallest useful unit in the course: a single agent with instructions, a chat client, and a live prompt.",
        "implementation": [
            (
                "Create an agent",
                """
                agent = create_agent(
                    name="FirstAgent",
                    instructions="You are a clear, concise Python tutor for developers learning agent systems.",
                )

                print_json(
                    {
                        "name": agent.name,
                        "description": agent.description,
                    },
                    title="Agent summary",
                )
                """,
            ),
            (
                "Run a first live prompt",
                """
                response = await agent.run("Explain in 4 sentences what an AI agent is.")
                print(response.text)
                print_json(describe_response(response), title="Response details")
                """,
            ),
        ],
        "exercise_prompt": "Create a second agent with different instructions and compare how tone changes on the same question.",
        "exercise_starter": """
        # TODO: create a second agent with a different personality
        # TODO: run the same prompt against both agents and compare the responses
        """,
        "exercise_solution": """
        mentor = create_agent(
            name="MentorAgent",
            instructions="You are a supportive engineering mentor. Explain ideas with one practical example.",
        )
        reviewer = create_agent(
            name="ReviewerAgent",
            instructions="You are a senior reviewer. Explain ideas crisply and call out tradeoffs.",
        )

        prompt = "What is the value of keeping tools separate from prompts in an agent app?"
        mentor_response = await mentor.run(prompt)
        reviewer_response = await reviewer.run(prompt)

        print_banner("Mentor response")
        print(mentor_response.text)
        print_banner("Reviewer response")
        print(reviewer_response.text)
        """,
        "best_practices": [
            "Give the agent a narrow role before you add tools or memory.",
            "Inspect the response object, not just the rendered text.",
            "Change one variable at a time when comparing providers or prompts.",
        ],
        "summary": "You created a working live agent and saw how instructions shape the final answer.",
        "resources": [
            "helpers/llm.py",
            "docs/llm_providers.md",
        ],
        "expected_output": """
        Expected output snapshot:

        - A short explanation of what an AI agent is
        - A response summary with text, response_id, and message_count
        """,
    },
    {
        "number": 3,
        "slug": "03_multi_turn_conversations.ipynb",
        "title": "Multi-Turn Conversations",
        "duration": "45 minutes",
        "difficulty": "Beginner",
        "objectives": [
            "Use `AgentSession` to preserve context.",
            "Run multiple turns with the same agent.",
            "Inspect how session state changes over time.",
            "Understand why session state matters before adding memory stores.",
        ],
        "prerequisites": [
            "Step 2 completed.",
            "Comfort with `await` in Jupyter.",
        ],
        "intro": "A single response is useful, but most agent experiences rely on context carried across turns. This notebook introduces reusable sessions.",
        "implementation": [
            (
                "Create a session-aware agent",
                """
                from agent_framework import AgentSession

                session = AgentSession(session_id="intro-session")
                agent = create_agent(
                    name="ConversationAgent",
                    instructions="You are a helpful assistant that remembers recent context from the conversation.",
                )

                first = await agent.run("My name is Riley and I like building Python tools.", session=session)
                second = await agent.run("What is my name and what do I like building?", session=session)

                print_banner("Turn 1")
                print(first.text)
                print_banner("Turn 2")
                print(second.text)
                print_json(summarize_session(session), title="Session summary")
                """,
            ),
            (
                "Serialize session state",
                """
                session_dict = session.to_dict()
                print_json(session_dict, title="Serialized session")
                """,
            ),
        ],
        "exercise_prompt": "Continue the conversation for two more turns and inspect the serialized session again.",
        "exercise_starter": """
        # TODO: add two more turns using the same session
        # TODO: inspect the updated session with summarize_session(session)
        """,
        "exercise_solution": """
        third = await agent.run("Please also remember that I prefer short answers.", session=session)
        fourth = await agent.run("Summarize what you know about me in two bullets.", session=session)

        print_banner("Turn 3")
        print(third.text)
        print_banner("Turn 4")
        print(fourth.text)
        print_json(summarize_session(session), title="Updated session summary")
        """,
        "best_practices": [
            "Reuse the same session object for related conversation turns.",
            "Serialize sessions when you want to checkpoint or inspect state.",
            "Keep session state simple before introducing external persistence.",
        ],
        "summary": "You now have a repeatable pattern for multi-turn agent interactions using `AgentSession`.",
        "resources": [
            "helpers/debug.py",
            "helpers/memory.py",
        ],
        "expected_output": """
        Expected output snapshot:

        - The second answer correctly recalls the name Riley
        - The session summary shows a stable `session_id`
        """,
    },
    {
        "number": 4,
        "slug": "04_understanding_tools.ipynb",
        "title": "Understanding Tools",
        "duration": "60 minutes",
        "difficulty": "Intermediate",
        "objectives": [
            "Turn Python callables into tools with `@tool`.",
            "Pass tools into an agent constructor.",
            "Understand tool signatures and docstrings as part of the model contract.",
            "Inspect tool execution results through live runs.",
        ],
        "prerequisites": [
            "Step 3 completed.",
            "Comfort reading type hints.",
        ],
        "intro": "Tools let the model move beyond pure text generation and call real application logic. The key is to make that logic explicit, typed, and easy for the model to choose.",
        "implementation": [
            (
                "Define simple tools",
                """
                from agent_framework import tool

                @tool
                def add_numbers(a: int, b: int) -> int:
                    \"\"\"Add two integers and return the result.\"\"\"
                    return a + b

                @tool
                def get_current_focus() -> str:
                    \"\"\"Return the current course topic.\"\"\"
                    return "Tool anatomy in Microsoft Agent Framework"

                agent = create_agent(
                    name="ToolPrimer",
                    instructions="You may use tools when they help answer factual questions.",
                    tools=[add_numbers, get_current_focus],
                )
                """,
            ),
            (
                "Ask the model to choose a tool",
                """
                response = await agent.run("What is 17 plus 25, and what topic are we studying?")
                print(response.text)
                print_json(describe_response(response), title="Tool call response details")
                """,
            ),
        ],
        "exercise_prompt": "Create a third tool that formats a repo path and ask the agent a question that requires it.",
        "exercise_starter": """
        # TODO: define a third tool and pass it to a new agent
        # TODO: ask a question that causes the agent to use it
        """,
        "exercise_solution": """
        @tool
        def format_repo_path(name: str) -> str:
            \"\"\"Return an absolute path for a named top-level folder in the course repo.\"\"\"
            root = resolve_notebook_root()
            return str(root / name)

        path_agent = create_agent(
            name="PathAgent",
            instructions="Use tools to answer path and arithmetic questions accurately.",
            tools=[add_numbers, get_current_focus, format_repo_path],
        )
        response = await path_agent.run("What is 9 + 8 and where is the docs folder located?")
        print(response.text)
        """,
        "best_practices": [
            "Prefer small, composable tools over one giant helper.",
            "Write docstrings as if the model will read them, because it effectively does.",
            "Keep return values clean and predictable for easy reuse in final responses.",
        ],
        "summary": "You converted ordinary Python functions into model-callable tools and saw them participate in a live answer.",
        "resources": [
            "agent_framework FunctionTool and tool decorator docs",
            "helpers/llm.py",
        ],
        "expected_output": """
        Expected output snapshot:

        - The agent uses `add_numbers`
        - The final answer combines arithmetic with the tool-provided topic string
        """,
    },
    {
        "number": 5,
        "slug": "05_single_tool_integration.ipynb",
        "title": "Single Tool Integration",
        "duration": "60 minutes",
        "difficulty": "Intermediate",
        "objectives": [
            "Integrate one realistic tool into an agent flow.",
            "Return deterministic data for easy validation.",
            "Observe how the final answer wraps raw tool output.",
            "Add lightweight tool-level error handling.",
        ],
        "prerequisites": [
            "Step 4 completed.",
        ],
        "intro": "Before adding multiple tools or remote APIs, it helps to anchor on a single deterministic tool whose behavior is easy to inspect.",
        "implementation": [
            (
                "Weather tool",
                """
                from agent_framework import tool

                WEATHER_DATA = {
                    "Paris": "Sunny, 22C, light breeze",
                    "Seattle": "Cloudy, 14C, drizzle",
                    "Tokyo": "Rainy, 19C, humid",
                    "London": "Overcast, 16C, cool",
                }

                @tool
                def get_weather(city: str) -> str:
                    \"\"\"Return a deterministic weather snapshot for a supported city.\"\"\"
                    if city not in WEATHER_DATA:
                        return f"No weather sample is available for {city}."
                    return f"Weather in {city}: {WEATHER_DATA[city]}"

                weather_agent = create_agent(
                    name="WeatherBot",
                    instructions="Use the weather tool whenever the user asks for weather conditions.",
                    tools=[get_weather],
                )
                """,
            ),
            (
                "Live tool usage",
                """
                response = await weather_agent.run("What's the weather in Paris today?")
                print(response.text)
                """,
            ),
        ],
        "exercise_prompt": "Add one more city and ask the agent a comparison question that still uses the same tool.",
        "exercise_starter": """
        # TODO: extend WEATHER_DATA with another city
        # TODO: ask a follow-up question that compares two cities
        """,
        "exercise_solution": """
        WEATHER_DATA["Singapore"] = "Warm, 31C, humid"
        comparison = await weather_agent.run("Compare the weather in Paris and Singapore.")
        print(comparison.text)
        """,
        "best_practices": [
            "Start with deterministic data before moving to remote APIs.",
            "Return clear plain text from simple tools unless structured output is required.",
            "Treat unsupported inputs as part of the happy path, not an afterthought.",
        ],
        "summary": "You now have a stable one-tool pattern that is easy to reuse in later notebooks.",
        "resources": [
            "Step 4 notebook",
            "helpers/debug.py",
        ],
        "expected_output": """
        Expected output snapshot:

        - The tool returns a weather string for Paris
        - The final agent answer wraps that tool result in natural language
        """,
    },
    {
        "number": 6,
        "slug": "06_multiple_tools.ipynb",
        "title": "Multiple Tools",
        "duration": "60 minutes",
        "difficulty": "Intermediate",
        "objectives": [
            "Give one agent several tools with distinct purposes.",
            "Observe tool choice across different user requests.",
            "Think about tool overlap and ambiguity.",
            "Prepare for async and API-backed tools in the next step.",
        ],
        "prerequisites": [
            "Step 5 completed.",
        ],
        "intro": "Multiple tools introduce selection pressure. The model now needs good descriptions and enough examples to decide which function helps most.",
        "implementation": [
            (
                "Define a small toolbelt",
                """
                from agent_framework import tool
                from datetime import datetime

                @tool
                def calculate(expression: str) -> str:
                    \"\"\"Evaluate a simple arithmetic expression safely for notebook demos.\"\"\"
                    allowed = {"__builtins__": {}}
                    return str(eval(expression, allowed, {}))

                @tool
                def convert_c_to_f(celsius: float) -> float:
                    \"\"\"Convert Celsius to Fahrenheit.\"\"\"
                    return round((celsius * 9 / 5) + 32, 2)

                @tool
                def get_current_time() -> str:
                    \"\"\"Return the current local timestamp.\"\"\"
                    return datetime.now().isoformat(timespec="seconds")

                multi_tool_agent = create_agent(
                    name="MultiToolAgent",
                    instructions="Use the most relevant tool for math, time, and temperature requests.",
                    tools=[calculate, convert_c_to_f, get_current_time],
                )
                """,
            ),
            (
                "Exercise the tool selection",
                """
                prompts = [
                    "What is 15 + 27 * 3?",
                    "Convert 30C to Fahrenheit.",
                    "What time is it right now?",
                ]

                for prompt in prompts:
                    print_banner(prompt)
                    reply = await multi_tool_agent.run(prompt)
                    print(reply.text)
                """,
            ),
        ],
        "exercise_prompt": "Add the Step 5 weather tool so the same agent can answer weather and arithmetic questions in one session.",
        "exercise_starter": """
        # TODO: reuse or redefine get_weather and add it to the tool list
        # TODO: ask a weather question and a math question back to back
        """,
        "exercise_solution": """
        from agent_framework import tool

        @tool
        def get_weather(city: str) -> str:
            \"\"\"Return a deterministic weather sample for a city.\"\"\"
            samples = {"Paris": "Sunny, 22C", "Seattle": "Cloudy, 14C"}
            return samples.get(city, f"No sample weather for {city}")

        blended_agent = create_agent(
            name="BlendedAgent",
            instructions="Use tools whenever a question is factual or computational.",
            tools=[calculate, convert_c_to_f, get_current_time, get_weather],
        )
        for prompt in ["What's the weather in Seattle?", "What is 3 * (8 + 4)?"]:
            print_banner(prompt)
            result = await blended_agent.run(prompt)
            print(result.text)
        """,
        "best_practices": [
            "Make tool names distinct so the model has clear selection cues.",
            "Avoid two tools that answer nearly the same request in different ways.",
            "Test tools individually before blending them into one agent.",
        ],
        "summary": "You now have a coordinated multi-tool agent and a framework for debugging tool selection.",
        "resources": [
            "Step 5 notebook",
            "helpers/llm.py",
        ],
        "expected_output": """
        Expected output snapshot:

        - math prompt routes to `calculate`
        - conversion prompt routes to `convert_c_to_f`
        - time prompt routes to `get_current_time`
        """,
    },
    {
        "number": 7,
        "slug": "07_custom_tools_and_apis.ipynb",
        "title": "Custom Tools & API Integration",
        "duration": "75 minutes",
        "difficulty": "Intermediate-Advanced",
        "objectives": [
            "Build async tools for remote APIs.",
            "Add retries and defensive error handling.",
            "Keep the tool contract readable even when the implementation is async.",
            "Use live API results in a model answer.",
        ],
        "prerequisites": [
            "Step 6 completed.",
            "Comfort with `aiohttp` and async functions.",
        ],
        "intro": "Remote APIs introduce latency, partial failures, and payload transformation. This notebook shows how to wrap that complexity in a tool the model can still use safely.",
        "implementation": [
            (
                "Async Wikipedia tool",
                """
                import aiohttp
                from agent_framework import tool

                @tool
                async def search_wikipedia(query: str) -> str:
                    \"\"\"Search Wikipedia and return up to three short snippets.\"\"\"
                    url = "https://en.wikipedia.org/w/api.php"
                    params = {
                        "action": "query",
                        "list": "search",
                        "srsearch": query,
                        "format": "json",
                    }
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, params=params, timeout=10) as response:
                            response.raise_for_status()
                            payload = await response.json()
                    results = payload.get("query", {}).get("search", [])
                    if not results:
                        return "No Wikipedia results found."
                    return "\\n".join(
                        f"- {item['title']}: {item['snippet'][:120]}..."
                        for item in results[:3]
                    )

                api_agent = create_agent(
                    name="WikiAgent",
                    instructions="Use the Wikipedia tool for fact-finding questions and summarize the results clearly.",
                    tools=[search_wikipedia],
                )
                """,
            ),
            (
                "Live API-backed question",
                """
                response = await api_agent.run("Give me a short introduction to Python generators.")
                print(response.text)
                """,
            ),
        ],
        "exercise_prompt": "Wrap the Wikipedia request in a retry helper so transient network errors do not fail the whole tool immediately.",
        "exercise_starter": """
        # TODO: create a retrying wrapper around the HTTP request
        # TODO: call it from a second version of the tool
        """,
        "exercise_solution": """
        import asyncio

        async def fetch_json_with_retry(url: str, params: dict, retries: int = 3) -> dict:
            for attempt in range(retries):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, params=params, timeout=10) as response:
                            response.raise_for_status()
                            return await response.json()
                except Exception:
                    if attempt == retries - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)
            raise RuntimeError("Unreachable")

        @tool
        async def resilient_wikipedia(query: str) -> str:
            \"\"\"Search Wikipedia with retry handling.\"\"\"
            payload = await fetch_json_with_retry(
                "https://en.wikipedia.org/w/api.php",
                {
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "format": "json",
                },
            )
            results = payload.get("query", {}).get("search", [])
            return "\\n".join(item["title"] for item in results[:3]) or "No results"
        """,
        "best_practices": [
            "Keep remote tools narrow and easy to test.",
            "Transform large JSON payloads before handing them back to the model.",
            "Plan for rate limits, timeouts, and empty results from the beginning.",
        ],
        "summary": "You now have a pattern for async, API-backed tools that still feels clean at the agent layer.",
        "resources": [
            "aiohttp documentation",
            "Wikipedia API reference",
        ],
        "expected_output": """
        Expected output snapshot:

        - The tool fetches Wikipedia data successfully
        - The model summarizes the returned snippets in a clean answer
        """,
    },
    {
        "number": 8,
        "slug": "08_memory_and_sessions.ipynb",
        "title": "Memory & Sessions",
        "duration": "60 minutes",
        "difficulty": "Intermediate",
        "objectives": [
            "Distinguish in-memory session state from external persistence.",
            "Store and retrieve conversation history in SQLite.",
            "Blend notebook-local session state with a durable store.",
            "Prepare for RAG and richer context engineering.",
        ],
        "prerequisites": [
            "Step 7 completed.",
        ],
        "intro": "Sessions give you in-run context. Durable memory lets your system bring context back later. This notebook uses a lightweight SQLite store so the pattern stays easy to inspect locally.",
        "implementation": [
            (
                "Persist simple conversation turns",
                """
                from agent_framework import AgentSession

                memory = SQLiteConversationMemory(resolve_notebook_root() / "data" / "databases" / "memory_demo.sqlite3")
                session = AgentSession(session_id="alice-session")
                memory_agent = create_agent(
                    name="MemoryAgent",
                    instructions="You are a helpful assistant that uses prior context when available.",
                )

                first = await memory_agent.run("My name is Alice and I work on platform engineering.", session=session)
                memory.save("alice", "My name is Alice and I work on platform engineering.", first.text)

                second = await memory_agent.run("Give me one encouraging sentence about learning agents.", session=session)
                memory.save("alice", "Give me one encouraging sentence about learning agents.", second.text)

                history = memory.history("alice")
                print_json([record.__dict__ for record in history], title="SQLite conversation history")
                """,
            ),
            (
                "Blend memory back into a prompt",
                """
                recent_notes = "\\n".join(f"- {item.user_message}" for item in history)
                recall_prompt = f\"\"\"Use this known context about the user:
                {recent_notes}

                What do you know about Alice?\"\"\"

                recall = await memory_agent.run(recall_prompt, session=session)
                print(recall.text)
                """,
            ),
        ],
        "exercise_prompt": "Store another turn and create a helper that formats the last three memory records for prompt injection.",
        "exercise_starter": """
        # TODO: save another interaction
        # TODO: write a helper that returns the most recent three records as bullet points
        """,
        "exercise_solution": """
        third_question = "Please remember that I prefer concise examples."
        third_response = await memory_agent.run(third_question, session=session)
        memory.save("alice", third_question, third_response.text)

        def recent_memory_bullets(user_id: str, limit: int = 3) -> str:
            rows = memory.history(user_id, limit=limit)
            return "\\n".join(f"- {row.user_message}" for row in rows)

        print(recent_memory_bullets("alice"))
        """,
        "best_practices": [
            "Use session state for active conversations and external storage for recall later.",
            "Persist only the fields you truly need for later context.",
            "Review stored memory formats before you rely on them in prompts.",
        ],
        "summary": "You now have both short-lived session context and a simple durable memory layer.",
        "resources": [
            "helpers/memory.py",
            "Step 3 notebook",
        ],
        "expected_output": """
        Expected output snapshot:

        - Two or more conversation rows saved in SQLite
        - A recall prompt that references Alice correctly
        """,
    },
    {
        "number": 9,
        "slug": "09_rag_implementation.ipynb",
        "title": "RAG Implementation",
        "duration": "75 minutes",
        "difficulty": "Intermediate-Advanced",
        "objectives": [
            "Load local documents for retrieval.",
            "Chunk content into search-friendly segments.",
            "Use TF-IDF as a local retrieval baseline.",
            "Inject retrieved context into a live model prompt.",
        ],
        "prerequisites": [
            "Step 8 completed.",
            "Basic understanding of embeddings and similarity search.",
        ],
        "intro": "RAG adds non-parametric context to your system. In this course repo we start with a local TF-IDF retriever so the retrieval mechanics are visible before moving to heavier infrastructure.",
        "implementation": [
            (
                "Index the sample documents",
                """
                documents = load_text_documents(resolve_notebook_root() / "data" / "documents")
                chunks = chunk_documents(documents)
                store = LocalTfidfVectorStore()
                store.add_chunks(chunks)

                print_json(
                    {
                        "document_count": len(documents),
                        "chunk_count": len(chunks),
                    },
                    title="RAG corpus summary",
                )
                """,
            ),
            (
                "Retrieve context and ask a live question",
                """
                question = "What are the benefits of async programming in Python?"
                results = store.search(question, top_k=3)
                context = "\\n\\n".join(
                    f"Source: {item['chunk'].title}\\n{item['chunk'].content}"
                    for item in results
                )

                rag_agent = create_agent(
                    name="RAGAgent",
                    instructions="Answer using the supplied context. If the context is thin, say so clearly.",
                )
                response = await rag_agent.run(
                    f\"\"\"Context:
                    {context}

                    Question: {question}
                    Answer using the context above.\"\"\"
                )
                print(response.text)
                """,
            ),
        ],
        "exercise_prompt": "Try a different question and print the retrieval scores before you ask the model.",
        "exercise_starter": """
        # TODO: search for another question
        # TODO: print each retrieved chunk title and similarity score
        """,
        "exercise_solution": """
        another_question = "How do tools make agent systems more reliable?"
        retrieved = store.search(another_question, top_k=3)
        for item in retrieved:
            print(item["chunk"].title, round(item["score"], 3))
        """,
        "best_practices": [
            "Inspect retrieval quality before blaming the generation layer.",
            "Keep chunk sizes and overlap small enough to debug locally.",
            "Tell the model explicitly how to behave when context is incomplete.",
        ],
        "summary": "You built a complete local RAG loop: load, chunk, retrieve, prompt, answer.",
        "resources": [
            "helpers/rag.py",
            "data/documents",
        ],
        "expected_output": """
        Expected output snapshot:

        - A corpus summary showing document and chunk counts
        - Retrieved chunk scores
        - A grounded answer that references the retrieved context
        """,
    },
    {
        "number": 10,
        "slug": "10_basic_workflows.ipynb",
        "title": "Basic Workflows",
        "duration": "75 minutes",
        "difficulty": "Intermediate",
        "objectives": [
            "Create a sequential workflow with typed executors.",
            "Connect nodes using `WorkflowBuilder`.",
            "Run the workflow on sample input.",
            "Read workflow outputs as a structured pipeline result.",
        ],
        "prerequisites": [
            "Step 9 completed.",
        ],
        "intro": "Workflows make dataflow explicit. Instead of one agent doing everything, we connect small executors into a graph that can be reasoned about step by step.",
        "implementation": [
            (
                "Build a three-step workflow",
                """
                from typing_extensions import Never
                from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler

                class ExtractExecutor(Executor):
                    @handler
                    async def process(self, text: str, ctx: WorkflowContext[str]) -> None:
                        await ctx.send_message(f"KEY IDEAS: {text[:120]}")

                class AnalyzeExecutor(Executor):
                    @handler
                    async def process(self, extracted: str, ctx: WorkflowContext[str]) -> None:
                        await ctx.send_message(f"ANALYSIS: {extracted}")

                class ReportExecutor(Executor):
                    @handler
                    async def process(self, analysis: str, ctx: WorkflowContext[Never, str]) -> None:
                        await ctx.yield_output(f"REPORT: {analysis}")

                extract = ExtractExecutor(id="extract")
                analyze = AnalyzeExecutor(id="analyze")
                report = ReportExecutor(id="report")

                workflow = WorkflowBuilder(start_executor=extract).add_chain([extract, analyze, report]).build()
                """,
            ),
            (
                "Run the workflow",
                """
                run_result = await workflow.run(
                    "The engineering team wants a course that moves from single agents to orchestration."
                )
                print(run_result.get_outputs())
                """,
            ),
        ],
        "exercise_prompt": "Add a fourth executor that reformats the report before it becomes the final output.",
        "exercise_starter": """
        # TODO: add one more executor to the chain
        # TODO: rebuild the workflow and run it again
        """,
        "exercise_solution": """
        class DraftReportExecutor(Executor):
            @handler
            async def process(self, analysis: str, ctx: WorkflowContext[str]) -> None:
                await ctx.send_message(f"DRAFT REPORT: {analysis}")

        class FormatExecutor(Executor):
            @handler
            async def process(self, report_text: str, ctx: WorkflowContext[Never, str]) -> None:
                await ctx.yield_output(report_text.replace("DRAFT REPORT:", "FINAL REPORT:"))

        draft_report = DraftReportExecutor(id="draft_report")
        formatter = FormatExecutor(id="formatter")
        workflow_v2 = WorkflowBuilder(start_executor=extract).add_chain([extract, analyze, draft_report, formatter]).build()
        print((await workflow_v2.run("Course design should stay progressive and hands-on.")).get_outputs())
        """,
        "best_practices": [
            "Keep executor responsibilities narrow and typed.",
            "Prefer chains for simple linear flows before using branching APIs.",
            "Inspect outputs at each step when debugging graph behavior.",
        ],
        "summary": "You created a sequential typed workflow and ran it end to end.",
        "resources": [
            "agent_framework WorkflowBuilder docs",
            "Step 11 notebook",
        ],
        "expected_output": """
        Expected output snapshot:

        - The workflow returns a list containing one final report string
        """,
    },
    {
        "number": 11,
        "slug": "11_conditional_workflows.ipynb",
        "title": "Conditional Workflows",
        "duration": "75 minutes",
        "difficulty": "Intermediate-Advanced",
        "objectives": [
            "Route messages based on conditions.",
            "Model branching logic with small executors.",
            "Choose specialized paths for technical and business inputs.",
            "Keep fallback behavior explicit.",
        ],
        "prerequisites": [
            "Step 10 completed.",
        ],
        "intro": "Once dataflow becomes non-linear, the workflow needs explicit routing rules. This notebook shows a minimal branching setup without hiding the logic behind a black box.",
        "implementation": [
            (
                "Route to specialized executors",
                """
                from typing_extensions import Never
                from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler

                class Router(Executor):
                    @handler
                    async def process(self, text: str, ctx: WorkflowContext[dict]) -> None:
                        route = "technical" if "python" in text.lower() or "code" in text.lower() else "business"
                        await ctx.send_message({"route": route, "text": text})

                class TechnicalExecutor(Executor):
                    @handler
                    async def process(self, payload: dict, ctx: WorkflowContext[Never, str]) -> None:
                        await ctx.yield_output(f"TECH PATH: {payload['text']}")

                class BusinessExecutor(Executor):
                    @handler
                    async def process(self, payload: dict, ctx: WorkflowContext[Never, str]) -> None:
                        await ctx.yield_output(f"BUSINESS PATH: {payload['text']}")

                router = Router(id="router")
                technical = TechnicalExecutor(id="technical")
                business = BusinessExecutor(id="business")

                conditional = (
                    WorkflowBuilder(start_executor=router)
                    .add_edge(router, technical, condition=lambda payload: payload["route"] == "technical")
                    .add_edge(router, business, condition=lambda payload: payload["route"] == "business")
                    .build()
                )
                """,
            ),
            (
                "Try both branches",
                """
                print((await conditional.run("How do I write async Python code?")).get_outputs())
                print((await conditional.run("How should we position this training program for managers?")).get_outputs())
                """,
            ),
        ],
        "exercise_prompt": "Add a third fallback path for general questions that do not match either primary route.",
        "exercise_starter": """
        # TODO: add a general route and a general executor
        """,
        "exercise_solution": """
        class GeneralExecutor(Executor):
            @handler
            async def process(self, payload: dict, ctx: WorkflowContext[Never, str]) -> None:
                await ctx.yield_output(f"GENERAL PATH: {payload['text']}")

        general = GeneralExecutor(id="general")

        def classify_route(payload: dict) -> str:
            text = payload["text"].lower()
            if "python" in text or "code" in text:
                return "technical"
            if "strategy" in text or "program" in text or "manager" in text:
                return "business"
            return "general"

        class RouterV2(Executor):
            @handler
            async def process(self, text: str, ctx: WorkflowContext[dict]) -> None:
                await ctx.send_message({"route": classify_route({"text": text}), "text": text})

        router_v2 = RouterV2(id="router_v2")
        conditional_v2 = (
            WorkflowBuilder(start_executor=router_v2)
            .add_edge(router_v2, technical, condition=lambda payload: payload["route"] == "technical")
            .add_edge(router_v2, business, condition=lambda payload: payload["route"] == "business")
            .add_edge(router_v2, general, condition=lambda payload: payload["route"] == "general")
            .build()
        )

        print((await conditional_v2.run("How do I structure Python async tools?")).get_outputs())
        print((await conditional_v2.run("How should we brief managers on this program?")).get_outputs())
        print((await conditional_v2.run("Summarize the course in one sentence.")).get_outputs())
        """,
        "best_practices": [
            "Keep classification logic inspectable and testable.",
            "Add fallback routes deliberately instead of letting messages disappear.",
            "Treat routing rules as product logic, not just plumbing.",
        ],
        "summary": "You now have a concrete branching workflow that routes messages to specialized handlers.",
        "resources": [
            "Step 10 notebook",
            "agent_framework WorkflowBuilder conditional edges",
        ],
        "expected_output": """
        Expected output snapshot:

        - Technical input yields a `TECH PATH` result
        - Business input yields a `BUSINESS PATH` result
        """,
    },
    {
        "number": 12,
        "slug": "12_orchestration_patterns.ipynb",
        "title": "Orchestration Patterns",
        "duration": "90 minutes",
        "difficulty": "Advanced",
        "objectives": [
            "Compare sequential, concurrent, and handoff patterns.",
            "Use multiple live agents in one orchestration.",
            "Measure the tradeoffs at a high level.",
            "Choose a pattern based on task shape rather than novelty.",
        ],
        "prerequisites": [
            "Step 11 completed.",
        ],
        "intro": "Orchestration patterns are about control flow, not just agent count. The same providers can support very different system designs depending on how tasks move through the team.",
        "implementation": [
            (
                "Sequential and concurrent orchestration",
                """
                import asyncio

                researcher = create_agent(name="Researcher", instructions="Gather key points on the topic.")
                analyst = create_agent(name="Analyst", instructions="Analyze the provided points for implications.")
                reporter = create_agent(name="Reporter", instructions="Write a concise summary for engineers.")

                async def sequential_orchestration(task: str) -> str:
                    research = await researcher.run(task)
                    analysis = await analyst.run(research.text)
                    report = await reporter.run(analysis.text)
                    return report.text

                async def concurrent_orchestration(task: str) -> list[str]:
                    agents = [
                        create_agent(name="MarketLens", instructions="Focus on market implications."),
                        create_agent(name="EngineeringLens", instructions="Focus on implementation implications."),
                        create_agent(name="ProductLens", instructions="Focus on user and product implications."),
                    ]
                    responses = await asyncio.gather(*(agent.run(task) for agent in agents))
                    return [item.text for item in responses]
                """,
            ),
            (
                "Simple handoff",
                """
                triage = create_agent(
                    name="TriageAgent",
                    instructions="Classify a request as technical, billing, or general using a single lowercase label.",
                )
                technical_support = create_agent(name="TechnicalSupport", instructions="Answer technical support questions.")
                billing_support = create_agent(name="BillingSupport", instructions="Answer billing support questions.")
                general_support = create_agent(name="GeneralSupport", instructions="Answer general questions.")

                async def handoff(request: str) -> str:
                    label = (await triage.run(f"Classify this request: {request}")).text.lower()
                    if "technical" in label:
                        return (await technical_support.run(request)).text
                    if "billing" in label:
                        return (await billing_support.run(request)).text
                    return (await general_support.run(request)).text
                """,
            ),
        ],
        "exercise_prompt": "Run the same topic through the sequential and concurrent patterns, then compare the output style and latency you observe.",
        "exercise_starter": """
        # TODO: call sequential_orchestration on one topic
        # TODO: call concurrent_orchestration on the same topic
        # TODO: compare the differences in a short note
        """,
        "exercise_solution": """
        sequential_result = await sequential_orchestration("Explain the impact of agent tools on developer productivity.")
        concurrent_result = await concurrent_orchestration("Explain the impact of agent tools on developer productivity.")

        print_banner("Sequential")
        print(sequential_result)
        print_banner("Concurrent")
        for item in concurrent_result:
            print("-", item)
        """,
        "best_practices": [
            "Use sequential flow when every step depends on the last one.",
            "Use concurrent flow when views are independent and easy to merge.",
            "Use handoff when specialization matters more than parallelism.",
        ],
        "summary": "You explored the three core orchestration patterns and saw why system shape matters as much as model choice.",
        "resources": [
            "Step 13 notebook",
            "agent_framework workflow and agent docs",
        ],
        "expected_output": """
        Expected output snapshot:

        - sequential orchestration returns one synthesized answer
        - concurrent orchestration returns several perspective-specific answers
        """,
    },
    {
        "number": 13,
        "slug": "13_advanced_orchestration.ipynb",
        "title": "Advanced Orchestration",
        "duration": "90 minutes",
        "difficulty": "Advanced",
        "objectives": [
            "Implement a lightweight group-chat loop.",
            "Model manager-worker decomposition with parallel subtasks.",
            "Reason about orchestration state beyond one direct prompt-response pair.",
            "Prepare for longer-running systems and supervision.",
        ],
        "prerequisites": [
            "Step 12 completed.",
        ],
        "intro": "Advanced orchestration becomes easier to understand when we build it in plain Python first. This notebook keeps the control loop explicit so the role of each agent stays visible.",
        "implementation": [
            (
                "Group chat loop",
                """
                import asyncio

                class GroupChat:
                    def __init__(self, agents, max_turns: int = 4):
                        self.agents = agents
                        self.max_turns = max_turns
                        self.history = []

                    async def run(self, topic: str) -> list[str]:
                        self.history = [f"Topic: {topic}"]
                        current_prompt = topic
                        for turn in range(self.max_turns):
                            agent = self.agents[turn % len(self.agents)]
                            response = await agent.run(
                                "Conversation so far:\\n" + "\\n".join(self.history) + f"\\n\\nRespond to: {current_prompt}"
                            )
                            self.history.append(f"{agent.name}: {response.text}")
                            current_prompt = response.text
                        return self.history

                group_chat = GroupChat(
                    [
                        create_agent(name="PM", instructions="Speak as a product manager."),
                        create_agent(name="Engineer", instructions="Speak as an engineer."),
                        create_agent(name="Designer", instructions="Speak as a designer."),
                    ]
                )
                """,
            ),
            (
                "Manager-worker decomposition",
                """
                class ManagerWorkerOrchestrator:
                    def __init__(self):
                        self.manager = create_agent(
                            name="Manager",
                            instructions="Break a goal into 3 short, concrete subtasks."
                        )
                        self.workers = [
                            create_agent(name="WorkerA", instructions="Complete the assigned subtask."),
                            create_agent(name="WorkerB", instructions="Complete the assigned subtask."),
                            create_agent(name="WorkerC", instructions="Complete the assigned subtask."),
                        ]

                    async def run(self, goal: str) -> dict:
                        task_plan = await self.manager.run(f"Break this into 3 numbered tasks:\\n{goal}")
                        tasks = [line.strip() for line in task_plan.text.splitlines() if line.strip()[:1].isdigit()]
                        results = await asyncio.gather(
                            *(worker.run(task) for worker, task in zip(self.workers, tasks, strict=False))
                        )
                        return {
                            "tasks": tasks,
                            "results": [item.text for item in results],
                        }

                orchestrator = ManagerWorkerOrchestrator()
                """,
            ),
        ],
        "exercise_prompt": "Run one group-chat topic and one manager-worker topic, then inspect the task breakdown or history.",
        "exercise_starter": """
        # TODO: run group_chat on a topic of your choice
        # TODO: run orchestrator on a more complex goal and inspect the returned dictionary
        """,
        "exercise_solution": """
        history = await group_chat.run("Design a helpful onboarding flow for new agent-framework learners.")
        print_json(history, title="Group chat history")

        result = await orchestrator.run("Create a launch plan for an internal agent-learning workshop.")
        print_json(result, title="Manager-worker result")
        """,
        "best_practices": [
            "Keep orchestration loops explicit while you are still learning the pattern.",
            "Distinguish role prompts from control logic.",
            "Inspect intermediate state instead of only the final synthesis.",
        ],
        "summary": "You now have two advanced orchestration patterns that make coordination state visible rather than magical.",
        "resources": [
            "Step 12 notebook",
            "docs/references.md",
        ],
        "expected_output": """
        Expected output snapshot:

        - Group chat returns a small conversation transcript
        - Manager-worker orchestration returns task and result lists
        """,
    },
    {
        "number": 14,
        "slug": "14_human_in_the_loop.ipynb",
        "title": "Human-in-the-Loop",
        "duration": "75 minutes",
        "difficulty": "Advanced",
        "objectives": [
            "Pause a workflow for approval.",
            "Model resumable state with checkpoints.",
            "Treat human review as a deliberate system boundary.",
            "Design for long-running workflows that need supervision.",
        ],
        "prerequisites": [
            "Step 13 completed.",
        ],
        "intro": "Human-in-the-loop is not just a UI prompt. It is a control point where the system explicitly waits for a trustworthy decision before acting.",
        "implementation": [
            (
                "Approval and checkpoint helpers",
                """
                from dataclasses import dataclass, field
                from datetime import datetime

                @dataclass
                class ApprovalRequest:
                    tool_name: str
                    reason: str
                    params: dict
                    status: str = "pending"

                @dataclass
                class CheckpointStore:
                    snapshots: dict = field(default_factory=dict)

                    def save(self, checkpoint_id: str, payload: dict) -> None:
                        self.snapshots[checkpoint_id] = {
                            "saved_at": datetime.utcnow().isoformat(),
                            "payload": payload,
                        }

                    def load(self, checkpoint_id: str) -> dict:
                        return self.snapshots[checkpoint_id]["payload"]

                approvals: list[ApprovalRequest] = []
                checkpoint_store = CheckpointStore()
                """,
            ),
            (
                "Simulate a gated operation",
                """
                async def request_approval(tool_name: str, reason: str, params: dict) -> bool:
                    approval = ApprovalRequest(tool_name=tool_name, reason=reason, params=params)
                    approvals.append(approval)
                    approval.status = "approved" if tool_name != "delete_database" else "rejected"
                    return approval.status == "approved"

                async def protected_delete(dataset_id: str) -> str:
                    allowed = await request_approval(
                        tool_name="delete_dataset",
                        reason="User requested destructive cleanup.",
                        params={"dataset_id": dataset_id},
                    )
                    if not allowed:
                        return "Deletion rejected."
                    checkpoint_store.save("before_delete", {"dataset_id": dataset_id})
                    return f"Deleted dataset {dataset_id}"

                print(await protected_delete("archive_2020"))
                print_json([approval.__dict__ for approval in approvals], title="Approvals")
                """,
            ),
        ],
        "exercise_prompt": "Add a resume helper that restores a checkpoint and prints the last saved payload.",
        "exercise_starter": """
        # TODO: add a resume helper that loads checkpoint_store.load(...)
        """,
        "exercise_solution": """
        def resume_from(checkpoint_id: str) -> dict:
            return checkpoint_store.load(checkpoint_id)

        print_json(resume_from("before_delete"), title="Resumed checkpoint payload")
        """,
        "best_practices": [
            "Require approval before destructive or irreversible actions.",
            "Checkpoint enough state to explain what the system was about to do.",
            "Separate approval records from model-generated text for auditability.",
        ],
        "summary": "You now have a basic pattern for approvals and checkpoint-based resume flows.",
        "resources": [
            "Step 15 notebook",
            "docs/troubleshooting.md",
        ],
        "expected_output": """
        Expected output snapshot:

        - An approval record is stored
        - A checkpoint payload is available for resume
        """,
    },
    {
        "number": 15,
        "slug": "15_production_features.ipynb",
        "title": "Production Features",
        "duration": "75 minutes",
        "difficulty": "Advanced",
        "objectives": [
            "Add structured logging around agent calls.",
            "Collect lightweight metrics and cost estimates.",
            "Trace prompts and responses for debugging.",
            "Close the course with a production-minded operating posture.",
        ],
        "prerequisites": [
            "Step 14 completed.",
        ],
        "intro": "Production readiness is about visibility. This notebook adds the minimum observability you need to reason about behavior, latency, failures, and rough usage costs.",
        "implementation": [
            (
                "Instrumentation helpers",
                """
                import logging
                from collections import defaultdict
                from dataclasses import dataclass
                from datetime import datetime
                from time import perf_counter

                logging.basicConfig(
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s",
                )
                logger = logging.getLogger("course.production")

                @dataclass
                class MetricPoint:
                    name: str
                    value: float
                    timestamp: str

                class MetricsCollector:
                    def __init__(self):
                        self.points = defaultdict(list)

                    def record(self, name: str, value: float) -> None:
                        self.points[name].append(
                            MetricPoint(name=name, value=value, timestamp=datetime.utcnow().isoformat())
                        )

                    def summary(self, name: str) -> dict:
                        values = [point.value for point in self.points[name]]
                        return {
                            "count": len(values),
                            "min": min(values) if values else None,
                            "max": max(values) if values else None,
                            "avg": sum(values) / len(values) if values else None,
                        }
                """,
            ),
            (
                "Instrument a live run",
                """
                metrics = MetricsCollector()
                production_agent = create_agent(
                    name="ProductionAgent",
                    instructions="Answer clearly and briefly for observability demos.",
                )

                start = perf_counter()
                response = await production_agent.run("List three signals that help debug an agent system.")
                duration = perf_counter() - start
                metrics.record("response_time_seconds", duration)

                logger.info("agent_call_completed", extra={"duration_seconds": duration})
                print(response.text)
                print_json(metrics.summary("response_time_seconds"), title="Metric summary")
                """,
            ),
        ],
        "exercise_prompt": "Add a tiny cost estimator that multiplies total tokens by a placeholder rate and prints a dashboard dictionary.",
        "exercise_starter": """
        # TODO: estimate cost from the response usage or a simple placeholder token count
        """,
        "exercise_solution": """
        usage = getattr(response, "usage", None)
        estimated_tokens = getattr(usage, "total_tokens", None) if usage else len(response.text.split()) * 2
        estimated_cost = estimated_tokens * 0.000002
        dashboard = {
            "response_time_seconds": duration,
            "estimated_tokens": estimated_tokens,
            "estimated_cost_usd": round(estimated_cost, 6),
        }
        print_json(dashboard, title="Production dashboard")
        """,
        "best_practices": [
            "Log the events you will wish you had during incident review.",
            "Record latency and token usage close to the call boundary.",
            "Keep debugging utilities simple enough to run inside a notebook first.",
        ],
        "summary": "You closed the course with the core production concerns: logging, metrics, debugging, and rough cost awareness.",
        "resources": [
            "helpers/debug.py",
            "scripts/smoke_live.py",
        ],
        "expected_output": """
        Expected output snapshot:

        - The live answer is printed
        - Response time metrics are summarized
        - A small dashboard dictionary is produced
        """,
    },
]


SUPPLEMENTAL_NOTEBOOKS = [
    {
        "number": 16,
        "slug": "16_intermediate_tool_reasoning_and_schema_design.ipynb",
        "title": "Intermediate: Tool Reasoning and Schema Design",
        "level": "Intermediate",
        "duration": "90 minutes",
        "objectives": [
            "Design tools with schema clarity and predictable outputs.",
            "Compare loose text returns with structured return contracts.",
            "Reason about tool ambiguity, overlap, and sequencing.",
            "Practice multi-step tool plans that the model can execute safely.",
        ],
        "prerequisites": [
            "Core Steps 4-7 completed.",
            "Comfort reading typed function signatures.",
        ],
        "intro": "This notebook goes beyond basic tool registration and focuses on how tool contract design changes model behavior. The goal is to make tools easier to choose, easier to compose, and easier to debug.",
        "implementation": [
            (
                "Compare weak and strong tool contracts",
                """
                from agent_framework import tool
                from pydantic import BaseModel

                @tool
                def weak_search_docs(query: str) -> str:
                    \"\"\"Search docs and return a free-form sentence.\"\"\"
                    return f"Found some notes about {query}, maybe in the docs folder."

                class SearchResult(BaseModel):
                    source: str
                    relevance: float
                    summary: str

                @tool
                def strong_search_docs(query: str) -> dict:
                    \"\"\"Search local course docs and return a stable structured payload.\"\"\"
                    return SearchResult(
                        source="docs/references.md",
                        relevance=0.82,
                        summary=f"Structured notes relevant to {query}",
                    ).model_dump()

                print_json(
                    {
                        "weak_return": weak_search_docs("tool design"),
                        "strong_return": strong_search_docs("tool design"),
                    },
                    title="Contract comparison",
                )
                """,
            ),
            (
                "Design a tool suite with minimal overlap",
                """
                @tool
                def list_course_docs() -> list[str]:
                    \"\"\"List high-level course docs available in the repo.\"\"\"
                    root = resolve_notebook_root() / "docs"
                    return sorted(path.name for path in root.glob("*.md"))

                @tool
                def read_course_doc(name: str) -> str:
                    \"\"\"Read a single markdown document from the docs folder.\"\"\"
                    path = resolve_notebook_root() / "docs" / name
                    if not path.exists():
                        return f"Document {name} does not exist."
                    return path.read_text(encoding="utf-8")[:1000]

                @tool
                def summarize_learning_goal(step: int) -> str:
                    \"\"\"Return a short learning-goal summary for a core course step.\"\"\"
                    summaries = {
                        4: "Understand tool definitions, signatures, and registration.",
                        9: "Build a local RAG loop with retrieval and grounded prompting.",
                        12: "Compare orchestration patterns and choose the right one.",
                    }
                    return summaries.get(step, "No summary registered for that step.")
                """,
            ),
            (
                "Ask the model to create a tool plan",
                """
                planner = create_agent(
                    name="ToolPlanner",
                    instructions=(
                        "You are a systems-thinking assistant. "
                        "When you answer, explain which tool seems appropriate and why."
                    ),
                    tools=[list_course_docs, read_course_doc, summarize_learning_goal],
                )

                plan_response = await planner.run(
                    "I need the docs file that best explains provider setup, and also the goal of Step 12."
                )
                print(plan_response.text)
                """,
            ),
            (
                "Inspect a manual multi-step tool workflow",
                """
                docs = list_course_docs()
                provider_doc_name = next((name for name in docs if "providers" in name), docs[0])
                provider_doc_excerpt = read_course_doc(provider_doc_name)
                step_goal = summarize_learning_goal(12)

                print_json(
                    {
                        "available_docs": docs,
                        "chosen_doc": provider_doc_name,
                        "step_goal": step_goal,
                        "excerpt_preview": provider_doc_excerpt[:240],
                    },
                    title="Manual tool chain inspection",
                )
                """,
            ),
        ],
        "exercise_1_prompt": "Refactor a weak tool so it returns a stable dictionary payload with clear field names and no ambiguous prose.",
        "exercise_1_starter": """
        # TODO: replace this weak return shape with a structured dictionary
        def weak_lookup(topic: str):
            return f"maybe helpful notes about {topic}"
        """,
        "exercise_1_solution": """
        def strong_lookup(topic: str) -> dict:
            return {
                "topic": topic,
                "status": "ok",
                "source": "local_reference",
                "summary": f"Helpful notes about {topic}",
            }

        print_json(strong_lookup("workflow routing"), title="Exercise 1 solution")
        """,
        "exercise_2_prompt": "Design two tool descriptions so the model can clearly distinguish when to list documents versus when to read one document.",
        "exercise_2_starter": """
        # TODO: write short explanation bullets for how you would keep these tools distinct
        tool_a_description = ""
        tool_b_description = ""
        """,
        "exercise_2_solution": """
        tool_a_description = "List document names only. Use this when the user does not yet know which file they need."
        tool_b_description = "Read one named document. Use this only after the target file is already known."

        print_json(
            {"list_tool": tool_a_description, "read_tool": tool_b_description},
            title="Exercise 2 solution",
        )
        """,
        "best_practices": [
            "Prefer structured outputs whenever another tool or prompt step will consume the result.",
            "Keep tool purpose boundaries sharp so the model can choose reliably.",
            "Treat tool descriptions as part of the interface contract, not optional decoration.",
            "Inspect manual tool chains before assuming the model should compose them automatically.",
        ],
        "summary": "You moved from basic tools to deliberate tool-interface design, with stronger attention to schema shape, overlap, and multi-step planning.",
        "resources": [
            "helpers/llm.py",
            "docs/references.md",
            "core notebook: 04_understanding_tools.ipynb",
        ],
    },
    {
        "number": 17,
        "slug": "17_intermediate_context_engineering_and_memory_patterns.ipynb",
        "title": "Intermediate: Context Engineering and Memory Patterns",
        "level": "Intermediate",
        "duration": "90 minutes",
        "objectives": [
            "Separate active session state from durable memory and injected context.",
            "Build prompt-ready context blocks from stored history.",
            "Introduce summarization and pruning strategies for long conversations.",
            "Reason about what should and should not be remembered.",
        ],
        "prerequisites": [
            "Core Steps 3 and 8 completed.",
            "Comfort with basic session management and SQLite examples.",
        ],
        "intro": "Context engineering is often more important than adding another model call. This notebook focuses on what context to keep, how to compress it, and how to inject it without polluting the conversation.",
        "implementation": [
            (
                "Create separate short-term and long-term stores",
                """
                from agent_framework import AgentSession

                session = AgentSession(session_id="context-lab")
                memory = SQLiteConversationMemory(resolve_notebook_root() / "data" / "databases" / "context_lab.sqlite3")

                context_agent = create_agent(
                    name="ContextAgent",
                    instructions="You are a context-aware assistant. Prefer concise answers and use prior notes only when relevant.",
                )
                """,
            ),
            (
                "Capture durable memory candidates",
                """
                interactions = [
                    ("sam", "My name is Sam and I lead platform tooling."),
                    ("sam", "I prefer examples in Python, not pseudocode."),
                    ("sam", "Please keep explanations short unless I ask for depth."),
                ]

                for user_id, prompt in interactions:
                    reply = await context_agent.run(prompt, session=session)
                    memory.save(user_id, prompt, reply.text)

                print_json([row.__dict__ for row in memory.history("sam", limit=5)], title="Persisted memory rows")
                """,
            ),
            (
                "Build a reusable context injector",
                """
                def build_context_block(user_id: str, *, limit: int = 3) -> str:
                    rows = list(reversed(memory.history(user_id, limit=limit)))
                    if not rows:
                        return ""
                    bullets = "\\n".join(f"- {row.user_message}" for row in rows)
                    return f"Known user context:\\n{bullets}"

                context_block = build_context_block("sam")
                print(context_block)
                """,
            ),
            (
                "Summarize and prune older conversation details",
                """
                def summarize_history(user_id: str, *, limit: int = 5) -> dict:
                    rows = list(reversed(memory.history(user_id, limit=limit)))
                    summary = {
                        "identity": [],
                        "preferences": [],
                        "current_focus": [],
                    }
                    for row in rows:
                        text = row.user_message.lower()
                        if "my name is" in text or "i lead" in text:
                            summary["identity"].append(row.user_message)
                        elif "prefer" in text or "keep explanations" in text:
                            summary["preferences"].append(row.user_message)
                        else:
                            summary["current_focus"].append(row.user_message)
                    return summary

                print_json(summarize_history("sam"), title="Summarized memory view")
                """,
            ),
        ],
        "exercise_1_prompt": "Write a helper that chooses whether a memory item belongs in identity, preference, or temporary-context buckets.",
        "exercise_1_starter": """
        def classify_memory_item(text: str) -> str:
            # TODO: return one of: identity, preference, temporary
            return "temporary"
        """,
        "exercise_1_solution": """
        def classify_memory_item(text: str) -> str:
            lowered = text.lower()
            if "my name is" in lowered or "i lead" in lowered or "i work on" in lowered:
                return "identity"
            if "prefer" in lowered or "keep explanations" in lowered:
                return "preference"
            return "temporary"

        print_json(
            {
                "name": classify_memory_item("My name is Sam."),
                "preference": classify_memory_item("I prefer Python examples."),
                "temporary": classify_memory_item("Can you summarize this issue?"),
            },
            title="Exercise 1 solution",
        )
        """,
        "exercise_2_prompt": "Create a prompt template that injects only preference memories, not every stored interaction.",
        "exercise_2_starter": """
        # TODO: build a short prompt template that includes only preference notes
        """,
        "exercise_2_solution": """
        summary = summarize_history("sam")
        preference_prompt = (
            "Use the following stable preferences when you answer.\\n"
            + "\\n".join(f"- {item}" for item in summary["preferences"])
            + "\\n\\nUser request: Explain how workflow fan-out differs from branching."
        )
        print(preference_prompt)
        """,
        "best_practices": [
            "Store only memory that is likely to matter again.",
            "Inject summarized context rather than raw transcripts whenever possible.",
            "Separate stable preferences from temporary task details.",
            "Treat context formatting as an explicit design problem, not a cleanup step.",
        ],
        "summary": "You deepened the memory story by shaping context deliberately instead of replaying whole conversations.",
        "resources": [
            "helpers/memory.py",
            "core notebook: 08_memory_and_sessions.ipynb",
            "core notebook: 03_multi_turn_conversations.ipynb",
        ],
    },
    {
        "number": 18,
        "slug": "18_intermediate_workflow_patterns_with_typed_executors.ipynb",
        "title": "Intermediate: Workflow Patterns with Typed Executors",
        "level": "Intermediate",
        "duration": "100 minutes",
        "objectives": [
            "Use typed executors for clearer workflow contracts.",
            "Model fan-out, fan-in, and branch selection explicitly.",
            "Inspect workflow outputs and intermediate routing decisions.",
            "Practice workflow debugging with small deterministic nodes before adding live agents.",
        ],
        "prerequisites": [
            "Core Steps 10 and 11 completed.",
        ],
        "intro": "This notebook adds more depth to the workflow material by focusing on typed executors, graph shape, and the debugging mindset needed when data moves across several nodes.",
        "implementation": [
            (
                "Create typed extractor and classifier nodes",
                """
                from typing_extensions import Never
                from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler

                class NormalizeRequest(Executor):
                    @handler
                    async def process(self, text: str, ctx: WorkflowContext[dict]) -> None:
                        await ctx.send_message({"raw": text, "normalized": text.lower().strip()})

                class ClassifyRequest(Executor):
                    @handler
                    async def process(self, payload: dict, ctx: WorkflowContext[dict]) -> None:
                        normalized = payload["normalized"]
                        route = "technical" if "python" in normalized or "workflow" in normalized else "general"
                        await ctx.send_message({"route": route, **payload})
                """,
            ),
            (
                "Add route-specific executors",
                """
                class TechnicalPath(Executor):
                    @handler
                    async def process(self, payload: dict, ctx: WorkflowContext[str]) -> None:
                        await ctx.send_message(f"TECH ANALYSIS: {payload['raw']}")

                class GeneralPath(Executor):
                    @handler
                    async def process(self, payload: dict, ctx: WorkflowContext[str]) -> None:
                        await ctx.send_message(f"GENERAL ANALYSIS: {payload['raw']}")

                class FinalReporter(Executor):
                    @handler
                    async def process(self, summary: str, ctx: WorkflowContext[Never, str]) -> None:
                        await ctx.yield_output(f"FINAL OUTPUT: {summary}")

                normalize = NormalizeRequest(id="normalize")
                classify = ClassifyRequest(id="classify")
                technical = TechnicalPath(id="technical")
                general = GeneralPath(id="general")
                reporter = FinalReporter(id="reporter")
                """,
            ),
            (
                "Build branching and fan-in into one workflow",
                """
                workflow = (
                    WorkflowBuilder(start_executor=normalize)
                    .add_edge(normalize, classify)
                    .add_edge(classify, technical, condition=lambda payload: payload["route"] == "technical")
                    .add_edge(classify, general, condition=lambda payload: payload["route"] == "general")
                    .add_edge(technical, reporter)
                    .add_edge(general, reporter)
                    .build()
                )

                print((await workflow.run("How do workflow edges affect Python agent design?")).get_outputs())
                print((await workflow.run("Give me a short summary of the course.")).get_outputs())
                """,
            ),
            (
                "Inspect message-shape assumptions",
                """
                examples = [
                    {"route": "technical", "raw": "Explain workflow fan-out."},
                    {"route": "general", "raw": "Summarize the docs."},
                ]

                print_json(
                    {
                        "normalize_output_shape": {"raw": "text", "normalized": "text"},
                        "classify_output_examples": examples,
                    },
                    title="Workflow message contracts",
                )
                """,
            ),
        ],
        "exercise_1_prompt": "Add a third route for risk-sensitive requests, and create a dedicated executor for it.",
        "exercise_1_starter": """
        # TODO: extend the routing logic with a risk-sensitive path
        """,
        "exercise_1_solution": """
        class RiskPath(Executor):
            @handler
            async def process(self, payload: dict, ctx: WorkflowContext[str]) -> None:
                await ctx.send_message(f"RISK REVIEW: {payload['raw']}")

        risk = RiskPath(id="risk")
        print("Created a dedicated risk-review executor.")
        """,
        "exercise_2_prompt": "Write a helper that prints which executor should receive a message based on the payload.",
        "exercise_2_starter": """
        def explain_route(payload: dict) -> str:
            # TODO: map payload route values to executor names
            return ""
        """,
        "exercise_2_solution": """
        def explain_route(payload: dict) -> str:
            mapping = {
                "technical": "technical",
                "general": "general",
                "risk": "risk",
            }
            return mapping.get(payload["route"], "unknown")

        print_json(
            {
                "technical": explain_route({"route": "technical"}),
                "general": explain_route({"route": "general"}),
                "risk": explain_route({"route": "risk"}),
            },
            title="Exercise 2 solution",
        )
        """,
        "best_practices": [
            "Design message shapes before writing edge conditions.",
            "Use deterministic executors first when debugging graph behavior.",
            "Keep each executor narrowly responsible for one transformation step.",
            "Make route labels explicit so you can inspect them later.",
        ],
        "summary": "You pushed past simple chains and treated workflows as typed graphs with inspectable contracts and debugging surfaces.",
        "resources": [
            "core notebook: 10_basic_workflows.ipynb",
            "core notebook: 11_conditional_workflows.ipynb",
            "docs/references.md",
        ],
    },
    {
        "number": 19,
        "slug": "19_advanced_multi_agent_evaluation_and_trace_analysis.ipynb",
        "title": "Advanced: Multi-Agent Evaluation and Trace Analysis",
        "level": "Advanced",
        "duration": "110 minutes",
        "objectives": [
            "Build a lightweight evaluation loop for agent outputs.",
            "Compare agent behavior against explicit rubric criteria.",
            "Capture simple traces and review failure patterns.",
            "Use evaluation results to guide prompt and orchestration changes.",
        ],
        "prerequisites": [
            "Core Steps 12-15 completed.",
            "Comfort reviewing prompt and orchestration outputs critically.",
        ],
        "intro": "Advanced agent work is iterative. This notebook makes evaluation and trace review part of the development loop instead of something added after deployment.",
        "implementation": [
            (
                "Create a tiny evaluation dataset",
                """
                eval_cases = [
                    {
                        "query": "Explain why tool descriptions matter.",
                        "expected_keywords": ["tool", "description", "model", "selection"],
                    },
                    {
                        "query": "What is the difference between branching and fan-out in workflows?",
                        "expected_keywords": ["branch", "fan-out", "workflow", "route"],
                    },
                ]

                judge = create_agent(
                    name="JudgeAgent",
                    instructions="Score answers from 0 to 5 for clarity, correctness, and usefulness. Return a short justification.",
                )
                candidate = create_agent(
                    name="CandidateAgent",
                    instructions="Answer course questions clearly for developers learning agent systems.",
                )
                """,
            ),
            (
                "Generate answers and record traces",
                """
                traces = []
                for case in eval_cases:
                    answer = await candidate.run(case["query"])
                    trace = {
                        "query": case["query"],
                        "answer": answer.text,
                        "keyword_hits": [kw for kw in case["expected_keywords"] if kw.lower() in answer.text.lower()],
                    }
                    traces.append(trace)

                print_json(traces, title="Candidate traces")
                """,
            ),
            (
                "Ask a judge model for qualitative review",
                """
                judged = []
                for trace in traces:
                    review = await judge.run(
                        f\"\"\"Question: {trace['query']}
                        Answer: {trace['answer']}
                        Score the answer from 0 to 5 and explain why.\"\"\"
                    )
                    judged.append({**trace, "judge_review": review.text})

                print_json(judged, title="Judged traces")
                """,
            ),
            (
                "Summarize recurring failure modes",
                """
                def trace_summary(items: list[dict]) -> dict:
                    return {
                        "case_count": len(items),
                        "average_keyword_hits": sum(len(item["keyword_hits"]) for item in items) / len(items),
                        "common_risk": "Answers may sound polished even when they omit required vocabulary.",
                    }

                print_json(trace_summary(judged), title="Evaluation summary")
                """,
            ),
        ],
        "exercise_1_prompt": "Add a new evaluation case that targets orchestration tradeoffs rather than definitions.",
        "exercise_1_starter": """
        # TODO: append a third eval case with expected keywords
        """,
        "exercise_1_solution": """
        eval_cases.append(
            {
                "query": "When should you prefer sequential orchestration over concurrent orchestration?",
                "expected_keywords": ["sequential", "concurrent", "dependency", "parallel"],
            }
        )
        print_json(eval_cases[-1], title="Exercise 1 solution")
        """,
        "exercise_2_prompt": "Write a helper that flags traces with fewer than two keyword hits as risky outputs.",
        "exercise_2_starter": """
        def flag_risky_trace(trace: dict) -> bool:
            # TODO: implement risk flagging
            return False
        """,
        "exercise_2_solution": """
        def flag_risky_trace(trace: dict) -> bool:
            return len(trace["keyword_hits"]) < 2

        print_json(
            [flag_risky_trace(trace) for trace in traces],
            title="Exercise 2 solution",
        )
        """,
        "best_practices": [
            "Keep evaluation cases small enough to inspect manually at first.",
            "Combine quantitative checks with rubric-style reviews.",
            "Store traces in a form that makes failure analysis easy later.",
            "Use evaluation to refine prompts, tool contracts, or orchestration shape.",
        ],
        "summary": "You turned evaluation and trace review into a repeatable engineering loop instead of a vague quality goal.",
        "resources": [
            "core notebook: 15_production_features.ipynb",
            "docs/references.md",
        ],
    },
    {
        "number": 20,
        "slug": "20_advanced_human_approval_and_checkpointed_workflows.ipynb",
        "title": "Advanced: Human Approval and Checkpointed Workflows",
        "level": "Advanced",
        "duration": "105 minutes",
        "objectives": [
            "Design approval boundaries for risky actions.",
            "Persist enough workflow state to resume reliably.",
            "Differentiate audit records from execution payloads.",
            "Think through operator-facing workflow recovery paths.",
        ],
        "prerequisites": [
            "Core Step 14 completed.",
        ],
        "intro": "This advanced notebook treats human oversight as a system design problem: what requires approval, what state must be saved, and how operators re-enter an interrupted flow safely.",
        "implementation": [
            (
                "Define auditable approval records",
                """
                from dataclasses import dataclass, asdict
                from datetime import datetime

                @dataclass
                class ApprovalRecord:
                    approval_id: str
                    action: str
                    reason: str
                    payload: dict
                    requested_at: str
                    status: str = "pending"

                approvals: dict[str, ApprovalRecord] = {}
                """,
            ),
            (
                "Create explicit checkpoint snapshots",
                """
                checkpoint_store: dict[str, dict] = {}

                def save_checkpoint(name: str, payload: dict) -> None:
                    checkpoint_store[name] = {
                        "saved_at": datetime.utcnow().isoformat(),
                        "payload": payload,
                    }

                def load_checkpoint(name: str) -> dict:
                    return checkpoint_store[name]["payload"]
                """,
            ),
            (
                "Model a gated workflow stage",
                """
                def request_approval(action: str, reason: str, payload: dict) -> ApprovalRecord:
                    approval_id = f"approval_{len(approvals) + 1}"
                    record = ApprovalRecord(
                        approval_id=approval_id,
                        action=action,
                        reason=reason,
                        payload=payload,
                        requested_at=datetime.utcnow().isoformat(),
                    )
                    approvals[approval_id] = record
                    return record

                def approve(approval_id: str) -> None:
                    approvals[approval_id].status = "approved"

                def reject(approval_id: str) -> None:
                    approvals[approval_id].status = "rejected"
                """,
            ),
            (
                "Run a checkpointed approval flow",
                """
                draft_report = {
                    "dataset": "quarterly_launch_notes",
                    "risk_level": "high",
                    "action": "publish_external_summary",
                }
                save_checkpoint("draft_created", draft_report)

                approval = request_approval(
                    action="publish_external_summary",
                    reason="External publication requires human review.",
                    payload=draft_report,
                )
                approve(approval.approval_id)

                print_json(asdict(approval), title="Approval record")
                print_json(load_checkpoint("draft_created"), title="Checkpoint payload")
                """,
            ),
        ],
        "exercise_1_prompt": "Add a second checkpoint after approval so the resume path can tell whether it should continue to publication or return to review.",
        "exercise_1_starter": """
        # TODO: save a second checkpoint that represents post-approval state
        """,
        "exercise_1_solution": """
        save_checkpoint(
            "approved_for_publication",
            {"next_stage": "publish", "approval_id": approval.approval_id, "status": approval.status},
        )
        print_json(load_checkpoint("approved_for_publication"), title="Exercise 1 solution")
        """,
        "exercise_2_prompt": "Write a resume helper that decides the next action based on the latest checkpoint state.",
        "exercise_2_starter": """
        def resume_decision(checkpoint_name: str) -> str:
            # TODO: return the next action string
            return ""
        """,
        "exercise_2_solution": """
        def resume_decision(checkpoint_name: str) -> str:
            payload = load_checkpoint(checkpoint_name)
            if payload.get("next_stage") == "publish":
                return "continue_to_publication"
            return "return_to_review"

        print_json(
            {"decision": resume_decision("approved_for_publication")},
            title="Exercise 2 solution",
        )
        """,
        "best_practices": [
            "Define approvals around business risk, not around arbitrary complexity.",
            "Save checkpoints that are meaningful to operators, not just to code.",
            "Record approval and execution state separately for cleaner audit trails.",
            "Design resume logic before you need it in an outage or long-running task.",
        ],
        "summary": "You deepened the HITL pattern into an auditable, resumable workflow design rather than a single approval prompt.",
        "resources": [
            "core notebook: 14_human_in_the_loop.ipynb",
            "docs/troubleshooting.md",
        ],
    },
    {
        "number": 21,
        "slug": "21_advanced_provider_strategy_and_production_hardening.ipynb",
        "title": "Advanced: Provider Strategy and Production Hardening",
        "level": "Advanced",
        "duration": "110 minutes",
        "objectives": [
            "Reason about provider selection as a product and operations decision.",
            "Design fallback and degradation behavior explicitly.",
            "Track latency, rough cost, and failure categories together.",
            "Create a hardening checklist for production-ready agent applications.",
        ],
        "prerequisites": [
            "Core Step 15 completed.",
        ],
        "intro": "This notebook turns production readiness into concrete decision-making. Instead of only measuring one call, you will reason about provider strategy, failure handling, and graceful degradation.",
        "implementation": [
            (
                "Model provider policies",
                """
                provider_policy = {
                    "primary": "openrouter",
                    "secondary": "azure_openai",
                    "max_latency_seconds": 8.0,
                    "max_estimated_cost_usd": 0.05,
                    "fallback_on_errors": {"timeout", "rate_limit", "temporary_unavailable"},
                }

                print_json(provider_policy, title="Provider policy")
                """,
            ),
            (
                "Capture an execution record shape",
                """
                def execution_record(provider: str, latency: float, estimated_cost: float, status: str) -> dict:
                    return {
                        "provider": provider,
                        "latency_seconds": latency,
                        "estimated_cost_usd": estimated_cost,
                        "status": status,
                    }

                records = [
                    execution_record("openrouter", 2.1, 0.004, "ok"),
                    execution_record("azure_openai", 6.8, 0.011, "ok"),
                    execution_record("openrouter", 9.4, 0.004, "timeout"),
                ]
                print_json(records, title="Execution records")
                """,
            ),
            (
                "Design fallback logic explicitly",
                """
                def should_fallback(record: dict, policy: dict) -> bool:
                    if record["status"] in policy["fallback_on_errors"]:
                        return True
                    if record["latency_seconds"] > policy["max_latency_seconds"]:
                        return True
                    return False

                fallback_decisions = [should_fallback(record, provider_policy) for record in records]
                print_json(fallback_decisions, title="Fallback decisions")
                """,
            ),
            (
                "Build a production hardening checklist",
                """
                hardening_checklist = [
                    "Define provider failure categories and fallback rules.",
                    "Log latency, estimated token usage, and status per request.",
                    "Add health checks for provider credentials and endpoint reachability.",
                    "Document degraded-mode behavior for operators and users.",
                    "Review prompt, tool, and workflow changes with evaluation traces.",
                ]
                print_json(hardening_checklist, title="Hardening checklist")
                """,
            ),
        ],
        "exercise_1_prompt": "Add a degraded-mode response strategy for when both primary and secondary providers fail.",
        "exercise_1_starter": """
        def degraded_mode_response(user_request: str) -> str:
            # TODO: return a safe degraded-mode message
            return ""
        """,
        "exercise_1_solution": """
        def degraded_mode_response(user_request: str) -> str:
            return (
                "The live providers are temporarily unavailable. "
                "Return a cached explanation, queue the request for retry, or ask the user to try again later."
            )

        print_json(
            {"degraded_mode": degraded_mode_response("Explain tool orchestration tradeoffs.")},
            title="Exercise 1 solution",
        )
        """,
        "exercise_2_prompt": "Write a helper that classifies each execution record as healthy, degraded, or failed.",
        "exercise_2_starter": """
        def classify_runtime_state(record: dict, policy: dict) -> str:
            # TODO: implement runtime classification
            return "healthy"
        """,
        "exercise_2_solution": """
        def classify_runtime_state(record: dict, policy: dict) -> str:
            if record["status"] != "ok":
                return "failed"
            if record["latency_seconds"] > policy["max_latency_seconds"] or record["estimated_cost_usd"] > policy["max_estimated_cost_usd"]:
                return "degraded"
            return "healthy"

        print_json(
            [classify_runtime_state(record, provider_policy) for record in records],
            title="Exercise 2 solution",
        )
        """,
        "best_practices": [
            "Treat provider choice as an operating policy, not only a config flag.",
            "Define degraded behavior before failures happen in production.",
            "Track cost, latency, and status together so tradeoffs are visible.",
            "Revisit hardening rules whenever prompts, tools, or workflows change materially.",
        ],
        "summary": "You extended the production story from basic metrics to explicit provider strategy, degradation handling, and operational hardening.",
        "resources": [
            "core notebook: 15_production_features.ipynb",
            "docs/llm_providers.md",
            "docs/depth_expansion_plan.md",
        ],
    },
]


SUPPORT_FILES = {
    "data/documents/python_basics.txt": dedent(
        """
        Python is a general-purpose programming language known for readability, batteries-included tooling,
        and a large ecosystem. Functions, modules, and objects make it a practical language for building
        scripts, services, data workflows, and agent applications. Python's async features let developers
        coordinate network-bound tasks without blocking the whole program.
        """
    ).strip()
    + "\n",
    "data/documents/async_patterns.txt": dedent(
        """
        Async programming is useful when tasks spend time waiting on network or file I/O. With async and await,
        one coroutine can yield control while another continues, which improves throughput for concurrency-heavy
        systems such as API-backed tools, retrieval pipelines, and orchestration loops.
        """
    ).strip()
    + "\n",
    "data/documents/agent_system_design.txt": dedent(
        """
        Agent systems become more reliable when prompts, tools, memory, and orchestration are designed as
        separate concerns. Tools reduce hallucination for deterministic operations. Memory helps personalize
        behavior over time. Workflows and orchestration make control flow explicit and easier to debug.
        """
    ).strip()
    + "\n",
    "data/examples/support_requests.json": json.dumps(
        [
            {"id": 1, "category": "technical", "message": "My notebook cannot import agent_framework."},
            {"id": 2, "category": "billing", "message": "How do we track monthly model spend?"},
            {"id": 3, "category": "general", "message": "What is the learning path for this course?"},
        ],
        indent=2,
    )
    + "\n",
    "data/examples/workflow_inputs.json": json.dumps(
        [
            {"topic": "agent tools", "audience": "engineers"},
            {"topic": "rag pipelines", "audience": "platform teams"},
            {"topic": "human approvals", "audience": "security reviewers"},
        ],
        indent=2,
    )
    + "\n",
    "data/databases/starter_schema.sql": dedent(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            user_message TEXT NOT NULL,
            agent_response TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    ).strip()
    + "\n",
    "data/databases/README.md": dedent(
        """
        # Database Assets

        This folder contains starter assets for the memory notebooks.

        - `starter_schema.sql` shows the SQLite schema used in the course
        - generated runtime databases such as `memory_demo.sqlite3` are intentionally ignored
        """
    ).strip()
    + "\n",
}


def build_intro(step: dict, *, solution_mode: bool) -> str:
    objectives = "\n".join(f"- [ ] {item}" for item in step["objectives"])
    prerequisites = "\n".join(f"- {item}" for item in step["prerequisites"])
    notebook_kind = "Instructor Solution Notebook" if solution_mode else "Learner Notebook"
    return dedent(
        f"""
        # Step {step['number']}: {step['title']}

        _{notebook_kind}_  
        Estimated time: **{step['duration']}**  
        Difficulty: **{step['difficulty']}**

        ## Learning Objectives
        {objectives}

        ## Prerequisites
        {prerequisites}
        """
    ).strip()


def build_toc() -> str:
    return dedent(
        """
        ## Table of Contents

        1. Setup & Imports
        2. Part 1: Introduction
        3. Part 2: Core Implementation
        4. Part 3: Hands-On Exercises
        5. Part 4: Solutions & Discussion
        6. Part 5: Best Practices & Tips
        7. Summary & Key Takeaways
        8. Additional Resources
        """
    ).strip()


def build_setup_markdown() -> str:
    return dedent(
        """
        ## Setup & Imports

        The next cell adds the repository root to `sys.path` and imports the shared course helpers.
        Most notebooks use the same bootstrap so the lesson content can stay focused on the concept,
        not on path setup.
        """
    ).strip()


def build_intro_markdown(step: dict) -> str:
    return dedent(
        f"""
        ## Part 1: Introduction

        {step['intro'].strip()}

        Expected output and validation notes:

        {step['expected_output'].strip()}
        """
    ).strip()


def build_implementation_markdown(title: str) -> str:
    return dedent(
        f"""
        ## Part 2: Core Implementation

        ### {title}
        """
    ).strip()


def build_exercise_markdown(step: dict, *, solution_mode: bool) -> str:
    mode_note = (
        "This mirrored notebook uses completed exercise code so instructors can demonstrate the target state."
        if solution_mode
        else "Try the exercise yourself before looking at the solutions in Part 4."
    )
    return dedent(
        f"""
        ## Part 3: Hands-On Exercises

        {step['exercise_prompt']}

        {mode_note}
        """
    ).strip()


def build_solution_markdown() -> str:
    return dedent(
        """
        ## Part 4: Solutions & Discussion

        Use this section to compare your implementation with one clear working approach. The goal is not
        perfect matching output; the goal is a sound pattern that is easy to explain, debug, and extend.
        """
    ).strip()


def build_best_practices_markdown(step: dict) -> str:
    bullets = "\n".join(f"- {item}" for item in step["best_practices"])
    return dedent(
        f"""
        ## Part 5: Best Practices & Tips

        {bullets}
        """
    ).strip()


def build_summary_markdown(step: dict) -> str:
    return dedent(
        f"""
        ## Summary & Key Takeaways

        {step['summary']}
        """
    ).strip()


def build_resources_markdown(step: dict) -> str:
    bullets = "\n".join(f"- `{item}`" for item in step["resources"])
    return dedent(
        f"""
        ## Additional Resources

        {bullets}
        """
    ).strip()


def build_supplemental_intro(step: dict, *, solution_mode: bool) -> str:
    objectives = "\n".join(f"- [ ] {item}" for item in step["objectives"])
    prerequisites = "\n".join(f"- {item}" for item in step["prerequisites"])
    notebook_kind = "Instructor Solution Notebook" if solution_mode else "Learner Notebook"
    return dedent(
        f"""
        # Step {step['number']}: {step['title']}

        _{notebook_kind}_  
        Level: **{step['level']}**  
        Estimated time: **{step['duration']}**

        ## Learning Objectives
        {objectives}

        ## Prerequisites
        {prerequisites}
        """
    ).strip()


def build_supplemental_toc() -> str:
    return dedent(
        """
        ## Table of Contents

        1. Setup & Imports
        2. Part 1: Introduction
        3. Part 2: Core Implementation
        4. Part 3: Hands-On Exercises
        5. Part 4: Solutions & Discussion
        6. Part 5: Best Practices & Tips
        7. Reflection & Next Experiments
        8. Summary & Key Takeaways
        9. Additional Resources
        """
    ).strip()


def build_supplemental_setup() -> str:
    return dedent(
        """
        ## Setup & Imports

        Supplemental notebooks assume the core helpers are available and that you have already worked
        through the matching core lessons. The import cell intentionally keeps the same bootstrap shape
        as the core course so you can focus on the deeper pattern rather than environment setup.
        """
    ).strip()


def build_supplemental_intro_markdown(step: dict) -> str:
    return dedent(
        f"""
        ## Part 1: Introduction

        {step['intro']}

        This notebook is intentionally deeper than the core path. Expect more design discussion,
        more implementation sections, and more open-ended exercises.
        """
    ).strip()


def build_supplemental_exercises_markdown(step: dict, *, solution_mode: bool) -> str:
    note = (
        "This solution notebook includes completed code for both guided exercises."
        if solution_mode
        else "Work through both guided exercises before comparing against the solutions."
    )
    return dedent(
        f"""
        ## Part 3: Hands-On Exercises

        ### Exercise 1
        {step['exercise_1_prompt']}

        ### Exercise 2
        {step['exercise_2_prompt']}

        {note}
        """
    ).strip()


def build_reflection_markdown(step: dict) -> str:
    return dedent(
        f"""
        ## Reflection & Next Experiments

        - Which part of `{step['title']}` felt like the biggest jump from the core course?
        - What would you keep deterministic before turning this into a live production feature?
        - Where would you add tests, traces, or operator controls before shipping this pattern?
        """
    ).strip()


def make_notebook(step: dict, *, solution_mode: bool) -> dict:
    exercise_code = step["exercise_solution"] if solution_mode else step["exercise_starter"]
    cells = [
        markdown_cell(build_intro(step, solution_mode=solution_mode)),
        markdown_cell(build_toc()),
        markdown_cell(build_setup_markdown()),
        code_cell(COMMON_SETUP_CODE),
        markdown_cell(build_intro_markdown(step)),
    ]

    for title, code in step["implementation"]:
        cells.append(markdown_cell(build_implementation_markdown(title)))
        cells.append(code_cell(code))

    cells.extend(
        [
            markdown_cell(build_exercise_markdown(step, solution_mode=solution_mode)),
            code_cell(exercise_code),
            markdown_cell(build_solution_markdown()),
            code_cell(step["exercise_solution"]),
            markdown_cell(build_best_practices_markdown(step)),
            markdown_cell(build_summary_markdown(step)),
            markdown_cell(build_resources_markdown(step)),
        ]
    )

    return {
        "cells": cells,
        "metadata": NOTEBOOK_METADATA,
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def make_supplemental_notebook(step: dict, *, solution_mode: bool) -> dict:
    exercise_one_code = step["exercise_1_solution"] if solution_mode else step["exercise_1_starter"]
    exercise_two_code = step["exercise_2_solution"] if solution_mode else step["exercise_2_starter"]

    cells = [
        markdown_cell(build_supplemental_intro(step, solution_mode=solution_mode)),
        markdown_cell(build_supplemental_toc()),
        markdown_cell(build_supplemental_setup()),
        code_cell(COMMON_SETUP_CODE),
        markdown_cell(build_supplemental_intro_markdown(step)),
    ]

    for title, code in step["implementation"]:
        cells.append(markdown_cell(build_implementation_markdown(title)))
        cells.append(code_cell(code))

    cells.extend(
        [
            markdown_cell(build_supplemental_exercises_markdown(step, solution_mode=solution_mode)),
            code_cell(exercise_one_code),
            code_cell(exercise_two_code),
            markdown_cell(build_solution_markdown()),
            code_cell(step["exercise_1_solution"]),
            code_cell(step["exercise_2_solution"]),
            markdown_cell(build_best_practices_markdown(step)),
            markdown_cell(build_reflection_markdown(step)),
            markdown_cell(build_summary_markdown(step)),
            markdown_cell(build_resources_markdown(step)),
        ]
    )

    return {
        "cells": cells,
        "metadata": NOTEBOOK_METADATA,
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate_support_files() -> None:
    for relative_path, content in SUPPORT_FILES.items():
        write_text(REPO_ROOT / relative_path, content)


def generate_notebooks() -> None:
    for step in STEP_DEFINITIONS:
        learner_path = NOTEBOOKS_DIR / step["slug"]
        solution_path = SOLUTIONS_DIR / step["slug"]
        write_json(learner_path, make_notebook(step, solution_mode=False))
        write_json(solution_path, make_notebook(step, solution_mode=True))

    for step in SUPPLEMENTAL_NOTEBOOKS:
        learner_path = SUPPLEMENTAL_NOTEBOOKS_DIR / step["slug"]
        solution_path = SUPPLEMENTAL_SOLUTIONS_DIR / step["slug"]
        write_json(learner_path, make_supplemental_notebook(step, solution_mode=False))
        write_json(solution_path, make_supplemental_notebook(step, solution_mode=True))


def main() -> int:
    generate_support_files()
    generate_notebooks()
    print("Generated learner notebooks, solution notebooks, and support assets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
