# agentic_governance_artemis_city

## Overview

Artemis City is an architectural framework designed to align agentic reasoning with transparent, accountable action across distributed intelligence systems—both human and machine. This initial scaffolding, Version Zero, provides a foundational structure for defining agents, managing memory, establishing interfaces, and simulating environments. The project is seeded with the intention of iterative clarity and accountable collaboration, balancing trust, entropy, and collaboration to move towards a "net good over noise" ethos.

This repository contains a command-line interface (CLI) to interact with the system's agent router, along with a standalone simulation for mail delivery within the "Sandbox City" environment.

## Prerequisites

Before you begin, ensure you have the following software installed on your system:
- **Python 3.8 or higher**: The core CLI and simulation scripts are written in Python.
- **pip**: Python's package installer, which typically comes with Python.

## Setup and Installation

Follow these steps to get Artemis City running on your local machine:

1.  **Clone the Repository**:
    If this were a Git repository, you would clone it. For now, ensure all project files are located in a single directory.

2.  **Navigate to the Project Directory**:
    Open your terminal and change to the directory containing the project files.

3.  **Create and Activate a Virtual Environment**:
    It is highly recommended to use a virtual environment to manage dependencies.

    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate on macOS and Linux
    source venv/bin/activate

    # Activate on Windows
    .\venv\Scripts\activate
    ```

4.  **Install Dependencies**:
    Install the required Python packages using the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Artemis City can be operated through its command-line interface or by running individual simulations.

### Running the Agentic Codex CLI

The main entry point is the Agentic Codex CLI, which simulates routing commands to different agents based on keywords.

1.  **Launch the CLI in Interactive Mode**:
    Run the `codex_cli.py` script without any arguments to enter an interactive session.

    ```bash
    python interface/codex_cli.py
    ```

    You will be greeted with a `codex>` prompt. Type commands and press Enter to see how they are routed. To exit, type `exit` or `quit`.

    **Example Session**:
    ```
    --- Agentic Codex CLI ---
    Type 'exit' or 'quit' to close.
    codex> ask artemis about system status
    CLI received command: 'ask artemis about system status'
    Routing command to Artemis (Overseer of the city's functions):
      - Input: 'ask artemis about system status'
      - Expected action: processing system-level commands and queries...
    codex> help me with a data query
    CLI received command: 'help me with a data query'
    Routing command to Copilot (Data retrieval and analysis assistant):
      - Input: 'help me with a data query'
      - Expected action: assisting with data-related tasks...
    ```

2.  **Run the CLI with a Command**:
    You can also pass a command directly as an argument. The script will execute it and then exit.

    ```bash
    python interface/codex_cli.py "check mail for delivery"
    ```

    **Example Output**:
    ```
    --- Agentic Codex CLI ---
    Type 'exit' or 'quit' to close.
    CLI received command: 'check mail for delivery'
    Routing command to Pack Rat (Secure data courier):
      - Input: 'check mail for delivery'
      - Expected action: handling secure data transfer and storage...
    ```

### Running the Mail Delivery Simulation

The `mail_delivery_sim.py` script simulates a secure mail delivery process within the Sandbox City environment.

-   **Execute the script directly from your terminal**:

    ```bash
    python sandbox_city/networked_scripts/mail_delivery_sim.py
    ```

    The script will run two predefined simulations and print the results, including a simulated delay and a random chance of failure.

    **Example Output**:
    ```
    Running Mail Delivery Simulation (Sandbox City - Post Office)

    --- Mail Delivery Simulation ---
    Sender: Agent_A, Recipient: Agent_B
    Message: 'Urgent operational update.'
    Pack Rat is initiating secure transfer...
    Transfer successful: Message delivered securely.

    --- Mail Delivery Simulation ---
    Sender: Human_User, Recipient: Artemis
    Message: 'Query about recent policy change.'
    Pack Rat is initiating secure transfer...
    Transfer failed: Data integrity compromised or recipient unreachable.
    ```

## Project Structure

This repository is organized into several key directories, each serving a distinct purpose within the Artemis City framework:

-   `agents/`: Contains Markdown files defining the roles and responsibilities of the different agents operating within the system (e.g., `artemis.md`, `copilot.md`).
-   `codex/`: Holds the core principles and high-level vision of the Artemis City project.
-   `interface/`: Includes the primary user-facing components, such as the command-line interface (`codex_cli.py`) and its configuration (`agent_router.yaml`).
-   `launch/`: Contains documents related to project governance, including the open source covenant and release gatechecks.
-   `memory/`: Provides conceptual frameworks for agent memory, trust decay models, and validation simulations.
-   `sandbox_city/`: A simulated environment designed for testing agent interactions. It includes networked scripts (`mail_delivery_sim.py`) and conceptual layouts.
-   `requirements.txt`: Lists the Python packages required to run the project.

## Contributing

Contributions are welcome! If you have ideas for improvements, please open an issue to discuss your proposed changes. For consistency, please adhere to the existing coding style and ensure that all public functions are documented using Google-style Python docstrings.
An architectural framework for building agentic reasoning systems with transparent, accountable action across distributed intelligence systems.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Interactive Demo](#interactive-demo)
3. [Quick Start](#quick-start)
4. [Architecture](#architecture)
5. [Core Components](#core-components)
6. [Memory Integration](#memory-integration)
7. [Agent System](#agent-system)
8. [Key Protocols](#key-protocols)
9. [Development Guide](#development-guide)
10. [Testing](#testing)
11. [Deployment](#deployment)
12. [Security](#security)
13. [Contributing](#contributing)
14. [License](#license)
15. [Resources](#resources)

---

## Project Overview

**Artemis City** is a comprehensive framework designed to align agentic reasoning with transparent, accountable action. It provides:

- **Agent definitions** with clear roles and boundaries
- **Memory management** with trust decay models
- **Secure communication** interfaces via the Artemis Transmission Protocol (ATP)
- **Simulation environments** for testing agent interactions

### Key Metadata

| Field | Value |
|-------|-------|
| **Project Name** | agentic_governance_artemis_city |
| **Version** | 0.1.0 |
| **License** | MIT |
| **Primary Languages** | Python 3.8+, TypeScript |
| **Author** | Prinston Palmer |

### Mission Statement

Balance **trust**, **entropy**, and **collaboration** to achieve "net good over noise" through iterative clarity and accountable collaboration.

---

## Interactive Demo

Try the **ATP Prototype** - a fully interactive visualization of the Artemis City agent ecosystem that runs directly in your browser.

### Running in GitHub Codespaces / Jupyter

1. Open `atp-prototype.html` in a Codespace or Jupyter environment
2. Use the built-in HTML preview or open in a browser tab
3. Explore the live agent ecosystem with:
   - **Trust Decay Visualization**: Watch trust scores evolve over time with real-time charts
   - **Agent Interaction Panel**: See Artemis, Copilot, Pack Rat, and Codex Daemon in action
   - **ATP Protocol Builder**: Construct structured commands with Mode, Priority, and ActionType
   - **Hebbian Weight Dynamics**: Observe how agent relationships strengthen through interaction

```bash
# In Codespaces: Right-click atp-prototype.html → Open Preview
# Or serve locally:
python -m http.server 8080
# Then open http://localhost:8080/atp-prototype.html
```

---

## Quick Start

### Prerequisites

- Python 3.8+ (3.10+ recommended)
- Node.js 18+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/popvilla/artemis-city.git
cd Artemis-City

# Set up secure environment (REQUIRED)
./setup_secrets.sh

# Create Python virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR .venv\Scripts\activate on Windows

# Install Python dependencies
pip install -r requirements.txt
```

### Running the CLI

```bash
# Interactive mode
python app/launch/main.py

# Single command mode
python app/launch/main.py "ask artemis about system status"

# With ATP headers
python app/launch/main.py "#Mode: Build #Context: Feature request"
```

### Starting the MCP Server

```bash
cd "app/Artemis Agentic Memory Layer"
npm install
npm run dev
```

---

## Architecture

### System Overview

```
Artemis-City/
├── app/                          # Main application code
│   ├── agents/                   # Agent definitions (ATP, Artemis)
│   ├── codex/                    # Kernel, router, memory bus
│   ├── core/                     # Core utilities (instructions)
│   ├── integration/              # External integrations (MCP)
│   ├── interface/                # CLI interface
│   ├── launch/                   # Entry points
│   └── sandbox_city/             # Simulation environment
├── artemis-city-blog/            # Next.js marketing blog
├── MCP/                          # Memory server & frontend
├── tests/                        # Test suite
└── docs/                         # Documentation
```

### Component Interactions

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI Interface                            │
│  (app/launch/main.py, app/interface/codex_cli.py)               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ATP Parser                                  │
│  (app/agents/atp/) - Parses structured command headers          │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Kernel                                      │
│  (app/codex/kernel.py) - Orchestrates all subsystems            │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐   ┌───────────────┐   ┌───────────────┐     │
│  │ Agent Router  │   │  Memory Bus   │   │   Agents      │     │
│  │ (Routes cmds) │   │ (Persistence) │   │ (Processors)  │     │
│  └───────────────┘   └───────────────┘   └───────────────┘     │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MCP Memory Server                              │
│  (app/integration/memory_client.py → MCP/)                      │
│  Obsidian vault integration for persistent memory               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### Kernel (`app/codex/kernel.py`)

The central orchestrator that manages:
- Command processing and routing
- Agent instantiation
- Persistent state management
- Memory bus operations

```python
from codex.kernel import Kernel

kernel = Kernel()
result = kernel.process({"type": "command", "content": "status"})
```

### Agent Router (`app/codex/agent_router.py`)

Routes commands to appropriate agents based on keyword matching:

```yaml
# agent_router.yaml
agents:
  artemis:
    role: "Governance Agent"
    keywords: ["artemis", "governance", "policy", "audit"]
    action_description: "Handles governance and policy queries"
```

### Memory Bus (`app/codex/memory_bus.py`)

Provides persistent memory storage with pluggable backends:

```python
from codex.memory_bus import MemoryBus

memory = MemoryBus()
memory.write("Content", metadata={"source": "agent_name"})
results = memory.read("search query")
```

### Instruction Loader (`app/core/instructions.py`)

Loads agent instructions from Markdown files with caching:

```python
from core.instructions import get_global_cache

cache = get_global_cache()
instructions = cache.get(agent_name="artemis")
```

---

## Memory Integration

Artemis City integrates with **Obsidian vault** as a persistent knowledge base through the Artemis Agentic Memory Layer (MCP Server). This enables agents to maintain context across sessions with trust-based access control.

### Key Features

| Feature | Description |
|---------|-------------|
| **Persistent Context** | Agents store and retrieve context across sessions |
| **Trust-Based Access** | Memory operations filtered by agent trust scores |
| **Obsidian Integration** | Vault acts as versioned source of truth |
| **MCP Operations** | Read, append, update, search, search/replace, list, delete, frontmatter, tags |

### Quick Example

```python
# Requires app/ on PYTHONPATH (e.g., run from app/ or set PYTHONPATH=app)
from integration import MemoryClient, get_trust_interface

client = MemoryClient(base_url="http://localhost:3000", api_key="your_key")
trust = get_trust_interface()

# Check permission and store agent context
if trust.can_perform_operation('artemis', 'write'):
    client.store_agent_context("artemis", "Session completed successfully")
    trust.record_success('artemis')  # Reinforce trust
```

### Trust Levels

| Level | Score | Allowed Operations |
|-------|-------|-------------------|
| FULL | 0.9-1.0 | read, write, delete, search, tag, update |
| HIGH | 0.7-<0.9 | read, write, search, tag, update |
| MEDIUM | 0.5-<0.7 | read, write, search, tag |
| LOW | 0.3-<0.5 | read, search |
| UNTRUSTED | <0.3 | none |

For complete documentation, see [docs/MEMORY_INTEGRATION.md](docs/MEMORY_INTEGRATION.md).

---

## Agent System

### Available Agents

| Agent | Role | Keywords |
|-------|------|----------|
| **Artemis** | Governance, dispute resolution | artemis, governance, policy, audit |
| **Copilot** | Real-time assistant | help, assist, explain, suggest |
| **Pack Rat** | Secure data transfer | transfer, send, receive, courier |
| **Codex Daemon** | System status, memory interface | memory, system, daemon, config |

### Creating a New Agent

1. Create agent definition in `app/agents/`:

```markdown
# Agent: MyAgent

## Semantic Role
Primary function description

## System Access Scope
- Read: specific resources
- Write: specific outputs

## Keywords
- keyword1
- keyword2
```

2. Implement agent class:

```python
from codex.agents.base import Agent

class MyAgent(Agent):
    """Custom agent implementation.

    Args:
        name: Agent identifier.
        config: Optional configuration dictionary.
    """

    def handle(self, request, memory):
        """Process the request and return a response.

        Args:
            request: Dictionary with 'content' key.
            memory: MemoryBus instance for persistence.

        Returns:
            str: Response content.
        """
        content = request.get("content", "")
        # Process content
        return f"Processed: {content}"
```

3. Register in `agent_router.yaml`

---

## Key Protocols

### Artemis Transmission Protocol (ATP)

Structured communication system with signal tags:

| Tag | Purpose | Values |
|-----|---------|--------|
| `#Mode:` | Overall intent | Build, Review, Organize, Capture, Synthesize, Commit |
| `#Context:` | Mission goal | Free text |
| `#Priority:` | Urgency level | Critical, High, Normal, Low |
| `#ActionType:` | Expected response | Summarize, Scaffold, Execute, Reflect |
| `#TargetZone:` | Project area | Path or scope |
| `#SpecialNotes:` | Exceptions | Free text |

Example:
```
#Mode: Build #Context: Add dark mode #Priority: High #ActionType: Execute
```

### Trust Decay Model

Dynamic trust evaluation framework:

- **Initial Trust Score**: Baseline for new entities
- **Decay Rate**: Erosion over time without reinforcement
- **Reinforcement Events**: Successful actions increase trust
- **Trust Thresholds**: Trigger access restrictions when crossed

---

## Development Guide

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -e '.[dev]'

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run code formatters
black app/ tests/
isort app/ tests/

# Run linters
flake8 app/ tests/
mypy app/
```

### Code Style

- **Python**: Google-style docstrings, Black formatting, type hints
- **TypeScript**: JSDoc comments, Prettier formatting
- **Configuration**: YAML for agent routing, JSON for settings

### Running the Development Server

```bash
# Terminal 1: MCP Server
cd MCP
npm run dev

# Terminal 2: Blog (optional)
cd artemis-city-blog
npm run dev

# Terminal 3: Python CLI
source .venv/bin/activate
python app/launch/main.py
```

---

## Testing

### Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=app --cov-report=html

# Specific test file
pytest tests/test_atp.py -v

# By marker
pytest tests/ -m unit -v
pytest tests/ -m integration -v
```

### Test Categories

| Marker | Description |
|--------|-------------|
| `unit` | Fast, isolated unit tests |
| `integration` | Tests requiring external services |
| `e2e` | End-to-end workflow tests |
| `slow` | Long-running tests |
| `requires_server` | Tests requiring MCP server |

### Test Coverage Areas

- ATP message parsing and validation
- Artemis persona and reflection engine
- Instruction loading and caching
- Memory integration (MCP client)
- Trust interface operations

---

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t artemis-city .

# Run with docker-compose
docker-compose up -d
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MCP_API_KEY` | API authentication key | Yes |
| `OBSIDIAN_BASE_URL` | Obsidian vault URL | Yes |
| `MCP_LOG_LEVEL` | Logging verbosity | No |

### CI/CD Pipeline

The project uses GitHub Actions for:

- **CI** (`.github/workflows/ci.yml`): Test on push/PR
- **Code Quality** (`.github/workflows/code-quality.yml`): Linting, formatting
- **Dependencies** (`.github/workflows/dependencies.yml`): Security updates
- **Release** (`.github/workflows/release.yml`): Automated releases

---

## Security

### Secret Management

- Never commit `.env` files (protected by `.gitignore`)
- Use `setup_secrets.sh` for secure environment setup
- Generate API keys with: `openssl rand -hex 32`
- Set file permissions: `chmod 600 .env`

### Security Tools

- **detect-secrets**: Pre-commit hook for secret detection
- **bandit**: Python security linter
- **Pre-commit hooks**: Comprehensive security checks

### If Secrets Are Exposed

1. Immediately rotate all compromised keys
2. Revoke old keys from all services
3. Monitor logs for unauthorized access
4. Document the incident
5. Review security practices

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes following code style guidelines
4. Add tests for new functionality
5. Run tests and linters: `pytest && flake8 && black --check .`
6. Commit with clear messages
7. Push and create a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Resources

### Documentation (`docs/`)

| Document | Description |
|----------|-------------|
| [MEMORY_INTEGRATION.md](docs/MEMORY_INTEGRATION.md) | Memory layer API reference and usage patterns |
| [LIVING_CITY.md](docs/LIVING_CITY.md) | Living City metaphor and architectural philosophy |
| [trust_decay_model.md](docs/trust_decay_model.md) | Trust decay mathematics and implementation |
| [ARTEMIS_FEATURES.md](docs/ARTEMIS_FEATURES.md) | Feature specifications for Artemis agent |
| [kernel.md](docs/kernel.md) | Kernel architecture and design |
| [INSTALL.md](docs/INSTALL.md) | Detailed installation guide |
| [CICD.md](docs/CICD.md) | CI/CD pipeline documentation |

### Other Resources

- **Interactive Demo**: [atp-prototype.html](atp-prototype.html) - Browser-based agent visualization
- **Security Guide**: [SECURITY.md](SECURITY.md)

---

Authored by Prinston (Apollo) Palmer - Systems Architect
With Claude (Anthropic) - AI Development Partner
