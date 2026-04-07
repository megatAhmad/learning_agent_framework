# Detailed Notebook Specifications
## Microsoft Agent Framework Mastery Program - 15 Steps

---

## Notebook Metadata Standards

Each notebook should have:

```python
{
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.9.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 4
}
```

---

## Step-by-Step Specifications

### STEP 1: Setup & Environment Configuration
**File**: `01_setup_and_environment.ipynb`  
**Duration**: 30 minutes  
**Difficulty**: ⭐ Beginner

#### Learning Objectives
- [ ] Create and activate Python virtual environment
- [ ] Install all required packages
- [ ] Configure API keys for OpenRouter or Azure OpenAI
- [ ] Verify environment is working correctly
- [ ] Understand project structure

#### Notebook Sections

**Section 1: Introduction (Markdown)**
- Welcome message
- Course overview
- What you'll accomplish

**Section 2: System Check (Code)**
```python
# Check Python version
import sys
print(f"Python version: {sys.version}")
assert sys.version_info >= (3, 9), "Python 3.9+ required"

# Check operating system
import platform
print(f"OS: {platform.system()}")
```

**Section 3: Virtual Environment Setup (Markdown + Code)**
- Instructions for venv creation
- Installation script
- Verification steps

**Section 4: Package Installation (Code)**
```python
# Display required packages
required_packages = {
    "agent-framework": "1.0.0",
    "python-dotenv": "1.0.0",
    "jupyter": "1.0.0",
    "openai": "1.3.0",
    "aiohttp": "3.8.0"
}

for package, version in required_packages.items():
    print(f"pip install {package}>={version}")
```

**Section 5: Environment Configuration (Code + Markdown)**
- .env file creation
- API key explanation
- Provider selection

**Section 6: Verification Tests (Code)**
```python
# Test OpenRouter connectivity
# Test Azure OpenAI connectivity
# Verify agent-framework import
```

**Section 7: Troubleshooting (Markdown)**
- Common issues and solutions
- Help resources
- Next steps

#### Key Code Elements
- Environment variable loading with `python-dotenv`
- Package import verification
- API key validation
- Provider switching example

#### Exercises
1. Create virtual environment
2. Install packages
3. Configure API keys
4. Run verification tests

#### Expected Output
```
✓ Python 3.9.x detected
✓ All packages installed successfully
✓ API keys configured
✓ OpenRouter connectivity verified
✓ Ready to start Step 2!
```

---

### STEP 2: Your First Agent
**File**: `02_your_first_agent.ipynb`  
**Duration**: 45 minutes  
**Difficulty**: ⭐ Beginner

#### Learning Objectives
- [ ] Create an Agent instance
- [ ] Run agent with a simple prompt
- [ ] Understand agent anatomy (client, name, instructions)
- [ ] Examine agent responses
- [ ] Switch between LLM providers

#### Notebook Sections

**1. Introduction & Concepts**
- What is an agent?
- Agent anatomy diagram (ASCII)
- Key components explained

**2. Creating Your First Agent (Code)**
```python
from agent_framework import Agent
from helpers.llm_client import get_agent

# Create agent
agent = get_agent(
    name="FirstAgent",
    instructions="You are a helpful Python programming assistant."
)

print(f"✓ Agent created: {agent.name}")
```

**3. Running the Agent (Code)**
```python
import asyncio

async def run_agent():
    response = await agent.run("What is Python?")
    print(f"Response: {response}")

asyncio.run(run_agent())
```

**4. Examining Responses (Code)**
```python
# Check response structure
# Display response metadata
# Measure response time
# Count tokens
```

**5. Prompt Engineering (Code)**
- Simple prompts
- Detailed prompts
- System message impact

**6. Provider Switching (Code)**
```python
# Switch to different provider
agent_azure = get_agent(
    name="AzureAgent",
    instructions="...",
    provider="azure_openai"
)
```

**7. Best Practices (Markdown)**
- Clear instructions
- Specific prompts
- Response handling

#### Exercises
1. Create agent with custom instructions
2. Ask agent 3 different questions
3. Compare responses from different providers
4. Modify system instructions and observe impact

#### Expected Output
```
Agent: FirstAgent
Response: [Python explanation]
Tokens used: 45
Time: 0.87 seconds
Model: meta-llama/llama-2-70b-chat
```

---

### STEP 3: Multi-Turn Conversations
**File**: `03_multi_turn_conversations.ipynb`  
**Duration**: 45 minutes  
**Difficulty**: ⭐ Beginner

#### Learning Objectives
- [ ] Create and manage agent sessions
- [ ] Maintain conversation history
- [ ] Understand context preservation
- [ ] Build interactive chatbots
- [ ] Handle session lifecycle

#### Notebook Sections

**1. Sessions Concept (Markdown + Diagrams)**
- What are sessions?
- Session lifecycle
- Context windows

**2. Creating Sessions (Code)**
```python
from agent_framework import AgentSession

session = AgentSession(
    id="user_123",
    max_messages=20
)

agent = get_agent(
    name="ChatBot",
    instructions="You are a helpful assistant.",
    session=session
)
```

**3. Multi-Turn Example (Code)**
```python
async def multi_turn_chat():
    response1 = await agent.run("My name is Alice")
    print(f"Turn 1: {response1}")
    
    response2 = await agent.run("What's my name?")
    print(f"Turn 2: {response2}")
    
    response3 = await agent.run("Tell me a joke")
    print(f"Turn 3: {response3}")
```

**4. Conversation History (Code)**
```python
# Inspect conversation history
# Display message count
# Show context windows
```

**5. Session Management (Code)**
```python
# Save session state
# Load previous session
# Clear conversation history
```

**6. Interactive Chat Loop (Code)**
```python
async def interactive_chat():
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        response = await agent.run(user_input)
        print(f"Bot: {response}")
```

**7. Common Issues (Markdown)**
- Token limits
- Context window overflow
- Memory management

#### Exercises
1. Create a multi-turn conversation (5 turns)
2. Build an interactive Q&A chatbot
3. Implement session persistence
4. Handle token limit scenarios

#### Expected Output
```
Session ID: user_123
Messages: 6
Context Window: 85% utilized

Turn 1: Alice said her name
Turn 2: Agent correctly recalled "Alice"
Turn 3: Agent continued conversation
```

---

### STEP 4: Understanding Tools
**File**: `04_understanding_tools.ipynb`  
**Duration**: 60 minutes  
**Difficulty**: ⭐⭐ Intermediate

#### Learning Objectives
- [ ] Understand tool concepts and anatomy
- [ ] Define functions as tools
- [ ] Use type annotations correctly
- [ ] Register tools with agents
- [ ] Inspect and debug tools

#### Notebook Sections

**1. Tool Concepts (Markdown)**
- What are tools?
- Why use tools?
- Tool anatomy diagram
- Function signature requirements

**2. Defining Simple Tools (Code)**
```python
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

def get_current_time() -> str:
    """Get the current time."""
    from datetime import datetime
    return datetime.now().isoformat()
```

**3. Type Annotations (Code)**
```python
# Required type annotations
from typing import List, Dict, Optional

def process_data(items: List[str]) -> Dict[str, int]:
    """Process a list of items."""
    return {item: len(item) for item in items}
```

**4. Tool Documentation (Code)**
```python
# Docstrings become tool descriptions
def calculate_discount(
    original_price: float,
    discount_percent: float
) -> float:
    """
    Calculate the discounted price.
    
    Args:
        original_price: The original item price
        discount_percent: Discount percentage (0-100)
    
    Returns:
        The final price after discount
    """
    return original_price * (1 - discount_percent / 100)
```

**5. Tool Registration (Code)**
```python
# Register with agent
agent = get_agent(
    name="Calculator",
    instructions="You are a helpful calculator assistant."
)

agent.tools.register(add_numbers)
agent.tools.register(get_current_time)
agent.tools.register(process_data)
```

**6. Tool Inspection (Code)**
```python
# List all tools
print(f"Available tools: {list(agent.tools.keys())}")

# Inspect specific tool
tool_info = agent.tools.get_info("add_numbers")
print(f"Tool: {tool_info}")
```

