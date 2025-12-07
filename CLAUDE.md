---
editor_options: 
  markdown: 
    wrap: 250
---

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Artemis City** (v0.1.0) is an architectural framework for agentic reasoning with transparent, accountable action across distributed intelligence systems. It combines Python-based agent orchestration with a Node.js/TypeScript memory layer to enable
AI agents to operate with clear roles, boundaries, and trust management.

**Core Philosophy:** Balance trust, entropy, and collaboration to achieve "net good over noise" through iterative clarity and accountable collaboration (see `codex/manifesto.md`).

## Architecture

### Hybrid System Design

-   **Python Core**: Agent definitions, CLI interface, ATP protocol, persona system
-   **Node.js Memory Layer**: MCP server for Obsidian vault integration, REST API for knowledge base access
-   **Communication**: Artemis Transmission Protocol (ATP) for structured agent messaging

### Key Components

1.  **Agent System** (`src/agents/`)
    -   Agents defined with roles, access scopes, energy signatures, trust thresholds
    -   Current agents: `artemis` (governance), `pack_rat` (data transfer), `codex_daemon` (system status), `copilot` (assistance)
    -   Agent routing via keyword matching in `src/interface/agent_router.yaml`
    -   ATP protocol implementation in `src/agents/atp/` for structured communication
2.  **Integration Layer** (`src/integration/`)
    -   `memory_client.py`: Interface to MCP memory server
    -   `trust_interface.py`: Trust decay model implementation
    -   `context_loader.py`: Agent context and instruction loading
    -   `postal_service.py`: Secure data transfer between agents
3.  **CLI Interface** (`src/interface/codex_cli.py`)
    -   Main entry point for user interaction
    -   Loads agent configurations and routes commands
    -   Can run interactively or execute single commands
4.  **Memory Layer** (`src/Artemis Agentic Memory Layer/`)
    -   TypeScript/Express server providing MCP protocol
    -   Integrates with Obsidian vaults for persistent knowledge
    -   REST API for memory operations

## Development Commands

### Environment Setup

``` bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Install core dependencies
pip install -r src/launch/requirements.txt

# Install development dependencies (for testing, linting, formatting)
pip install -r src/launch/requirements-dev.txt
# OR: pip install -e '.[dev]'
```

### Running the Application

``` bash
# Start Memory Layer server (in terminal 1)
cd "src/Artemis Agentic Memory Layer"
npm install
npm run dev

# Run CLI interactively (in terminal 2)
python main.py

# Run CLI with single command
python main.py "ask artemis about system status"

# Run as installed command (after pip install -e .)
artemis
```

### Testing

``` bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=. --cov-report=html

# Run specific test file
pytest tests/test_atp.py -v

# Run tests matching a pattern
pytest tests/ -k "memory" -v

# Run tests by marker
pytest tests/ -m unit -v
pytest tests/ -m integration -v
```

**Test organization:** - `tests/test_atp.py`: ATP protocol parsing and validation - `tests/test_memory_integration.py`: Memory client and trust interface - `tests/test_artemis_persona.py`: Artemis persona reflection engine -
`tests/test_instruction_loader.py`: Agent instruction loading

### Code Quality

``` bash
# Using Makefile (from src/launch/)
cd src/launch
make lint          # Run all linters
make format        # Auto-format with Black and isort
make check         # Run all checks (format, lint, type)
make security      # Run security scans (Bandit, Safety)
make test          # Run test suite

# Direct commands
black .                    # Format code
isort .                    # Sort imports
flake8 .                   # Lint
mypy .                     # Type checking
bandit -r . -c pyproject.toml  # Security scan
```

### Memory Layer Development

``` bash
cd "src/Artemis Agentic Memory Layer"

# Install dependencies
npm install

# Start development server (with auto-reload)
npm run dev

# Build TypeScript
npm run build

# Start production server
npm start

# Lint TypeScript
npm run lint
```

## Code Organization

### Source Structure

```         
src/
├── agents/                # Agent definitions and implementations
│   ├── artemis/          # Artemis persona (governance agent)
│   ├── atp/              # Artemis Transmission Protocol
│   ├── agent_template.md # Template for new agents
│   └── *.md              # Agent specification files
├── integration/          # Integration components
│   ├── memory_client.py  # MCP memory server client
│   ├── trust_interface.py # Trust decay model
│   ├── context_loader.py # Agent instruction loader
│   └── postal_service.py # Inter-agent communication
├── interface/            # User interaction layer
│   ├── codex_cli.py     # Main CLI entry point
│   └── agent_router.yaml # Agent routing configuration
├── launch/               # Runtime configuration
│   ├── Makefile         # Development commands
│   └── requirements*.txt # Python dependencies
└── Artemis Agentic Memory Layer/  # Node.js MCP server
    └── src/
        ├── index.ts     # Server entry point
        ├── config/      # Configuration
        ├── mcp-server/  # MCP protocol implementation
        └── services/    # Business logic
```

### Important File Patterns

-   Agent specs: `src/agents/*.md` (artemis.md, pack_rat.md, etc.)
-   Agent implementations: `src/agents/<name>/` directories
-   Tests mirror source: `tests/test_<module>.py`
-   Configuration: YAML for routing, .env for secrets (never commit!)

