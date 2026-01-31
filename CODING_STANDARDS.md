# Artemis City - Coding Standards

## Overview

This document establishes coding standards for Artemis City, adapted from the Joint Strike Fighter (JSF) C++ Coding Standards applied to Python development. These standards promote safety, reliability, maintainability, and transparency in a multi-agent system context where code quality directly impacts system trustworthiness.

**Core Philosophy**: Write code that is safe, clear, and maintainable—prioritizing readability and correctness over cleverness or premature optimization.

---

## 1. General Design Principles

### 1.1 Coupling and Cohesion

**Principle**: Minimize coupling between modules while maximizing cohesion within modules.

- **Cohesion**: Elements within a module should work together toward a single purpose
  - ✅ `handle_command()` only handles command routing
  - ❌ Mixing agent execution with CLI concerns

- **Coupling**: Modules should have minimal dependencies on each other
  - ✅ Agent router uses configuration interface, not specific implementations
  - ❌ Agents directly importing each other's internal state

**Rationale**: Loose coupling enables independent testing, modification, and reuse.

### 1.2 Single Responsibility Principle

**Rule**: Each function/class should have exactly one reason to change.

**Examples**:
```python
# ✅ GOOD: Single responsibility
def load_agent_router_config(config_path):
    """Loads agent router configuration."""
    if not os.path.exists(config_path):
        print(f"Error: Agent router config not found at {config_path}")
        return {}
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# ❌ BAD: Multiple responsibilities
def load_config_and_route_command(config_path, command):
    # Loading config + routing logic mixed together
    config = load_config(config_path)
    route_command(command, config)  # Should be separate
    save_to_database(command)  # Should be separate
```

### 1.3 Code Complexity Limits

**Rule**: Keep cyclomatic complexity ≤ 20, with most functions ≤ 10.

**Complexity is measured by**:
- If/elif/else branches
- Logical operators (and/or)
- Exception handlers
- Loops (for/while)

**Example**:
```python
# ✅ Low complexity (complexity = 4)
def handle_command(command, agent_router):
    for agent_name, config in agent_router.get('agents', {}).items():
        if any(keyword in command.lower() for keyword in config.get('keywords', [])):
            print(f"Routing command to {agent_name}...")
            return  # Early return reduces nesting

# ❌ High complexity (complexity > 15)
def handle_command_bad(command, agent_router):
    # Multiple nested conditions and branches...
    if condition1:
        if condition2:
            if condition3:
                # Very nested, hard to follow
```

**When complexity exceeds limits**:
- Extract helper functions
- Use early returns to reduce nesting
- Consider design patterns (Strategy, State)

---

## 2. C++ Standards Applied to Python

### 2.1 Type Safety

**Rule**: Use meaningful type hints and validate at function boundaries.

```python
# ✅ GOOD: Type hints in docstring
def load_agent_router_config(config_path: str) -> dict:
    """
    Args:
        config_path (str): Path to YAML configuration file.

    Returns:
        dict: Parsed agent router configuration.
    """

# ✅ GOOD: Input validation
def simulate_mail_delivery(sender: str, recipient: str, message: str) -> bool:
    if not isinstance(sender, str) or not sender.strip():
        raise ValueError("Sender must be non-empty string")
    # ... rest of function

# ❌ BAD: No type information
def load_config(path):
    return yaml.safe_load(open(path))
```

### 2.2 Resource Management

**Rule**: Always clean up resources using context managers.

```python
# ✅ GOOD: Using context manager
def load_agent_router_config(config_path):
    if not os.path.exists(config_path):
        return {}
    with open(config_path, 'r') as f:  # File auto-closes
        return yaml.safe_load(f)

# ❌ BAD: File not guaranteed to close
def load_config_bad(path):
    f = open(path, 'r')
    config = yaml.safe_load(f)
    # If error occurs, file never closes!
```

### 2.3 Error Handling