**7. Tool Error Handling (Code)**
```python
def safe_divide(a: float, b: float) -> float:
    """Divide two numbers safely."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

#### Exercises
1. Create 5 different tool functions
2. Register tools with agent
3. Inspect tool metadata
4. Implement error handling in tools
5. Document tools properly

#### Expected Output
```
Available tools: ['add_numbers', 'get_current_time', 'process_data']

Tool info for 'add_numbers':
  Description: Add two numbers together.
  Parameters: a (int), b (int)
  Returns: int
```

---

### STEP 5: Single Tool Integration
**File**: `05_single_tool_integration.ipynb`  
**Duration**: 60 minutes  
**Difficulty**: ⭐⭐ Intermediate

#### Learning Objectives
- [ ] Integrate a real-world tool (weather API)
- [ ] Handle tool invocation by agents
- [ ] Process tool responses
- [ ] Handle errors gracefully
- [ ] Debug tool execution

#### Notebook Sections

**1. Real-World Tool Example (Markdown)**
- Weather API tool overview
- API documentation
- Expected behavior

**2. Implementing Weather Tool (Code)**
```python
def get_weather(city: str) -> str:
    """
    Get weather information for a city.
    
    Args:
        city: Name of the city
    
    Returns:
        Weather information string
    """
    # Simulated weather data
    weather_data = {
        "Paris": "Sunny, 22°C, light breeze",
        "New York": "Cloudy, 15°C, occasional rain",
        "Tokyo": "Rainy, 18°C, humid",
        "London": "Overcast, 14°C, cool"
    }
    
    if city in weather_data:
        return f"Weather in {city}: {weather_data[city]}"
    else:
        return f"Weather data not available for {city}"
```

**3. Registering Tool with Agent (Code)**
```python
agent = get_agent(
    name="WeatherBot",
    instructions="You are a helpful weather assistant. Use the weather tool to answer questions about weather."
)

agent.tools.register(get_weather)
```

**4. Agent Using Tools (Code)**
```python
async def test_tool_usage():
    # Agent decides to use tool
    response = await agent.run("What's the weather in Paris?")
    print(f"Response: {response}")
```

**5. Tool Invocation Flow (Markdown + Diagram)**
```
User Input
    ↓
Agent analyzes
    ↓
Agent decides to call get_weather("Paris")
    ↓
Tool executes
    ↓
Response returned to agent
    ↓
Agent formats final response
    ↓
User receives answer
```

**6. Error Handling (Code)**
```python
def safe_get_weather(city: str) -> str:
    """Get weather with error handling."""
    try:
        return get_weather(city)
    except Exception as e:
        return f"Error getting weather: {str(e)}"
```

**7. Debugging Tool Calls (Code)**
```python
# Add logging to see when tools are called
import logging
logging.basicConfig(level=logging.INFO)

# Inspect tool calls
# Monitor execution time
# Check return values
```

#### Exercises
1. Implement weather tool with more cities
2. Make agent use tool for multiple queries
3. Add error handling for edge cases
4. Implement fallback responses
5. Debug tool execution with logging

#### Expected Output
```
Q: "What's the weather in Paris?"

Agent reasoning: User is asking about weather
Agent decision: Call get_weather("Paris")
Tool result: "Weather in Paris: Sunny, 22°C, light breeze"

Final response: "The weather in Paris is sunny, 22 degrees Celsius with a light breeze."
```

---

### STEP 6: Multiple Tools
**File**: `06_multiple_tools.ipynb`  
**Duration**: 60 minutes  
**Difficulty**: ⭐⭐ Intermediate

#### Learning Objectives
- [ ] Create multiple coordinated tools
- [ ] Understand agent decision-making
- [ ] Coordinate tool usage
- [ ] Handle conflicting outputs
- [ ] Implement tool priorities

#### Notebook Sections

**1. Multi-Tool Architecture (Markdown)**
- Multiple tool patterns
- Tool selection logic
- Coordination strategies

**2. Defining Multiple Tools (Code)**
```python
# Tool 1: Calculator
def calculate(expression: str) -> float:
    """Evaluate a mathematical expression."""
    return eval(expression)

# Tool 2: Unit Converter
def convert_temperature(celsius: float, to_fahrenheit: bool = True) -> float:
    """Convert temperature between Celsius and Fahrenheit."""
    if to_fahrenheit:
        return (celsius * 9/5) + 32
    return (celsius - 32) * 5/9

# Tool 3: Time Tool
def get_current_time() -> str:
    """Get current date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Tool 4: Weather
def get_weather(city: str) -> str:
    """Get weather for a city."""
    # [Same as Step 5]
    pass
```

**3. Registering Multiple Tools (Code)**
```python
agent = get_agent(
    name="MultiToolBot",
    instructions="""You are a helpful assistant with access to multiple tools:
    - Calculator: for math problems
    - Temperature converter: for temperature conversions
    - Time: for current time
    - Weather: for weather information
    
    Use the appropriate tool for each query."""
)

agent.tools.register(calculate)
agent.tools.register(convert_temperature)
agent.tools.register(get_current_time)
agent.tools.register(get_weather)
```

**4. Agent Tool Selection (Code)**
```python
async def test_multiple_tools():
    queries = [
        "What is 15 + 27 * 3?",          # Calls calculate
        "Convert 100°C to Fahrenheit",   # Calls convert_temperature
        "What time is it?",              # Calls get_current_time
        "What's the weather in Paris?"   # Calls get_weather
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        response = await agent.run(query)
        print(f"Response: {response}")
```

**5. Tool Chaining (Code + Markdown)**
- When multiple tools are needed
- Sequencing tool calls
- Example: "It's 0°C, convert to Fahrenheit and add 10 degrees"

**6. Handling Conflicting Tools (Markdown)**
- When multiple tools could apply
- Agent decision-making
- Best practices

**7. Tool Priority (Code)**
```python
# Tool ordering affects selection
agent.tools.register(calculate, priority=1)  # Higher priority
agent.tools.register(get_weather, priority=2)
```

#### Exercises
1. Create 4-5 different tools
2. Register all tools with agent
3. Test tool selection with various queries
4. Implement tool chaining
5. Debug agent tool selection

#### Expected Output
```
Test 1: Math query
  Selected tool: calculate
  Result: 426

Test 2: Temperature query
  Selected tool: convert_temperature
  Result: 212°F

Test 3: Time query
  Selected tool: get_current_time
  Result: 2024-04-07 10:30:45

Test 4: Weather query
  Selected tool: get_weather
  Result: Sunny, 22°C
```

---

### STEP 7: Custom Tools & API Integration
**File**: `07_custom_tools_and_apis.ipynb`  
**Duration**: 75 minutes  
**Difficulty**: ⭐⭐⭐ Intermediate-Advanced

#### Learning Objectives
- [ ] Integrate with real REST APIs
- [ ] Handle async tool implementations
- [ ] Implement error handling and retries
- [ ] Manage API authentication
- [ ] Optimize API usage

#### Notebook Sections

**1. REST API Concepts (Markdown)**
- HTTP methods (GET, POST)
- Headers and authentication
- Error codes and handling
- Rate limiting

**2. Simple REST Tool (Code)**
```python
import aiohttp
import asyncio

async def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                
                if data['query']['search']:
                    # Return top 3 results
                    results = []
                    for item in data['query']['search'][:3]:
                        results.append(f"- {item['title']}: {item['snippet'][:100]}...")
                    return "\n".join(results)
                else:
                    return "No results found"
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"
```

**3. Error Handling Patterns (Code)**
```python
async def get_with_retry(url: str, max_retries: int = 3) -> dict:
    """GET request with retry logic."""
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"Status {response.status}, retrying...")
        except asyncio.TimeoutError:
            print(f"Timeout on attempt {attempt + 1}")
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")
        
        if attempt < max_retries - 1:
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    raise Exception("Max retries exceeded")
```

**4. Authentication & Headers (Code)**
```python
async def authenticated_request(
    url: str,
    api_key: str,
    endpoint: str
) -> dict:
    """Make authenticated API request."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"{url}/{endpoint}") as response:
            return await response.json()