## Coding Conventions

### Python Style

-   **Line length**: 100 characters (not 79)
-   **Formatting**: Black formatter, isort for imports (Black profile)
-   **Naming**:
    -   Functions/variables: `snake_case`
    -   Classes: `PascalCase`
    -   Constants: `UPPER_SNAKE_CASE`
    -   Private: `_leading_underscore`
-   **Docstrings**: Google-style for all public functions/classes
-   **Type hints**: Use where helpful, especially for public APIs
-   **Python version**: 3.8+ (CI tests on 3.10)

### TypeScript Style (Memory Layer)

-   **Line length**: 100 characters
-   **Indentation**: 2 spaces
-   **Quotes**: Single quotes preferred
-   **Linting**: ESLint with TypeScript plugin

### Project Conventions

-   Configuration files use YAML (agent_router.yaml, etc.)
-   Environment variables loaded from .env (never commit!)
-   Fail gracefully with informative error messages
-   Log configuration status, not secret values

## Key Concepts

### Artemis Transmission Protocol (ATP)

Structured communication format with signal tags: - `#Mode:` - Intent (Build, Review, Organize, Capture, Synthesize, Commit) - `#Context:` - Mission goal or purpose - `#Priority:` - Urgency (Critical, High, Normal, Low) - `#ActionType:` - Expected
response (Summarize, Scaffold, Execute, Reflect) - `#TargetZone:` - Project/folder area - `#SpecialNotes:` - Unusual instructions or warnings

**Implementation**: `src/agents/atp/atp_parser.py`, `atp_models.py`, `atp_validator.py`

### Trust Decay Model

Dynamic trust evaluation for agents, memories, and protocols: - Initial trust scores decay over time without reinforcement - Positive events (successful tasks, validations) increase trust - Negative events (failures, violations) decrease trust -
Trust thresholds trigger re-evaluation or access restrictions

**Implementation**: `src/integration/trust_interface.py`

### Agent Routing

Keywords in user commands map to agents via `src/interface/agent_router.yaml`: 1. User inputs command 2. Extract keywords from input 3. Match against agent keyword lists 4. Route to appropriate agent 5. Load agent instructions from
`src/agents/<name>.md` 6. Execute and return results

## Security Practices

**Critical**: Never commit secrets to version control!

-   Use `.env` files for all secrets (already in `.gitignore`)
-   Template: `.env.example` shows required variables
-   Setup script: `docs/setup_secrets.sh` for automated secure setup
-   Generate keys: `openssl rand -hex 32`
-   File permissions: `chmod 600 .env`
-   Load in code: `os.environ.get('VAR_NAME')`

**Protected patterns** (via .gitignore): - `.env*`, `*.key`, `*.pem`, `secrets/` - Credentials files, SSH keys, cloud configs - Database files (*.sqlite,* .db)

See `SECURITY.md` for comprehensive security guidelines.

## Common Development Patterns

### Adding a New Agent

1.  Create agent spec: `src/agents/<name>.md` using `agent_template.md`
2.  Add keywords to `src/interface/agent_router.yaml`
3.  (Optional) Create persona: `src/agents/<name>/persona.py`
4.  Add tests: `tests/test_<name>.py`
5.  Update documentation

### Working with ATP Messages

``` python
from agents.atp import ATPParser

parser = ATPParser()
message = parser.parse(user_input)
# Access: message.mode, message.context, message.priority, etc.
```

### Accessing Memory Layer

``` python
from integration.memory_client import MemoryClient

client = MemoryClient()
result = client.query(topic="agent_history")
```

### Loading Agent Instructions

``` python
from integration.context_loader import ContextLoader

loader = ContextLoader()
instructions = loader.load_agent_instructions("artemis")
```

## Testing Guidelines

-   Use pytest markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.slow`
-   Mock external services (MCP server) in unit tests
-   Use parametrized tests for protocol parsing variations
-   Coverage target: Aim for meaningful coverage on critical paths (ATP, memory integration, agent routing)
-   Tests requiring MCP server: Mark with `@pytest.mark.requires_server`

## Documentation Resources

-   `README.md`: User-facing overview and quick start
-   `SECURITY.md`: Security best practices and incident response
-   `CONTRIBUTING.md`: Detailed contribution guidelines
-   `docs/`: Additional guides and setup scripts
-   `codex/manifesto.md`: Project philosophy and principles
-   `tests/TEST_PLAN.md`: Comprehensive test scenarios

## Common Issues

1.  **Import errors**: Ensure virtual environment is activated
2.  **Module not found**: Install dependencies with `pip install -r src/launch/requirements.txt`
3.  **Memory Layer connection**: Start MCP server with `cd "src/Artemis Agentic Memory Layer" && npm run dev`
4.  **Directory path issues**: Note "Artemis Agentic Memory Layer" has space in name
5.  **Test failures**: Some tests may have API differences during development - focus on tests relevant to your changes

## CI/CD

Workflows in `.github/workflows/`: - `ci.yml`: Main CI pipeline (format, lint, test) - `code-quality.yml`: Extended quality checks - `dependencies.yml`: Dependency management - `release.yml`: Package building and release

CI runs on: Python 3.10, Node.js 18+
