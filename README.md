# agentic_governance_artemis_city

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

```asiic
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
└─────────────────────────────────────────────────────────────────

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

1. Implement agent class:

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

1. Register in `agent_router.yaml`

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