```

**5. Async Tool Implementation (Code)**
```python
# Tools can be async
async def fetch_data(url: str) -> str:
    """Async tool for fetching data."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                return text[:500]  # Return first 500 chars
            else:
                return f"Error: {response.status}"

# Register async tool
agent.tools.register(fetch_data)
```

**6. Rate Limiting & Throttling (Code)**
```python
import time
from functools import wraps

def rate_limit(calls_per_second: float):
    """Decorator to rate limit tool calls."""
    min_interval = 1 / calls_per_second
    last_called = [0]
    
    def decorator(func):
        async def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                await asyncio.sleep(min_interval - elapsed)
            
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limit(calls_per_second=2)
async def rate_limited_tool(query: str) -> str:
    """Tool with rate limiting."""
    return f"Result for {query}"
```

**7. Tool Data Transformation (Code)**
```python
async def fetch_and_parse(url: str) -> dict:
    """Fetch and transform API response."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            
            # Transform the data
            return {
                "status": response.status,
                "item_count": len(data.get("items", [])),
                "summary": data.get("description", "No description")
            }
```

#### Exercises
1. Implement Wikipedia search tool
2. Add error handling and retries
3. Implement rate limiting
4. Create authenticated API tool
5. Handle JSON transformation

#### Expected Output
```
Query: "Tell me about Python"

Tool: search_wikipedia
API: https://en.wikipedia.org/w/api.php
Status: 200 OK
Results: 3 matches found

Response: "Python is a high-level programming language..."
```

---

### STEP 8: Memory & Sessions
**File**: `08_memory_and_sessions.ipynb`  
**Duration**: 60 minutes  
**Difficulty**: ⭐⭐ Intermediate

#### Learning Objectives
- [ ] Implement persistent user memory
- [ ] Manage session state across turns
- [ ] Store and retrieve user context
- [ ] Handle memory limits
- [ ] Implement memory cleanup

#### Notebook Sections

**1. Memory Concepts (Markdown)**
- Session vs memory distinction
- Persistence strategies
- Context window limits
- User profiles

**2. Session State Management (Code)**
```python
from agent_framework import AgentSession

# Create session with metadata
session = AgentSession(
    id="user_alice_2024",
    max_messages=50,
    metadata={
        "user_name": "Alice",
        "company": "TechCorp",
        "role": "Engineer",
        "preferences": {"language": "Python"}
    }
)

agent = get_agent(
    name="ContextAwareBot",
    instructions="You are a helpful assistant aware of user context.",
    session=session
)
```

**3. User Context Tools (Code)**
```python
def get_user_context(session: AgentSession) -> dict:
    """Retrieve user context from session."""
    return {
        "name": session.metadata.get("user_name"),
        "company": session.metadata.get("company"),
        "role": session.metadata.get("role")
    }

def update_user_preference(
    session: AgentSession,
    key: str,
    value: str
) -> None:
    """Update user preference in session."""
    if "preferences" not in session.metadata:
        session.metadata["preferences"] = {}
    session.metadata["preferences"][key] = value
```

**4. Conversation Summarization (Code)**
```python
def summarize_conversation(messages: list, max_summary_length: int = 200) -> str:
    """Summarize conversation history."""
    if len(messages) < 3:
        return ""
    
    # Keep recent messages, summarize older ones
    summary = "Previous conversation context: "
    for i, msg in enumerate(messages[:-3]):
        if msg.role == "user":
            summary += f"User asked about {msg.text[:50]}... "
    
    return summary[:max_summary_length]
```

**5. Persistent Memory with SQLite (Code)**
```python
import sqlite3
import json
from datetime import datetime

