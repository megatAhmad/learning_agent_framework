# Implementation Guide
## Microsoft Agent Framework Mastery Program
### 15-Step Hands-On Learning Course

**Version**: 1.0  
**Status**: Implementation Ready  
**Last Updated**: April 2026

---

## 1. Project Structure

### Directory Organization

```
microsoft-agent-framework-mastery/
├── README.md                              # Main overview
├── SETUP.md                              # Setup instructions
├── requirements.txt                      # Python dependencies
├── .env.example                          # Example environment file
├── .gitignore
│
├── notebooks/                            # All learning notebooks
│   ├── 01_setup_and_environment.ipynb
│   ├── 02_your_first_agent.ipynb
│   ├── 03_multi_turn_conversations.ipynb
│   ├── 04_understanding_tools.ipynb
│   ├── 05_single_tool_integration.ipynb
│   ├── 06_multiple_tools.ipynb
│   ├── 07_custom_tools_and_apis.ipynb
│   ├── 08_memory_and_sessions.ipynb
│   ├── 09_rag_implementation.ipynb
│   ├── 10_basic_workflows.ipynb
│   ├── 11_conditional_workflows.ipynb
│   ├── 12_orchestration_patterns.ipynb
│   ├── 13_advanced_orchestration.ipynb
│   ├── 14_human_in_the_loop.ipynb
│   └── 15_production_features.ipynb
│
├── helpers/                              # Reusable utility code
│   ├── __init__.py
│   ├── config.py                        # Configuration management
│   ├── llm_client.py                    # LLM provider abstraction
│   ├── logger.py                        # Logging utilities
│   ├── debug_tools.py                   # Debugging helpers
│   └── validators.py                    # Validation helpers
│
├── data/                                 # Sample data for notebooks
│   ├── documents/                       # For RAG examples
│   │   ├── sample_doc_1.txt
│   │   ├── sample_doc_2.txt
│   │   └── sample_doc_3.txt
│   ├── databases/                       # SQLite databases
│   └── examples/                        # Example data files
│
├── solutions/                            # Solution notebooks (for instructors)
│   ├── 01_setup_solutions.ipynb
│   ├── 02_agent_solutions.ipynb
│   └── ... (mirror of notebooks dir)
│
└── docs/                                 # Documentation
    ├── troubleshooting.md
    ├── llm_providers.md
    ├── glossary.md
    └── references.md
```

---

## 2. Setup and Configuration

### 2.1 Virtual Environment Setup

```bash
# Create virtual environment
python -m venv agent_env

# Activate (Windows)
agent_env\Scripts\activate

# Activate (macOS/Linux)
source agent_env/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 2.2 Requirements File

**requirements.txt:**
```
# Core framework
agent-framework==1.0.0
agent-framework-core==1.0.0

# LLM providers
openai>=1.3.0
azure-ai-projects>=1.0.0
azure-identity>=1.14.0

# Development
jupyter>=1.0.0
ipython>=8.0.0
ipykernel>=6.0.0

# Utilities
python-dotenv>=1.0.0
pydantic>=2.0.0
requests>=2.28.0
aiohttp>=3.8.0

# Optional for specific steps
pandas>=1.3.0
numpy>=1.21.0
sqlalchemy>=1.4.0
scikit-learn>=1.0.0

# Development tools
black>=23.0.0
pylint>=2.17.0
```

### 2.3 Environment Configuration

**.env.example:**
```bash
# ===== OpenRouter Configuration =====
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=meta-llama/llama-2-70b-chat

# ===== Azure OpenAI Configuration =====
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_openai_key_here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_SUBSCRIPTION_ID=your_subscription_id
AZURE_RESOURCE_GROUP=your_resource_group

# ===== General Configuration =====
LLM_PROVIDER=openrouter  # or azure_openai
DEBUG=False
LOG_LEVEL=INFO