**Rule**: Use explicit error handling, not silent failures.

```python
# ✅ GOOD: Meaningful error message
def load_agent_router_config(config_path):
    if not os.path.exists(config_path):
        print(f"Error: Agent router config not found at {config_path}")
        return {}

# ✅ GOOD: Try-except with specific exceptions
try:
    user_input = input("codex> ").strip()
except KeyboardInterrupt:
    print("\nExiting Codex CLI. Goodbye!")
    break
except Exception as e:
    print(f"An error occurred: {e}")
```

**Error Handling Levels** (from most to least preferred):
1. **Compile-time/Load-time**: Validate configuration at startup
2. **Explicit exceptions**: Raise specific exceptions for error conditions
3. **Return codes**: Return status indicators (less preferred for Python)
4. **Silent failure**: Never acceptable (logging is minimum)

### 2.4 Avoiding Hidden Data

**Rule**: No implicit conversions or hidden side effects.

```python
# ✅ GOOD: Explicit conversion
if any(keyword in command.lower() for keyword in config.get('keywords', [])):
    # Explicit lowercase conversion, clear intent

# ❌ BAD: Hidden type conversion
if keyword in command:  # May do unexpected string comparison

# ✅ GOOD: Explicit default
config.get('keywords', [])  # Clear what happens if key missing

# ❌ BAD: Implicit None
keywords = config['keywords']  # Will error if missing
```

---

## 3. Code Style and Readability

### 3.1 Naming Conventions

**Rule**: Use descriptive, unambiguous names.

```python
# ✅ GOOD: Clear, descriptive names
def load_agent_router_config(config_path: str) -> dict:
    """Loads the agent router configuration from a YAML file."""

def handle_command(command: str, agent_router: dict) -> None:
    """Routes and processes a user command to the appropriate agent."""

# ❌ BAD: Unclear abbreviations
def lrc(p):  # What does lrc mean?
def hc(c, ar):  # Unclear abbreviations
```

**Naming Rules**:
- Functions and variables: `lowercase_with_underscores`
- Classes: `PascalCase` (when introduced)
- Constants: `UPPERCASE_WITH_UNDERSCORES`
- Private items: `_leading_underscore`
- No abbreviations unless universal (e.g., `i` for loop counter)

### 3.2 Line Length and Layout

**Rule**: Limit lines to 100 characters for readability.

```python
# ✅ GOOD: Readable line length
print(f"Routing command to {agent_name} ({config.get('role', 'unknown role')}):")

# For very long lines, break them:
print(
    f"Routing command to {agent_name} "
    f"({config.get('role', 'unknown role')}):"
)

# ❌ BAD: Very long line (hard to read)
print(f"Routing command to {agent_name} ({config.get('role', 'unknown role')}): Input: '{command}' Expected action: {config.get('action_description', 'processing...')}")
```

### 3.3 Comments and Documentation

**Rule**: Comments explain "why", not "what". Code should be clear enough to explain "what".

```python
# ✅ GOOD: Comments explain intent
# Use substring matching for flexibility in command phrasing
if any(keyword in command.lower() for keyword in config.get('keywords', [])):
    routed = True
    break

# ❌ BAD: Comments just restate code
# Check if keyword is in command
if keyword in command.lower():
    routed = True
    break
```

### 3.4 Whitespace and Formatting

**Rule**: Use consistent spacing for clarity.

```python
# ✅ GOOD: Proper spacing
def main():
    """Entry point for the Agentic Codex CLI application."""
    parser = argparse.ArgumentParser(description="Agentic Codex CLI Interface")
    args = parser.parse_args()

    print("--- Agentic Codex CLI ---")

# ❌ BAD: Inconsistent spacing
def main():
    """Entry point."""
    parser=argparse.ArgumentParser(description="Agentic Codex CLI Interface")
    args=parser.parse_args()
    print("--- Agentic Codex CLI ---")
```

---

## 4. Specific Python Guidelines