class PersistentMemory:
    """Store conversation history in SQLite."""
    
    def __init__(self, db_path: str = "memory.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                timestamp TEXT,
                user_message TEXT,
                agent_response TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save(self, user_id: str, user_msg: str, agent_resp: str):
        """Save conversation to memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (user_id, timestamp, user_message, agent_response)
            VALUES (?, ?, ?, ?)
        ''', (user_id, datetime.now().isoformat(), user_msg, agent_resp))
        
        conn.commit()
        conn.close()
    
    def retrieve(self, user_id: str, limit: int = 5) -> list:
        """Retrieve conversation history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_message, agent_response FROM conversations
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
```

**6. Memory Usage Pattern (Code)**
```python
async def remembered_chat():
    memory = PersistentMemory()
    
    # First turn
    response1 = await agent.run("My name is Alice")
    memory.save("alice_user", "My name is Alice", response1)
    
    # Later session - retrieve memory
    previous = memory.retrieve("alice_user", limit=1)
    if previous:
        context = f"User previously said: {previous[0][0]}"
        
        response2 = await agent.run(
            f"{context}\nWhat's my name?"
        )
        print(f"Response: {response2}")
```

**7. Memory Cleanup (Code)**
```python
def cleanup_old_messages(
    messages: list,
    keep_count: int = 10
) -> list:
    """Keep only recent messages to manage memory."""
    if len(messages) > keep_count:
        # Keep last N messages
        return messages[-keep_count:]
    return messages
```

#### Exercises
1. Implement user context storage
2. Build SQLite-based memory
3. Retrieve and use past context
4. Implement memory cleanup
5. Test multi-session conversations

#### Expected Output
```
Session 1:
  User: "My name is Alice"
  Agent: "Nice to meet you, Alice!"

Session 2 (later):
  System: Loading memory for alice_user
  User: "What's my name?"
  Agent: "Your name is Alice, nice to talk with you again!"
```

---

### STEP 9: RAG Implementation
**File**: `09_rag_implementation.ipynb`  
**Duration**: 75 minutes  
**Difficulty**: ⭐⭐⭐ Intermediate-Advanced

#### Learning Objectives
- [ ] Load and process documents
- [ ] Implement semantic search
- [ ] Create embeddings
- [ ] Build RAG pipeline
- [ ] Retrieve and inject context

#### Notebook Sections

**1. RAG Concepts (Markdown)**
- Retrieval-Augmented Generation overview
- Why RAG matters
- RAG pipeline diagram
- Document processing

**2. Document Loading (Code)**
```python
from pathlib import Path

def load_documents(documents_dir: str) -> list[dict]:
    """Load documents from directory."""
    documents = []
    
    for doc_path in Path(documents_dir).glob("*.txt"):
        with open(doc_path, 'r') as f:
            content = f.read()
            documents.append({
                "id": doc_path.stem,
                "title": doc_path.stem.replace('_', ' '),
                "content": content
            })
    
    return documents

# Load sample documents
docs = load_documents("data/documents")
print(f"Loaded {len(docs)} documents")
```

**3. Document Chunking (Code)**
```python
def chunk_documents(
    documents: list[dict],
    chunk_size: int = 300,
    overlap: int = 50
) -> list[dict]:
    """Split documents into chunks."""
    chunks = []
    
    for doc in documents:
        text = doc["content"]
        
        # Split into overlapping chunks
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            chunks.append({
                "id": f"{doc['id']}_chunk_{i}",
                "source": doc["id"],
                "content": chunk
            })
    
    return chunks

chunks = chunk_documents(docs)
print(f"Created {len(chunks)} chunks from documents")
```

**4. Simple Vector Similarity (Code)**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleVectorStore:
    """Simple in-memory vector store using TF-IDF."""
    
    def __init__(self):
        self.documents = []
        self.vectorizer = None
        self.vectors = None
    
    def add_documents(self, documents: list[dict]):
        """Add documents to store."""
        self.documents = documents
        
        # Create TF-IDF vectors
        texts = [doc["content"] for doc in documents]
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english'
        )
        self.vectors = self.vectorizer.fit_transform(texts)
    
    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """Search for similar documents."""
        # Vectorize query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarity
        similarities = cosine_similarity(query_vector, self.vectors)[0]
        
        # Get top results
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "document": self.documents[idx],
                "score": float(similarities[idx])
            })
        
        return results
```

**5. RAG Pipeline (Code)**
```python
class RAGSystem:
    """Complete RAG system."""
    
    def __init__(self, documents: list[dict]):
        self.vector_store = SimpleVectorStore()
        self.vector_store.add_documents(documents)
        
        self.agent = get_agent(
            name="RAGBot",
            instructions="""You are a helpful assistant with access to documents.
            Answer questions based on the provided context.
            If information is not in the context, say so."""
        )
    
    async def query(self, question: str) -> str:
        """Query the RAG system."""
        # Retrieve relevant documents
        results = self.vector_store.search(question, top_k=3)
        
        # Format context
        context = "\n".join([
            f"Document: {r['document']['source']}\n{r['document']['content']}"
            for r in results
        ])
        
        # Create prompt with context
        prompt = f"""Context from documents:
{context}

User question: {question}

Answer based on the provided context."""
        
        # Get agent response
        response = await self.agent.run(prompt)
        
        return response
```

**6. Complete Example (Code)**
```python
async def rag_example():
    # Load documents
    documents = load_documents("data/documents")
    
    # Create RAG system
    rag = RAGSystem(documents)
    
    # Ask questions
    questions = [
        "What is Python?",
        "How do you define a function?",
        "What are the benefits of using async/await?"
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        answer = await rag.query(question)
        print(f"A: {answer}")

await rag_example()
```

**7. RAG Evaluation (Code)**
```python
def evaluate_rag_response(
    response: str,
    expected_keywords: list[str]
) -> float:
    """Evaluate RAG response quality."""
    response_lower = response.lower()
    
    matched = sum(
        1 for keyword in expected_keywords
        if keyword.lower() in response_lower
    )
    
    return matched / len(expected_keywords) if expected_keywords else 0
```

#### Exercises
1. Load and chunk sample documents
2. Build vector store
3. Implement search functionality
4. Create complete RAG pipeline
5. Evaluate response quality

#### Expected Output
```
Documents loaded: 3
Chunks created: 15

Query: "What is Python?"

Retrieved contexts:
  - document_1 (score: 0.85)
  - document_2 (score: 0.72)
  - document_3 (score: 0.68)

Response: "Python is a high-level programming language..."
Quality score: 0.95
```

---

### STEP 10: Basic Workflows
**File**: `10_basic_workflows.ipynb`  
**Duration**: 75 minutes  
**Difficulty**: ⭐⭐ Intermediate

#### Learning Objectives
- [ ] Create workflow builder
- [ ] Add agents as executors
- [ ] Define edges (connections)
- [ ] Execute sequential workflows
- [ ] Handle workflow state

#### Notebook Sections

**1. Workflow Concepts (Markdown)**
- Workflow vs agent
- Workflow anatomy
- Executors and edges
- Data flow diagram

**2. Creating Workflow Builder (Code)**
```python
from agent_framework import WorkflowBuilder

# Create builder
builder = WorkflowBuilder()

# Define agents
extractor = get_agent(
    name="Extractor",
    instructions="Extract key information from text"
)

analyzer = get_agent(
    name="Analyzer",
    instructions="Analyze the extracted information"
)

reporter = get_agent(
    name="Reporter",
    instructions="Create a summary report"
)
```

**3. Adding Executors (Code)**
```python
# Add agents as executors
builder.add_executor("extract_step", extractor)
builder.add_executor("analyze_step", analyzer)
builder.add_executor("report_step", reporter)

print("✓ Executors added")
```

**4. Defining Edges (Code)**
```python
# Define workflow connections
builder.add_edge("input", "extract_step")      # Input → Extract
builder.add_edge("extract_step", "analyze_step")  # Extract → Analyze
builder.add_edge("analyze_step", "report_step")   # Analyze → Report
builder.add_edge("report_step", "output")     # Report → Output

print("✓ Workflow edges defined")
```

**5. Building and Executing (Code)**
```python
async def execute_workflow():
    # Build workflow
    workflow = builder.build()
    
    # Prepare input
    input_text = """
    The technology industry is evolving rapidly.
    Artificial Intelligence is becoming mainstream.
    Companies are investing heavily in AI development.
    """
    
    # Execute workflow
    print("Executing workflow...")
    result = await workflow.run(input_text)
    
    print(f"\nFinal result:\n{result}")

await execute_workflow()
```

**6. Workflow Visualization (Code)**
```python
# Visualize workflow structure
def print_workflow_structure(builder):
    """Print workflow as ASCII diagram."""
    print("""
    [Input]
        ↓
    [Extract Agent]
        ↓
    [Analyze Agent]
        ↓
    [Report Agent]
        ↓
    [Output]
    """)

print_workflow_structure(builder)
```

**7. Workflow Debugging (Code)**
```python
async def debug_workflow():
    workflow = builder.build()
    
    # Enable debug output
    input_text = "Test input"
    
    # Execute with monitoring
    result = await workflow.run(input_text)
    
    # Print workflow state
    print("Workflow execution completed")
    return result
```

#### Exercises
1. Create 3-step sequential workflow
2. Build data processing pipeline
3. Visualize workflow structure
4. Execute workflow with test data
5. Debug workflow execution

#### Expected Output
```
[Input Text]
    ↓ 
[Extract]: Extracted 5 key points
    ↓
[Analyze]: Analysis of extracted data
    ↓
[Report]: Final formatted report
    ↓
[Output]: Complete workflow result

Status: ✓ Workflow completed successfully
Execution time: 3.45 seconds
```

---

### STEP 11: Conditional Workflows
**File**: `11_conditional_workflows.ipynb`  
**Duration**: 75 minutes  
**Difficulty**: ⭐⭐⭐ Intermediate-Advanced

#### Learning Objectives
- [ ] Add conditional logic to workflows
- [ ] Implement branching paths
- [ ] Create decision nodes
- [ ] Handle errors in workflows
- [ ] Route based on conditions

#### Notebook Sections

**1. Conditional Logic (Markdown)**
- Why conditional workflows?
- Decision patterns
- Branching strategies
- Error handling paths

**2. Decision Functions (Code)**
```python
def classify_input(text: str) -> str:
    """Classify input to route to correct agent."""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["python", "code", "program"]):
        return "technical"
    elif any(word in text_lower for word in ["python", "company", "business"]):
        return "business"
    else:
        return "general"

async def decision_node(input_text: str) -> tuple[str, str]:
    """Decision node that classifies and routes."""
    category = classify_input(input_text)
    return category, input_text
```

**3. Building Conditional Workflow (Code)**
```python
async def build_conditional_workflow():
    builder = WorkflowBuilder()
    
    # Create specialized agents
    tech_agent = get_agent(
        name="TechSpecialist",
        instructions="Answer technical questions about Python and programming"
    )
    
    business_agent = get_agent(
        name="BusinessSpecialist",
        instructions="Answer business and company questions"
    )
    
    general_agent = get_agent(
        name="GeneralAssistant",
        instructions="Answer general questions"
    )
    
    # Add agents
    builder.add_executor("tech", tech_agent)
    builder.add_executor("business", business_agent)
    builder.add_executor("general", general_agent)
```

**4. Conditional Routing (Code)**
```python
# Simplified conditional routing
async def route_workflow(text: str):
    category = classify_input(text)
    
    if category == "technical":
        agent = tech_agent
        name = "technical path"
    elif category == "business":
        agent = business_agent
        name = "business path"
    else:
        agent = general_agent
        name = "general path"
    
    result = await agent.run(text)
    
    return {
        "category": category,
        "path": name,
        "response": result
    }
```

**5. Error Handling Paths (Code)**
```python
async def workflow_with_error_handling():
    builder = WorkflowBuilder()
    
    # Main agents
    primary = get_agent(
        name="PrimaryAgent",
        instructions="Try to process the request"
    )
    
    fallback = get_agent(
        name="FallbackAgent",
        instructions="Handle requests the primary agent couldn't process"
    )
    
    # Add both paths
    builder.add_executor("primary", primary)
    builder.add_executor("fallback", fallback)
    
    # Main flow
    builder.add_edge("input", "primary")
    
    # Error/fallback path
    # In real implementation, this would be conditional
    
    return builder
```

**6. Complex Branching Example (Code)**
```python
async def multi_branch_workflow(input_data: str):
    """Workflow with multiple conditional branches."""
    
    # Step 1: Classify
    classification = classify_input(input_data)
    
    # Step 2: Route based on classification
    if classification == "technical":
        # Technical branch
        tech_response = await tech_agent.run(input_data)
        
        # Step 3a: Code review if needed
        if "code" in input_data.lower():
            review = await code_reviewer.run(tech_response)
            return review
        else:
            return tech_response
    
    elif classification == "business":
        # Business branch
        business_response = await business_agent.run(input_data)
        
        # Step 3b: Get second opinion
        second_opinion = await analyst.run(business_response)
        
        return f"{business_response}\n\nAdditional analysis:\n{second_opinion}"
    
    else:
        # General branch
        return await general_agent.run(input_data)
```

**7. Workflow Visualization (Code)**
```python
def visualize_conditional_workflow():
    """ASCII visualization of conditional workflow."""
    print("""
    ┌─────────────┐
    │   Input     │
    └──────┬──────┘
           │
     ┌─────▼──────┐
     │  Classify  │
     └─┬──────┬──┬┘
       │      │  │
       ▼      ▼  ▼
     Tech   Biz Gen
     │      │  │
     └──┬───┴──┘
        │
    ┌───▼────────┐
    │   Output   │
    └────────────┘
    """)
```

#### Exercises
1. Create classification function
2. Build conditional workflow
3. Implement branching logic
4. Add error handling paths
5. Test different input routes

#### Expected Output
```
Input: "How do I write a Python function?"
  ↓
Classification: technical
  ↓
Route: Tech Specialist Agent
  ↓
Response: "To write a Python function..."

Status: ✓ Routed correctly to technical agent
```

---

### STEP 12: Orchestration Patterns
**File**: `12_orchestration_patterns.ipynb`  
**Duration**: 90 minutes  
**Difficulty**: ⭐⭐⭐ Advanced

#### Learning Objectives
- [ ] Understand sequential orchestration
- [ ] Implement concurrent execution
- [ ] Use handoff patterns
- [ ] Compare pattern tradeoffs
- [ ] Choose appropriate patterns

#### Notebook Sections

**1. Orchestration Patterns Overview (Markdown)**
- Pattern comparison table
- Sequential pattern
- Concurrent pattern
- Handoff pattern
- When to use each

**2. Sequential Orchestration (Code)**
```python
async def sequential_example():
    """
    Step 1: Research Agent finds information
    ↓
    Step 2: Analysis Agent analyzes findings
    ↓
    Step 3: Report Agent creates report
    """
    
    researcher = get_agent(
        name="Researcher",
        instructions="Research and gather information on topics"
    )
    
    analyst = get_agent(
        name="Analyst",
        instructions="Analyze research findings"
    )
    
    reporter = get_agent(
        name="Reporter",
        instructions="Create comprehensive reports"
    )
    
    # Sequential execution
    task = "Research AI trends in 2024"
    
    print("Step 1: Researching...")
    research = await researcher.run(task)
    
    print("Step 2: Analyzing...")
    analysis = await analyst.run(research)
    
    print("Step 3: Reporting...")
    report = await reporter.run(analysis)
    
    return report
```

**3. Concurrent Orchestration (Code)**
```python
import asyncio

async def concurrent_example():
    """
    All agents execute simultaneously
    
    ├─ Social Media Analyzer ─┐
    │                        ├─ Aggregate Results
    ├─ News Analyzer ────────┤
    │                        │
    └─ Market Analyzer ──────┘
    """
    
    social_agent = get_agent(
        name="SocialAnalyzer",
        instructions="Analyze social media trends"
    )
    
    news_agent = get_agent(
        name="NewsAnalyzer",
        instructions="Analyze news trends"
    )
    
    market_agent = get_agent(
        name="MarketAnalyzer",
        instructions="Analyze market trends"
    )
    
    # Execute in parallel
    task = "Analyze AI market trends"
    
    results = await asyncio.gather(
        social_agent.run(task),
        news_agent.run(task),
        market_agent.run(task)
    )
    
    # Aggregate results
    aggregated = "\n".join([
        f"Social Media: {results[0]}",
        f"News: {results[1]}",
        f"Market: {results[2]}"
    ])
    
    return aggregated
```

**4. Handoff Orchestration (Code)**
```python
async def handoff_example():
    """
    Triage Agent classifies request
    ↓
    Routes to specialized agent:
    ├─ Technical Support Agent
    ├─ Billing Support Agent
    └─ General Support Agent
    """
    
    triage = get_agent(
        name="Triage",
        instructions="Classify support requests: technical, billing, or general"
    )
    
    tech_support = get_agent(
        name="TechSupport",
        instructions="Handle technical issues"
    )
    
    billing_support = get_agent(
        name="BillingSupport",
        instructions="Handle billing questions"
    )
    
    general_support = get_agent(
        name="GeneralSupport",
        instructions="Handle general inquiries"
    )
    
    # Customer request
    request = "My password isn't working"
    
    # Triage
    print("Triaging request...")
    classification = await triage.run(f"Classify this: {request}")
    
    # Handoff based on classification
    if "technical" in classification.lower():
        print("Handing off to Technical Support...")
        response = await tech_support.run(request)
    elif "billing" in classification.lower():
        print("Handing off to Billing Support...")
        response = await billing_support.run(request)
    else:
        print("Handing off to General Support...")
        response = await general_support.run(request)
    
    return response
```

**5. Pattern Comparison (Code)**
```python
def compare_patterns():
    """Compare orchestration patterns."""
    
    comparison = {
        "Sequential": {
            "pros": ["Simple", "Deterministic", "Easy to debug"],
            "cons": ["Slower", "No parallelism"],
            "use_case": "Linear pipelines"
        },
        "Concurrent": {
            "pros": ["Fast", "Parallel execution", "Scalable"],
            "cons": ["Complex aggregation", "Harder to debug"],
            "use_case": "Independent parallel tasks"
        },
        "Handoff": {
            "pros": ["Specialized handling", "Clear routing"],
            "cons": ["More agents needed", "Classification overhead"],
            "use_case": "Task-specific processing"
        }
    }
    
    for pattern, details in comparison.items():
        print(f"\n{pattern}:")
        print(f"  Pros: {', '.join(details['pros'])}")
        print(f"  Cons: {', '.join(details['cons'])}")
        print(f"  Use case: {details['use_case']}")

compare_patterns()
```

**6. Performance Comparison (Code)**
```python
import time

async def benchmark_patterns():
    """Benchmark different patterns."""
    
    task = "Analyze complex data"
    
    # Sequential timing
    start = time.time()
    # ... sequential execution
    sequential_time = time.time() - start
    
    # Concurrent timing
    start = time.time()
    # ... concurrent execution
    concurrent_time = time.time() - start
    
    print(f"Sequential: {sequential_time:.2f}s")
    print(f"Concurrent: {concurrent_time:.2f}s")
    print(f"Speedup: {sequential_time/concurrent_time:.1f}x")
```

**7. Choosing Patterns (Code)**
```python
def choose_pattern(task_description: str) -> str:
    """Recommend orchestration pattern."""
    
    if any(word in task_description.lower() for word in ["pipeline", "then", "after"]):
        return "Sequential"
    
    elif any(word in task_description.lower() for word in ["parallel", "multiple", "together"]):
        return "Concurrent"
    
    elif any(word in task_description.lower() for word in ["route", "classify", "direct"]):
        return "Handoff"
    
    else:
        return "Sequential (default)"

# Test recommendation
tasks = [
    "Process data then analyze then report",
    "Analyze 3 different data sources in parallel",
    "Route customer request to appropriate department"
]

for task in tasks:
    pattern = choose_pattern(task)
    print(f"Task: {task}")
    print(f"Recommended pattern: {pattern}\n")
```

#### Exercises
1. Implement sequential orchestration
2. Build concurrent system
3. Create handoff workflow
4. Compare execution times
5. Choose pattern for use case

#### Expected Output
```
Pattern Comparison:

Sequential:
  Pros: Simple, Easy debugging
  Cons: Slower execution
  Time: 9.34 seconds

Concurrent:
  Pros: Fast, Parallel
  Cons: Complex aggregation
  Time: 3.12 seconds

Speedup: 3.0x faster
Recommended for this task: Concurrent
```

---

### STEP 13: Advanced Orchestration
**File**: `13_advanced_orchestration.ipynb`  
**Duration**: 90 minutes  
**Difficulty**: ⭐⭐⭐ Advanced

#### Learning Objectives
- [ ] Implement group chat orchestration
- [ ] Understand Magentic One pattern
- [ ] Coordinate complex agent teams
- [ ] Handle streaming responses
- [ ] Manage long-running orchestrations

#### Notebook Sections

**1. Group Chat Orchestration (Markdown + Code)**
- Multiple agents discuss together
- Shared conversation context
- Consensus building
- When to use group chat

**2. Group Chat Implementation (Code)**
```python
class GroupChat:
    """Multi-agent group chat."""
    
    def __init__(self, agents: list, max_turns: int = 10):
        self.agents = agents
        self.max_turns = max_turns
        self.conversation = []
        self.current_agent_idx = 0
    
    async def run(self, initial_prompt: str) -> str:
        """Run group chat."""
        print(f"Topic: {initial_prompt}\n")
        
        # Initialize conversation
        self.conversation.append({
            "role": "system",
            "content": initial_prompt
        })
        
        # Run conversation
        for turn in range(self.max_turns):
            # Get current agent
            agent = self.agents[self.current_agent_idx]
            
            # Build prompt with conversation history
            history = "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in self.conversation[-5:]  # Last 5 messages
            ])
            
            # Get response
            response = await agent.run(
                f"Conversation so far:\n{history}\n\nYour response:"
            )
            
            # Add to conversation
            self.conversation.append({
                "role": agent.name,
                "content": response
            })
            
            print(f"{agent.name}: {response}\n")
            
            # Move to next agent
            self.current_agent_idx = (self.current_agent_idx + 1) % len(self.agents)
            
            # Check for conclusion
            if "agree" in response.lower() or turn == self.max_turns - 1:
                break
        
        return self.summarize_discussion()
    
    def summarize_discussion(self) -> str:
        """Summarize discussion outcomes."""
        return f"Discussion completed with {len(self.conversation)} messages"
```

**3. Group Chat Example (Code)**
```python
async def group_chat_example():
    """Team discussion example."""
    
    product_manager = get_agent(
        name="ProductManager",
        instructions="Think about product requirements and user needs"
    )
    
    engineer = get_agent(
        name="Engineer",
        instructions="Think about technical feasibility and implementation"
    )
    
    designer = get_agent(
        name="Designer",
        instructions="Think about user experience and design"
    )
    
    # Create group chat
    chat = GroupChat([product_manager, engineer, designer], max_turns=6)
    
    # Run discussion
    result = await chat.run(
        "Design a new feature for real-time collaboration"
    )
    
    print(f"\nFinal summary: {result}")
```

**4. Magentic One Pattern (Code)**
```python
class MagenticOne:
    """
    Magentic One orchestration:
    - Manager agent creates and updates task list
    - Worker agents complete subtasks
    - Managers coordinates and aggregates
    """
    
    def __init__(self, manager, workers: list):
        self.manager = manager
        self.workers = workers
        self.tasks = []
        self.results = {}
    
    async def decompose(self, goal: str):
        """Manager decomposes goal into subtasks."""
        prompt = f"""Break down this goal into 3-5 concrete subtasks:
{goal}

Format each task as:
1. [Task description]
2. [Task description]
..."""
        
        task_list = await self.manager.run(prompt)
        
        # Parse tasks
        self.tasks = [line.strip() for line in task_list.split('\n') if line.strip().startswith(tuple('123456789'))]
        
        return self.tasks
    
    async def execute_tasks(self):
        """Workers execute tasks in parallel."""
        async def execute_task(task: str, worker):
            return await worker.run(f"Execute this task: {task}")
        
        # Distribute tasks to workers
        executions = []
        for i, task in enumerate(self.tasks):
            worker = self.workers[i % len(self.workers)]
            executions.append(execute_task(task, worker))
        
        # Execute in parallel
        results = await asyncio.gather(*executions)
        
        self.results = {task: result for task, result in zip(self.tasks, results)}
        
        return self.results
    
    async def synthesize(self) -> str:
        """Manager synthesizes results."""
        results_text = "\n".join([
            f"Task: {task}\nResult: {result}"
            for task, result in self.results.items()
        ])
        
        prompt = f"""Synthesize these task results into a comprehensive solution:

{results_text}

Provide final recommendations."""
        
        final_result = await self.manager.run(prompt)
        
        return final_result
    
    async def run(self, goal: str) -> str:
        """Run complete Magentic One orchestration."""
        print("Step 1: Decomposing goal...")
        tasks = await self.decompose(goal)
        print(f"  Created {len(tasks)} subtasks")
        
        print("Step 2: Executing tasks...")
        await self.execute_tasks()
        print(f"  Completed {len(self.results)} tasks")
        
        print("Step 3: Synthesizing results...")
        final = await self.synthesize()
        
        return final
```

**5. Magentic One Example (Code)**
```python
async def magentic_example():
    """Complete Magentic One orchestration example."""
    
    manager = get_agent(
        name="ProjectManager",
        instructions="You are a project manager. Decompose goals and coordinate work."
    )
    
    researcher = get_agent(
        name="Researcher",
        instructions="Research complex topics thoroughly"
    )
    
    analyst = get_agent(
        name="Analyst",
        instructions="Analyze data and provide insights"
    )
    
    writer = get_agent(
        name="Writer",
        instructions="Write clear, comprehensive content"
    )
    
    # Create Magentic One
    magentic = MagenticOne(manager, [researcher, analyst, writer])
    
    # Complex goal
    goal = """
    Analyze the impact of AI on software development:
    1. Research current AI tools and frameworks
    2. Analyze productivity improvements
    3. Write comprehensive report
    """
    
    # Run orchestration
    result = await magentic.run(goal)
    
    print(f"\nFinal Report:\n{result}")
```

**6. Streaming & Long-Running Tasks (Code)**
```python
async def streaming_orchestration():
    """Handle streaming responses in orchestration."""
    
    async for chunk in orchestration.run_streaming("Process data"):
        print(f"Chunk: {chunk}")
```

**7. Error Recovery (Code)**
```python
async def orchestration_with_recovery():
    """Orchestration with error recovery."""
    
    try:
        result = await magentic.run(goal)
    except Exception as e:
        print(f"Error in task: {e}")
        print("Attempting recovery...")
        
        # Use fallback agent
        fallback_result = await fallback_agent.run(goal)
        return fallback_result
```

#### Exercises
1. Implement group chat
2. Build Magentic One system
3. Handle parallel task execution
4. Implement error recovery
5. Test with complex goals

#### Expected Output
```
Magentic One Orchestration:

Step 1: Goal Decomposition
  Task 1: Research AI development tools
  Task 2: Analyze impact on productivity
  Task 3: Identify best practices
  Task 4: Write recommendations

Step 2: Parallel Execution
  ├─ Worker 1: Task 1 → ✓ Complete
  ├─ Worker 2: Task 2 → ✓ Complete
  ├─ Worker 3: Task 3 → ✓ Complete
  └─ Manager: Task 4 → ✓ Complete

Step 3: Synthesis
  Final Report Generated

Result: Comprehensive analysis ready
```

---

### STEP 14: Human-in-the-Loop
**File**: `14_human_in_the_loop.ipynb`  
**Duration**: 75 minutes  
**Difficulty**: ⭐⭐⭐ Advanced

#### Learning Objectives
- [ ] Implement tool approval workflows
- [ ] Create human decision points
- [ ] Use checkpoints and resuming
- [ ] Handle approval requests
- [ ] Manage long-running operations

#### Notebook Sections

**1. Human-in-the-Loop Concepts (Markdown)**
- When to include humans
- Approval workflows
- Checkpoints and resuming
- Use cases

**2. Tool Approval (Code)**
```python
class ToolApprovalSystem:
    """System for approving tool calls."""
    
    def __init__(self):
        self.pending_approvals = []
        self.approved_tools = set()
    
    async def request_approval(
        self,
        tool_name: str,
        parameters: dict,
        reason: str
    ) -> bool:
        """Request human approval for tool use."""
        
        approval_id = len(self.pending_approvals)
        
        request = {
            "id": approval_id,
            "tool": tool_name,
            "params": parameters,
            "reason": reason,
            "status": "pending"
        }
        
        self.pending_approvals.append(request)
        
        print(f"\n⚠️ APPROVAL REQUIRED (ID: {approval_id})")
        print(f"Tool: {tool_name}")
        print(f"Parameters: {parameters}")
        print(f"Reason: {reason}")
        
        # Simulate human approval
        # In real system, wait for actual user input
        print("Enter 'y' to approve, 'n' to reject, or 'q' to cancel: ", end="")
        
        # For demo, auto-approve non-sensitive operations
        response = "y" if tool_name != "delete_database" else "n"
        
        if response.lower() == "y":
            request["status"] = "approved"
            return True
        else:
            request["status"] = "rejected"
            return False
    
    def get_pending(self) -> list:
        """Get pending approvals."""
        return [r for r in self.pending_approvals if r["status"] == "pending"]
```

**3. Approval Workflow (Code)**
```python
async def approval_workflow():
    """Workflow with tool approvals."""
    
    approval_system = ToolApprovalSystem()
    
    agent = get_agent(
        name="DataManager",
        instructions="Manage data operations with human oversight"
    )
    
    # Define a sensitive tool
    async def delete_data(dataset_id: str) -> str:
        """Delete a dataset - requires approval."""
        
        approved = await approval_system.request_approval(
            tool_name="delete_data",
            parameters={"dataset_id": dataset_id},
            reason="User requested permanent deletion"
        )
        
        if approved:
            return f"✓ Dataset {dataset_id} deleted"
        else:
            return f"✗ Dataset deletion cancelled"
    
    agent.tools.register(delete_data)
    
    # Use agent
    response = await agent.run("Delete old dataset from 2020")
    print(f"\nResult: {response}")

await approval_workflow()
```

**4. Checkpoints and Resuming (Code)**
```python
class WorkflowCheckpoint:
    """Save and resume workflow state."""
    
    def __init__(self):
        self.checkpoints = {}
    
    def save(self, workflow_id: str, state: dict, name: str = "auto"):
        """Save workflow checkpoint."""
        checkpoint_id = f"{workflow_id}_{name}"
        self.checkpoints[checkpoint_id] = {
            "timestamp": datetime.now().isoformat(),
            "state": state
        }
        print(f"✓ Checkpoint saved: {checkpoint_id}")
        return checkpoint_id
    
    def load(self, checkpoint_id: str) -> dict:
        """Load workflow from checkpoint."""
        if checkpoint_id in self.checkpoints:
            return self.checkpoints[checkpoint_id]["state"]
        else:
            raise ValueError(f"Checkpoint not found: {checkpoint_id}")
    
    def list_checkpoints(self, workflow_id: str) -> list:
        """List all checkpoints for workflow."""
        return [
            key for key in self.checkpoints.keys()
            if key.startswith(workflow_id)
        ]
```

**5. Checkpoint Usage (Code)**
```python
async def checkpointed_workflow():
    """Long-running workflow with checkpoints."""
    
    checkpoint_system = WorkflowCheckpoint()
    workflow_id = "analysis_2024"
    
    # Step 1: Data collection (can be slow)
    print("Step 1: Collecting data...")
    data = await collect_data()
    
    # Save checkpoint
    checkpoint_system.save(
        workflow_id,
        {"data": data, "stage": "collection"},
        "after_collection"
    )
    
    # Step 2: Analysis
    print("Step 2: Analyzing data...")
    analysis = await analyze_data(data)
    
    # Save checkpoint
    checkpoint_system.save(
        workflow_id,
        {"data": data, "analysis": analysis, "stage": "analysis"},
        "after_analysis"
    )
    
    # Step 3: Reporting
    print("Step 3: Generating report...")
    report = await generate_report(analysis)
    
    # Save final checkpoint
    checkpoint_system.save(
        workflow_id,
        {"data": data, "analysis": analysis, "report": report, "stage": "complete"},
        "final"
    )
    
    return report

# To resume from checkpoint
async def resume_workflow(workflow_id: str, checkpoint_name: str):
    """Resume workflow from checkpoint."""
    
    checkpoint_system = WorkflowCheckpoint()
    
    # Load state
    state = checkpoint_system.load(f"{workflow_id}_{checkpoint_name}")
    
    # Continue from checkpoint
    if state["stage"] == "analysis":
        print("Resuming from analysis stage...")
        analysis = state["analysis"]
        report = await generate_report(analysis)
        return report
```

**6. Interactive Decision Points (Code)**
```python
async def interactive_workflow():
    """Workflow with human decision points."""
    
    async def get_human_input(prompt: str, options: list[str]) -> str:
        """Get human input for decision."""
        print(f"\n{prompt}")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        # In real app, wait for actual input
        choice = 1  # Default
        
        return options[choice - 1]
    
    # Example: Workflow waiting for human decision
    analysis = await analyze_data()
    print(f"Analysis results: {analysis}")
    
    # Ask human to choose next step
    action = await get_human_input(
        "How should we proceed?",
        ["Approve and proceed", "Request changes", "Reject"]
    )
    
    print(f"User chose: {action}")
    
    if action == "Approve and proceed":
        result = await execute_approved_workflow()
        return result
    else:
        return "Workflow cancelled by user"

await interactive_workflow()
```

**7. Monitoring Approvals (Code)**
```python
def monitor_approvals(approval_system):
    """Monitor pending approvals."""
    
    pending = approval_system.get_pending()
    
    if pending:
        print(f"\n📋 Pending Approvals: {len(pending)}")
        for req in pending:
            print(f"  ID {req['id']}: {req['tool']} - {req['reason']}")
    else:
        print("✓ No pending approvals")
```

#### Exercises
1. Implement approval system
2. Create sensitive tool with approval
3. Build checkpointed workflow
4. Implement resume functionality
5. Test interactive decisions

#### Expected Output
```
Workflow: Data Analysis
Status: Running

⚠️ APPROVAL REQUIRED (ID: 1)
Tool: delete_old_data
Parameters: {'dataset': 'archive_2020'}
Reason: Cleanup old data

Enter approval [y/n]: y

✓ Checkpoint saved: analysis_2024_after_deletion

Step 2: Processing...
✓ Checkpoint saved: analysis_2024_after_processing

Status: ✓ Workflow completed successfully
```

---

### STEP 15: Production Features
**File**: `15_production_features.ipynb`  
**Duration**: 75 minutes  
**Difficulty**: ⭐⭐⭐ Advanced

#### Learning Objectives
- [ ] Implement comprehensive logging
- [ ] Add observability with tracing
- [ ] Create monitoring dashboards
- [ ] Debug agent behavior
- [ ] Implement cost tracking

#### Notebook Sections

**1. Logging Setup (Code)**
```python
import logging
from datetime import datetime

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/agent_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use logging
logger.info("Agent started")
logger.debug("Debug information")
logger.warning("Warning message")
logger.error("Error occurred")
```

**2. Custom Instrumentation (Code)**
```python
class AgentInstrumentation:
    """Instrument agent for monitoring."""
    
    def __init__(self, agent):
        self.agent = agent
        self.call_count = 0
        self.total_tokens = 0
        self.errors = 0
    
    async def run_instrumented(self, prompt: str) -> str:
        """Run agent with instrumentation."""
        
        import time
        start_time = time.time()
        
        try:
            self.call_count += 1
            
            logger.info(f"Agent call #{self.call_count}")
            logger.debug(f"Prompt: {prompt[:100]}...")
            
            response = await self.agent.run(prompt)
            
            execution_time = time.time() - start_time
            
            logger.info(f"Execution time: {execution_time:.2f}s")
            logger.debug(f"Response: {response[:100]}...")
            
            # Estimate tokens
            tokens_used = len(prompt.split()) + len(response.split())
            self.total_tokens += tokens_used
            
            return response
        
        except Exception as e:
            self.errors += 1
            logger.error(f"Agent error: {str(e)}")
            raise
    
    def get_stats(self) -> dict:
        """Get agent statistics."""
        return {
            "calls": self.call_count,
            "errors": self.errors,
            "total_tokens": self.total_tokens,
            "error_rate": self.errors / self.call_count if self.call_count > 0 else 0
        }
```

**3. Metrics Collection (Code)**
```python
from collections import defaultdict
from dataclasses import dataclass

@dataclass
class MetricPoint:
    """Single metric data point."""
    timestamp: str
    value: float
    tags: dict

class MetricsCollector:
    """Collect metrics over time."""
    
    def __init__(self):
        self.metrics = defaultdict(list)
    
    def record(self, metric_name: str, value: float, tags: dict = None):
        """Record metric value."""
        point = MetricPoint(
            timestamp=datetime.now().isoformat(),
            value=value,
            tags=tags or {}
        )
        self.metrics[metric_name].append(point)
    
    def get_summary(self, metric_name: str) -> dict:
        """Get metric summary statistics."""
        points = self.metrics[metric_name]
        
        if not points:
            return {}
        
        values = [p.value for p in points]
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "latest": values[-1]
        }

# Usage
metrics = MetricsCollector()

# Record execution times
metrics.record("response_time", 1.23, {"agent": "ResearchBot"})
metrics.record("response_time", 0.98, {"agent": "ResearchBot"})

# Get summary
print(metrics.get_summary("response_time"))
```

**4. Cost Tracking (Code)**
```python
class CostTracker:
    """Track and monitor API costs."""
    
    # Approximate costs (in USD per 1000 tokens)
    COSTS = {
        "gpt-4": 0.03,
        "gpt-3.5-turbo": 0.0005,
        "llama-2": 0.0001
    }
    
    def __init__(self):
        self.total_tokens = 0
        self.costs = {}
    
    def add_usage(self, model: str, input_tokens: int, output_tokens: int):
        """Track token usage."""
        
        total = input_tokens + output_tokens
        self.total_tokens += total
        
        if model not in self.costs:
            self.costs[model] = 0
        
        # Calculate cost
        cost_per_token = self.COSTS.get(model, 0.001) / 1000
        cost = total * cost_per_token
        
        self.costs[model] += cost
        
        logger.info(f"Used {total} tokens on {model}: ${cost:.4f}")
    
    def get_total_cost(self) -> float:
        """Get total costs."""
        return sum(self.costs.values())
    
    def get_breakdown(self) -> dict:
        """Get cost breakdown by model."""
        return {
            "total": self.get_total_cost(),
            "by_model": self.costs,
            "total_tokens": self.total_tokens
        }

# Usage
tracker = CostTracker()
tracker.add_usage("gpt-4", 100, 50)
tracker.add_usage("gpt-3.5-turbo", 200, 100)

print(tracker.get_breakdown())
```

**5. Debugging Tools (Code)**
```python
class AgentDebugger:
    """Tools for debugging agent behavior."""
    
    @staticmethod
    def trace_execution(prompt: str, response: str, metadata: dict = None):
        """Trace agent execution."""
        
        print("\n" + "="*60)
        print("EXECUTION TRACE")
        print("="*60)
        
        print(f"\nPrompt:\n{prompt}")
        print(f"\nResponse:\n{response}")
        
        if metadata:
            print("\nMetadata:")
            for key, value in metadata.items():
                print(f"  {key}: {value}")
        
        print("\n" + "="*60)
    
    @staticmethod
    def analyze_response(response: str) -> dict:
        """Analyze response characteristics."""
        
        return {
            "length": len(response),
            "word_count": len(response.split()),
            "sentence_count": response.count(".") + response.count("!") + response.count("?"),
            "has_code": "```" in response,
            "has_lists": any(marker in response for marker in ["-", "*", "•"])
        }

