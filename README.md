# Artemis City

An architectural framework for building agentic reasoning systems with transparent, accountable action across distributed intelligence systems.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Architecture](#architecture)
4. [Core Components](#core-components)
5. [Agent System](#agent-system)
6. [Key Protocols](#key-protocols)
7. [Development Guide](#development-guide)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Security](#security)
11. [Contributing](#contributing)
12. [License](#license)

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
| **Project Name** | Artemis City (agentic-codex) |
| **Version** | 0.1.0 |
| **License** | Apache 2.0 |
| **Primary Languages** | Python 3.8+, TypeScript |
| **Author** | Prinston Palmer |

### Mission Statement

Balance **trust**, **entropy**, and **collaboration** to achieve "net good over noise" through iterative clarity and accountable collaboration.

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
├── build/                          # Main application code
│   ├── agents/                   # Agent definitions (ATP, Artemis)
│   ├── codex/                    # Kernel, router, memory bus
│   ├── core/                     # Core utilities (instructions)
│   ├── integration/              # External integrations (MCP)
│   ├── interface/                # CLI interface
│   ├── launch/                   # Entry points
│   └── sandbox_city/             # Simulation environment
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

- **Documentation**: [docs/](docs/)
- **Security Guide**: [SECURITY.md](SECURITY.md)
- **API Reference**: [docs/MEMORY_INTEGRATION.md](docs/MEMORY_INTEGRATION.md)
- **Living City Metaphor**: [docs/LIVING_CITY.md](docs/LIVING_CITY.md)

---

Authored by Prinston (Apollo) Palmer - Systems Architect
With Claude (Anthropic) - AI Development Partner