### 4.1 Imports

**Rule**: Import only what you use, and place imports in specific order.

```python
# ✅ GOOD: Organized imports
import argparse
import os
from pathlib import Path
from typing import Dict, Any

import yaml

# ❌ BAD: Unused imports or poor organization
import argparse, os, yaml
from typing import *
import unused_module
```

**Import Order**:
1. Standard library (argparse, os, sys, etc.)
2. Third-party packages (yaml, requests, numpy, etc.)
3. Local imports (relative to project)

### 4.2 Function Length

**Rule**: Keep functions to 200 logical lines or less; aim for ~50 lines.

```python
# ✅ GOOD: Compact function
def handle_command(command, agent_router):
    """Routes and processes a user command to the appropriate agent."""
    print(f"CLI received command: '{command}'")
    routed = False
    for agent_name, config in agent_router.get('agents', {}).items():
        if any(keyword in command.lower() for keyword in config.get('keywords', [])):
            print(f"Routing command to {agent_name} ({config.get('role')}):")
            print(f"  - Input: '{command}'")
            print(f"  - Expected action: {config.get('action_description')}")
            routed = True
            break
    if not routed:
        print("No specific agent found for this command. Defaulting to general system processing.")
```

**When function exceeds 200 lines**:
- Extract helper functions
- Separate concerns into different functions
- Consider refactoring into a class

### 4.3 Function Parameters

**Rule**: Limit functions to 7 parameters or fewer.

```python
# ✅ GOOD: Reasonable number of parameters
def simulate_mail_delivery(sender: str, recipient: str, message: str) -> bool:
    """Simulates a secure mail delivery process."""

# ❌ BAD: Too many parameters
def process_transfer(sender, recipient, message, timeout, retry_count,
                     encryption_level, log_level, failure_rate,
                     notification_enabled, priority_level):
    # Too many to understand at a glance
```

**If exceeding 7 parameters**:
- Group related parameters into a configuration dict or dataclass
- Reconsider if all parameters are necessary

### 4.4 Variable Initialization

**Rule**: Initialize variables where declared, at smallest possible scope.

```python
# ✅ GOOD: Initialize immediately
routed = False
for agent_name, config in agent_router.get('agents', {}).items():
    if any(keyword in command.lower() for keyword in config.get('keywords', [])):
        routed = True
        break

# ❌ BAD: Declare without initialization
routed  # Undefined!
for agent_name, config in agent_router.get('agents', {}).items():
    routed = False  # Initialize inside loop (wrong scope)
```

### 4.5 Avoid Magic Numbers/Strings

**Rule**: Extract magic numbers and strings into named constants.

```python
# ✅ GOOD: Named constant
MAIL_DELIVERY_FAILURE_RATE = 0.10  # 10% failure rate
NETWORK_DELAY_MIN_SECONDS = 0.5
NETWORK_DELAY_MAX_SECONDS = 1.5

def simulate_mail_delivery(sender: str, recipient: str, message: str) -> bool:
    """Simulates a secure mail delivery process."""
    time.sleep(random.uniform(NETWORK_DELAY_MIN_SECONDS, NETWORK_DELAY_MAX_SECONDS))
    if random.random() < MAIL_DELIVERY_FAILURE_RATE:
        return False
    return True

# ❌ BAD: Magic numbers scattered throughout
def simulate_mail_delivery(sender, recipient, message):
    time.sleep(random.uniform(0.5, 1.5))  # What are these numbers?
    if random.random() < 0.1:  # Why 0.1?
        return False
```

---

## 5. Documentation Standards

### 5.1 Docstring Format

**Rule**: Use Google-style docstrings for all public functions and classes.