# Usage
analysis = AgentDebugger.analyze_response(response)
print(f"Response analysis: {analysis}")
```

**6. Monitoring Dashboard (Code)**
```python
def print_monitoring_dashboard(
    agent_stats: dict,
    metrics: dict,
    costs: dict
):
    """Print ASCII monitoring dashboard."""
    
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║             AGENT MONITORING DASHBOARD                 ║
    ╠════════════════════════════════════════════════════════╣
    │                                                        │
    │  Agent Statistics:                                     │
    │    Total Calls:     """+str(agent_stats.get("calls", 0))+"""                           │
    │    Error Rate:      """+f"{agent_stats.get('error_rate', 0):.1%}"+"""                          │
    │    Total Tokens:    """+str(agent_stats.get("total_tokens", 0))+"""                        │
    │                                                        │
    │  Performance:                                          │
    │    Avg Response:    1.23 sec                           │
    │    P95 Response:    2.45 sec                           │
    │    Success Rate:    99.5%                              │
    │                                                        │
    │  Costs:                                                │
    │    Total Cost:      $"""+f"{costs.get('total', 0):.2f}"+"""                          │
    │    Daily Average:   $0.15                              │
    │    Monthly Est:     $4.50                              │
    │                                                        │
    ╚════════════════════════════════════════════════════════╝
    """)

# Usage
agent_stats = {"calls": 150, "error_rate": 0.01, "total_tokens": 25000}
metrics = {"avg_response": 1.23}
costs = {"total": 0.35}

print_monitoring_dashboard(agent_stats, metrics, costs)
```

**7. Best Practices (Markdown + Code)**
```python
# Best Practices for Production Agents

# 1. Always log important events
logger.info("Significant event occurred")

# 2. Monitor costs
cost_tracker.add_usage(model, input_tokens, output_tokens)

# 3. Track metrics
metrics.record("response_time", execution_time)

# 4. Handle errors gracefully
try:
    response = await agent.run(prompt)
except Exception as e:
    logger.error(f"Error: {e}")
    # Fallback behavior

# 5. Debug when needed
AgentDebugger.trace_execution(prompt, response)

# 6. Regular health checks
stats = instrumentation.get_stats()
if stats["error_rate"] > 0.05:
    logger.warning("High error rate detected")
```

#### Exercises
1. Implement comprehensive logging
2. Add cost tracking
3. Create monitoring dashboard
4. Debug agent execution
5. Set up alerts for issues

#### Expected Output
```
╔════════════════════════════════════════════════════════╗
║             AGENT MONITORING DASHBOARD                 ║
╠════════════════════════════════════════════════════════╣
│                                                        │
│  Agent Statistics:                                     │
│    Total Calls:     150                                │
│    Error Rate:      1.0%                               │
│    Total Tokens:    25000                              │
│                                                        │
│  Performance:                                          │
│    Avg Response:    1.23 sec                           │
│    P95 Response:    2.45 sec                           │
│    Success Rate:    99.0%                              │
│                                                        │
│  Costs:                                                │
│    Total Cost:      $0.35                              │
│    Daily Average:   $0.15                              │
│    Monthly Est:     $4.50                              │
│                                                        │
╚════════════════════════════════════════════════════════╝
```

---

## Summary

All 15 notebooks follow a consistent structure:
1. Learning objectives
2. Introduction & concepts
3. Implementation examples
4. Hands-on exercises
5. Complete solutions
6. Best practices & pitfalls
7. Summary & next steps

Each notebook is self-contained but builds on previous steps, creating a comprehensive learning path from basic agents to production-ready multi-agent systems.