# ===== API Keys (if using specific APIs) =====
WEATHER_API_KEY=
NEWS_API_KEY=
```

**Copy to .env:**
```bash
cp .env.example .env
# Edit .env with your actual keys
```

### 2.4 Configuration Module (helpers/config.py)

```python
"""Configuration management for the learning program."""

import os
from dataclasses import dataclass
from typing import Literal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class OpenRouterConfig:
    """OpenRouter configuration."""
    api_key: str
    base_url: str = "https://openrouter.ai/api/v1"
    model: str = "meta-llama/llama-2-70b-chat"
    
    @classmethod
    def from_env(cls):
        return cls(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            model=os.getenv("OPENROUTER_MODEL", "meta-llama/llama-2-70b-chat")
        )

@dataclass
class AzureOpenAIConfig:
    """Azure OpenAI configuration."""
    endpoint: str
    api_key: str
    deployment_name: str
    
    @classmethod
    def from_env(cls):
        return cls(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
        )

class Config:
    """Main configuration manager."""
    
    provider: Literal["openrouter", "azure_openai"] = os.getenv("LLM_PROVIDER", "openrouter")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    openrouter = OpenRouterConfig.from_env()
    azure_openai = AzureOpenAIConfig.from_env()
    
    @classmethod
    def get_active_config(cls):
        """Get active LLM provider configuration."""
        if cls.provider == "openrouter":
            return cls.openrouter
        elif cls.provider == "azure_openai":
            return cls.azure_openai
        else:
            raise ValueError(f"Unknown provider: {cls.provider}")

# Export for easy import
config = Config()
```

---

## 3. Helper Modules

### 3.1 LLM Client Abstraction (helpers/llm_client.py)

```python
"""Abstraction layer for LLM providers."""

import os
from typing import Optional
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient, AzureOpenAIChatClient
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from .config import config

class LLMClientFactory:
    """Factory for creating LLM clients."""
    
    @staticmethod
    def create_client(provider: Optional[str] = None):
        """Create appropriate LLM client based on configuration."""
        provider = provider or config.provider
        
        if provider == "openrouter":
            return OpenAIChatClient(
                base_url=config.openrouter.base_url,
                api_key=config.openrouter.api_key,
                model=config.openrouter.model
            )
        elif provider == "azure_openai":
            return AzureOpenAIChatClient(
                endpoint=config.azure_openai.endpoint,
                api_key=config.azure_openai.api_key,
                deployment=config.azure_openai.deployment_name
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")

class AgentFactory:
    """Factory for creating agents with standard configuration."""
    
    @staticmethod
    def create_agent(
        name: str,
        instructions: str,
        provider: Optional[str] = None,
        **kwargs
    ) -> Agent:
        """Create an agent with standard setup."""
        client = LLMClientFactory.create_client(provider)
        
        agent = Agent(
            client=client,
            name=name,
            instructions=instructions,
            **kwargs
        )
        
        return agent

# Helper function for quick access
def get_agent(name: str, instructions: str) -> Agent:
    """Quick helper to create an agent."""
    return AgentFactory.create_agent(name, instructions)
```

### 3.2 Logger Setup (helpers/logger.py)

```python
"""Logging configuration."""

import logging
import sys
from .config import config

def setup_logging(name: str = __name__) -> logging.Logger:
    """Setup structured logging."""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.log_level))
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, config.log_level))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger

# Create module-level logger
logger = setup_logging()
```

### 3.3 Debug Tools (helpers/debug_tools.py)

```python
"""Debugging utilities for learning and development."""

import json
from typing import Any

def pretty_print(obj: Any, title: str = "Output"):
    """Pretty print any object."""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    
    if isinstance(obj, dict):
        print(json.dumps(obj, indent=2, default=str))
    elif isinstance(obj, (list, tuple)):
        for i, item in enumerate(obj):
            print(f"[{i}] {item}")
    else:
        print(obj)
    
    print()