```python
def simulate_mail_delivery(sender: str, recipient: str, message: str) -> bool:
    """Simulates a secure mail delivery process with network latency and failures.

    This function models the Pack Rat agent's mail delivery functionality within
    the Sandbox City environment. It simulates realistic network conditions.

    Args:
        sender (str): The identifier or name of the message sender.
        recipient (str): The identifier or name of the message recipient.
        message (str): The content of the message to be delivered.

    Returns:
        bool: True if the delivery simulation succeeds, False if a failure is
              simulated.

    Side Effects:
        This function prints detailed information about the transfer process
        to stdout.

    Example:
        >>> success = simulate_mail_delivery("Agent_A", "Agent_B", "Status")
        >>> if success:
        ...     print("Message delivered successfully")
    """
```

**Required Sections**:
- Brief one-line summary
- Extended description (if needed)
- Args: Parameter descriptions
- Returns: Return value description
- Raises: Exceptions that can be raised
- Example: Usage example (for complex functions)

### 5.2 Module-Level Documentation

**Rule**: Every module should have a module docstring.

```python
"""Agentic Codex Command-Line Interface Module.

This module implements the core CLI for the Artemis City agentic governance system.
It provides a command router that matches user input against agent keywords and
routes commands to the appropriate agents for processing.

Typical usage example:
    python interface/codex_cli.py              # Interactive mode
    python interface/codex_cli.py "command"    # Single command mode

Dependencies:
    - argparse: Command-line argument parsing
    - yaml: YAML configuration file parsing
    - os: Path and file system operations

Version: 0.1.0
License: MIT
"""
```

### 5.3 Inline Comments

**Rule**: Write comments that explain non-obvious decisions.

```python
# ✅ GOOD: Explains reasoning
# Use substring matching rather than exact keyword match to allow for
# natural language variations in user commands (e.g., "ask artemis" vs "talk to artemis")
if any(keyword in command.lower() for keyword in config.get('keywords', [])):

# ✅ GOOD: Explains trade-off
# 10% failure rate chosen to balance realism with not being too pessimistic.
# Adjust if empirical network data suggests different rate.
if random.random() < 0.1:
    return False

# ❌ BAD: Unnecessary comments
# Increment the counter
counter = counter + 1
```

---

## 6. Testing and Validation

### 6.1 Code Review Checklist

Before submitting code, verify:

- [ ] All public functions have complete docstrings
- [ ] Docstrings follow Google style format
- [ ] Function complexity ≤ 20 (most ≤ 10)
- [ ] Functions ≤ 200 logical lines (aim for ~50)
- [ ] Functions ≤ 7 parameters
- [ ] All variables initialized at declaration
- [ ] No magic numbers/strings (use named constants)
- [ ] Proper error handling (no silent failures)
- [ ] Resource cleanup with context managers
- [ ] Type information in docstrings
- [ ] Examples for complex functions
- [ ] No unused imports
- [ ] Consistent naming conventions
- [ ] Lines ≤ 100 characters
- [ ] Comments explain "why", not "what"

### 6.2 Complexity Measurement

**Cyclomatic Complexity** counts independent execution paths:

```python
def handle_command(command, agent_router):  # Complexity: 4
    print(f"CLI received command: '{command}'")
    routed = False
    for agent_name, config in agent_router.get('agents', {}).items():  # +1
        if any(keyword in command.lower() for keyword in config.get('keywords', [])):  # +1
            print(f"Routing command to {agent_name}...")
            routed = True
            break
    if not routed:  # +1
        print("No specific agent found...")
```

**Complexity Calculation**:
- Start with 1
- +1 for each `if`, `elif`, `else`
- +1 for each `for`, `while` loop
- +1 for each `except` clause
- +1 for each boolean operator (`and`, `or`)

---

## 7. Security Considerations

### 7.1 Input Validation

**Rule**: Validate all user input at system boundaries.

```python
# ✅ GOOD: Validate command input
def handle_command(command: str, agent_router: dict) -> None:
    if not isinstance(command, str):
        raise TypeError("Command must be a string")
    if not command.strip():
        raise ValueError("Command cannot be empty")
    # Process validated command
```