def inspect_agent(agent, title: str = "Agent Inspection"):
    """Inspect agent structure and configuration."""
    pretty_print({
        "name": agent.name,
        "instructions": agent.instructions[:100] + "...",
        "tools": list(agent.tools.keys()) if hasattr(agent, 'tools') else [],
        "session_id": getattr(agent, 'session_id', 'N/A'),
    }, title)

def compare_responses(response1: str, response2: str, title: str = "Response Comparison"):
    """Compare two responses side-by-side."""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"\nResponse 1:\n{response1}\n")
    print(f"\nResponse 2:\n{response2}\n")
```

---

## 4. Notebook Template

### Standard Notebook Structure

```python
# ============================================================================
# STEP N: [TITLE]
# ============================================================================
"""
Learning Step N: [Title]

This notebook teaches [primary concept].

Learning Objectives:
- Understand [concept 1]
- Implement [concept 2]  
- Debug [concept 3]

Time Estimate: XX minutes
"""

# %% [markdown]
# # Step N: [Title]
# 
# ## Learning Objectives
# - [ ] Understand [concept 1]
# - [ ] Implement [concept 2]
# - [ ] Debug [concept 3]
# 
# ## Prerequisites
# - Complete Step N-1
# - Basic understanding of [prerequisite concept]
# 
# ## Estimated Time
# 60-90 minutes

# %% 
# SETUP AND IMPORTS
import os
import asyncio
from pathlib import Path
import sys

# Add helpers to path
sys.path.insert(0, str(Path.cwd().parent))

from helpers.config import config
from helpers.llm_client import get_agent, LLMClientFactory
from helpers.logger import logger
from helpers.debug_tools import pretty_print, inspect_agent

# Verify setup
print(f"✓ Python version: {sys.version}")
print(f"✓ Using LLM Provider: {config.provider}")
print(f"✓ Debug mode: {config.debug}")

# %% [markdown]
# ## Part 1: Introduction & Concepts
# 
# ### What is [concept]?
# [Explanation of core concept]

# %% [markdown]
# ### Key Components
# 1. Component 1: [Description]
# 2. Component 2: [Description]
# 3. Component 3: [Description]

# %% [markdown]
# ### Real-World Example
# [Example showing why this matters]

# %% [markdown]
# ## Part 2: Implementation
# 
# ### Basic Implementation

# %%
# Example 1: Basic usage
async def example_1():
    """Basic example of [concept]."""
    agent = get_agent(
        name="ExampleAgent",
        instructions="You are a helpful assistant."
    )
    
    result = await agent.run("Example prompt")
    pretty_print(result, "Agent Response")

# Run the example
await example_1()

# %% [markdown]
# ### Advanced Implementation

# %%
# Example 2: Advanced patterns
async def example_2():
    """Advanced example of [concept]."""
    # Implementation here
    pass

# await example_2()

# %% [markdown]
# ## Part 3: Hands-On Exercises
# 
# ### Exercise 1: [Title]
# 
# **Task**: [Description of what to do]
# 
# **Starter Code**:

# %%
# EXERCISE 1 - Complete the implementation
async def exercise_1_solution():
    """Solution to exercise 1."""
    # TODO: Complete this implementation
    # Hints:
    # 1. Create an agent with [instructions]
    # 2. [Additional hints]
    pass

# %%
# Test your implementation
# Uncomment to run:
# await exercise_1_solution()

# %% [markdown]
# ### Exercise 2: [Title]
# 
# **Task**: [Description]

# %%
# EXERCISE 2
async def exercise_2_solution():
    """Solution to exercise 2."""
    # TODO: Complete this
    pass

# %% [markdown]
# ## Part 4: Solutions & Discussion
# 
# ### Solution to Exercise 1

# %%
# COMPLETE SOLUTION to Exercise 1
async def exercise_1_complete():
    """Complete solution with explanation."""
    agent = get_agent(
        name="SolutionAgent",
        instructions="You are [detailed instructions]"
    )
    
    result = await agent.run("Your prompt here")
    return result