### 7.2 Safe YAML Loading

**Rule**: Always use `yaml.safe_load()`, never `yaml.load()`.

```python
# ✅ GOOD: Safe YAML loading
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)  # Safe - prevents arbitrary code execution

# ❌ BAD: Unsafe YAML loading
with open(config_path, 'r') as f:
    config = yaml.load(f)  # Unsafe - can execute arbitrary code!
```

### 7.3 File Path Handling

**Rule**: Validate file paths to prevent directory traversal attacks.

```python
# ✅ GOOD: Validate path is safe
import os
config_path = os.path.join(script_dir, 'agent_router.yaml')
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

# ❌ BAD: Unsafe path construction
config_path = f"/configs/{user_provided_path}"  # What if user provides "../../../etc/passwd"?
```

---

## 8. Performance Considerations

### 8.1 Premature Optimization

**Rule**: Prioritize clarity and correctness; optimize only when needed.

**80/20 Rule**: 80% of execution time comes from 20% of code. Profile first, optimize specific hotspots.

```python
# ✅ GOOD: Clear, maintainable code
for agent_name, config in agent_router.get('agents', {}).items():
    if any(keyword in command.lower() for keyword in config.get('keywords', [])):
        # Simple, readable approach

# ❌ BAD: Premature optimization (also less readable)
keywords_set = {kw for agent in agent_router for kw in agent_router[agent]['keywords']}
if any(keyword in command.lower() for keyword in keywords_set):
    # Micro-optimization that sacrifices clarity
```

### 8.2 Lazy Initialization

**Rule**: Load resources only when needed.

```python
# ✅ GOOD: Lazy load configuration
script_dir = os.path.dirname(__file__)
agent_router_path = os.path.join(script_dir, 'agent_router.yaml')
agent_router_config = load_agent_router_config(agent_router_path)  # Load once when needed
```

---

## 9. Maintenance and Evolution

### 9.1 Backward Compatibility

**Rule**: Document breaking changes clearly.

When changing function signatures:
- Document old and new signatures
- Provide migration guide if possible
- Mark deprecated functions with docstring warning

```python
def load_agent_router_config(config_path):
    """Loads the agent router configuration from a YAML file.

    .. deprecated:: 0.2.0
        Use ConfigurationManager.load_agent_router() instead.
        This function will be removed in version 1.0.0.

    Args:
        config_path (str): Path to the agent router YAML configuration file.

    Returns:
        dict: Parsed agent router configuration.
    """
```

### 9.2 Version Management

**Rule**: Use semantic versioning.

Format: `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes
- **MINOR**: New functionality, backward compatible
- **PATCH**: Bug fixes

Current version: **0.1.0** (Version Zero - Alpha)

---

## 10. Enforcing Standards

### 10.1 Code Review Process

1. **Automated Checks** (Future):
   - Pylint/flake8 for style violations
   - Type checking with mypy
   - Complexity analysis with radon

2. **Manual Review**:
   - Senior developer reviews code against checklist
   - Focus on design, not just style
   - Check for understanding of Codex principles

3. **Approval Criteria**:
   - Passes all automated checks
   - Passes manual code review
   - Adequate test coverage
   - Documentation complete

### 10.2 Deviation Process

**Minor deviations** (style):
- Approve with inline comment explaining reason

**Major deviations** (complexity, design):
- Requires documented approval from technical lead
- Document reason for deviation in code comments
- Plan for future remediation

---

## References

- **JSF C++ Coding Standards**: Foundation for these standards
- **Google Python Style Guide**: Modern Python best practices
- **PEP 8 - Style Guide for Python Code**: Python community standards
- **Clean Code**: Robert C. Martin - Principles applied here
- **Codex Manifesto** (`codex/manifesto.md`): Agentic governance principles

---

**Document Version**: 0.1.0
**Last Updated**: 2026-01-04
**Status**: Active - All new code must follow these standards