solution_1 = await exercise_1_complete()
pretty_print(solution_1, "Exercise 1 Output")

# %% [markdown]
# **Why this works:**
# - Reason 1
# - Reason 2

# %% [markdown]
# ### Solution to Exercise 2

# %%
# COMPLETE SOLUTION to Exercise 2
async def exercise_2_complete():
    """Complete solution."""
    # Implementation
    pass

# %% [markdown]
# ## Part 5: Best Practices & Common Pitfalls
# 
# ### Best Practices ✓
# 1. Always [practice 1]
# 2. Remember to [practice 2]
# 3. Consider [practice 3]
# 
# ### Common Pitfalls ✗
# 1. **Pitfall**: [Description]
#    **Solution**: [How to avoid]
# 
# 2. **Pitfall**: [Description]
#    **Solution**: [How to avoid]

# %% [markdown]
# ## Summary & Next Steps
# 
# ### Key Takeaways
# - You learned about [concept 1]
# - You implemented [concept 2]
# - You practiced [concept 3]
# 
# ### You Are Now Ready For
# - Step N+1: [Next Topic]
# 
# ### Additional Resources
# - [Link 1]
# - [Link 2]

# %% [markdown]
# ## Self-Check
# 
# Can you answer these questions?
# 
# - [ ] What is [concept]?
# - [ ] How do you [implementation detail]?
# - [ ] When would you use [pattern]?
# - [ ] What are common issues with [topic]?

# %%
# Thank you for completing Step N!
print("✓ Step N: [Title] - Completed!")
print("Next: Move to Step N+1 when ready")
```

---

## 5. Notebook-Specific Requirements

### Step 1: Setup & Environment
- **File**: `01_setup_and_environment.ipynb`
- **Key Code**:
  - Virtual environment setup
  - Package installation
  - API key verification
  - Import all required libraries
  - Test basic functionality

### Step 2: Your First Agent
- **File**: `02_your_first_agent.ipynb`
- **Key Code**:
  - Agent creation
  - Basic execution
  - Response handling
  - Provider switching

### Step 5: Single Tool Integration
- **File**: `05_single_tool_integration.ipynb`
- **Key Code**:
  - Weather tool function
  - Tool registration
  - Agent invocation
  - Response inspection

### Step 9: RAG Implementation
- **File**: `09_rag_implementation.ipynb`
- **Key Code**:
  - Document loading
  - Chunking strategy
  - Embedding generation
  - Vector search
  - Complete RAG pipeline

### Step 10-13: Workflows
- **Files**: `10-13_*.ipynb`
- **Key Code**:
  - WorkflowBuilder usage
  - Executor definition
  - Edge connections
  - Pattern implementations

---

## 6. Sample Data Organization

### data/documents/ (for RAG Step)
```
documents/
├── README.md
├── document_1.txt     # Sample document
├── document_2.txt     # Sample document
└── document_3.txt     # Sample document
```

### data/examples/ (for tool examples)
```
examples/
├── weather_data.json
├── user_profiles.json
└── sample_responses.txt
```

---

## 7. Development Workflow

### Creating a Notebook

**Checklist:**
- [ ] Create notebook file following naming convention
- [ ] Add metadata and learning objectives
- [ ] Include all necessary imports
- [ ] Test all code cells
- [ ] Add explanation blocks
- [ ] Include 2-3 exercises
- [ ] Provide complete solutions
- [ ] Add best practices section
- [ ] Verify execution end-to-end
- [ ] Save with example outputs

### Testing Notebook

```bash
# Install nbval for testing
pip install nbval

# Run all notebooks
pytest --nbval notebooks/

# Run specific notebook
pytest --nbval notebooks/01_setup_and_environment.ipynb
```

### Notebook Validation Script

**scripts/validate_notebooks.py:**
```python
#!/usr/bin/env python3
"""Validate all notebooks can execute."""

import subprocess
import sys
from pathlib import Path

def validate_notebooks():
    """Run all notebooks and check for errors."""
    notebooks_dir = Path("notebooks")
    notebooks = sorted(notebooks_dir.glob("*.ipynb"))
    
    failed = []
    
    for notebook in notebooks:
        print(f"Validating {notebook.name}...", end=" ")
        try:
            result = subprocess.run(
                ["jupyter", "nbconvert", "--to", "notebook", "--execute", str(notebook)],
                capture_output=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print("✓")
            else:
                print("✗")
                failed.append((notebook.name, result.stderr.decode()))
        
        except Exception as e:
            print("✗")
            failed.append((notebook.name, str(e)))
    
    if failed:
        print(f"\n❌ {len(failed)} notebook(s) failed:")
        for name, error in failed:
            print(f"  - {name}")
            print(f"    {error[:100]}...")
        return 1
    else:
        print(f"\n✓ All {len(notebooks)} notebooks validated successfully!")
        return 0

if __name__ == "__main__":
    sys.exit(validate_notebooks())
```

---

## 8. Documentation Requirements

### README.md (Main)
```markdown
# Microsoft Agent Framework Mastery Program

A comprehensive, hands-on learning program with 15 progressive steps.

## Quick Start
[Setup instructions]

## Course Structure
[Step overview table]

## Time Commitment
[Estimated hours]

## Getting Help
[Support resources]
```

### SETUP.md
```markdown
# Setup Instructions

## Prerequisites
[System and software requirements]

## Installation
[Step-by-step setup]

## Verification
[How to verify setup works]

## Troubleshooting
[Common issues and solutions]
```

### docs/troubleshooting.md
```markdown
# Troubleshooting Guide

## Common Issues

### Issue 1: [Issue]
**Error Message**: [Message]
**Solution**: [Steps to fix]

### Issue 2: [Issue]
...
```

---

## 9. Quality Assurance

### Testing Checklist

For each notebook:
- [ ] All imports work
- [ ] Code cells execute without errors
- [ ] Output matches expected results
- [ ] Exercises are solvable
- [ ] Solutions are correct
- [ ] No hardcoded paths
- [ ] Works with both LLM providers
- [ ] Documentation is clear
- [ ] Estimated time is accurate

### Code Quality Standards

- **PEP 8 Compliance**: Use black for formatting
- **Type Hints**: All functions annotated
- **Docstrings**: All functions documented
- **Comments**: Complex logic explained
- **Error Handling**: Try/except for external calls
- **Logging**: logger.info/debug used appropriately

---

## 10. Deployment & Release

### Release Checklist

- [ ] All 15 notebooks completed
- [ ] All notebooks tested and validated
- [ ] Documentation complete
- [ ] Troubleshooting guide comprehensive
- [ ] Example outputs included
- [ ] README and setup guides written
- [ ] Sample data provided
- [ ] Helper modules finalized
- [ ] Requirements.txt pinned
- [ ] .env.example created

### Version Control

```bash
# Tag release
git tag -a v1.0 -m "Microsoft Agent Framework Mastery Program v1.0"
git push origin v1.0
```

---

## 11. Maintenance & Updates

### Update Frequency
- Monthly: Check for framework updates
- Quarterly: Update dependencies
- As-needed: Fix bugs and issues

### Community Feedback
- GitHub Issues for bug reports
- Discussions for questions
- Pull requests for improvements

---

## 12. Success Metrics

### Quantitative
- ✓ 15/15 notebooks completed
- ✓ 100% notebook pass rate
- ✓ <2% error rate in code
- ✓ <5 minutes average per exercise

### Qualitative
- ✓ Learners can build own agents
- ✓ Learners understand orchestration
- ✓ Learners can debug issues
- ✓ Positive feedback on clarity

---

**End of Implementation Guide**
