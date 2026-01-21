# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Artemis City is an architectural framework for aligning agentic reasoning with transparent, accountable action. It provides agent definitions, memory management with trust decay, secure communication via the Artemis Transmission Protocol (ATP), and simulation environments.

**Primary Languages:** Python 3.8+ (core logic), TypeScript (MCP server)

## Build & Development Commands

### Python Setup
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -e '.[dev]'    # Install with dev dependencies
```

### Running the CLI
```bash
python app/launch/main.py                    # Interactive mode
python app/launch/main.py "your command"     # Single command
python app/launch/main.py "#Mode: Build #Context: Feature request"  # With ATP headers
```

### Testing
```bash
pytest                                    # All tests
pytest tests/ -v                          # Verbose
pytest tests/test_atp.py -v               # Single file
pytest -m unit                            # By marker (unit, integration, e2e, slow)
pytest --cov=app --cov-report=html        # With coverage
```

### Linting & Formatting
```bash
black app/ tests/                         # Format Python
isort app/ tests/                         # Sort imports
flake8 app/ tests/                        # Lint
mypy app/                                 # Type check
npm run lint                              # ESLint for TypeScript
npm run format                            # Prettier
```

### MCP Server
```bash
cd MCP && npm install && npm run dev
```

## Architecture

```
app/
├── agents/
│   ├── artemis/          # ArtemisPersona, ReflectionEngine, SemanticTagger
│   └── atp/              # ATPMessage, ATPParser, ATPValidator
├── codex/
│   ├── kernel.py         # Central orchestrator
│   ├── agent_router.py   # Keyword-based command routing
│   └── memory_bus.py     # Persistent memory with pluggable backends
├── integration/          # MemoryClient, TrustInterface, ContextLoader
├── interface/            # CLI interface, agent_router.yaml config
└── launch/main.py        # Main entry point
MCP/                      # TypeScript MCP memory server (Obsidian integration)
```

### Key Data Flows

1. **CLI Input** → ATP Parser extracts headers → Kernel routes to agent
2. **Agent Processing** → Memory Bus for persistence → Trust Interface validates access
3. **Instructions** loaded hierarchically: global < project < local < agent-specific

### Core Components

- **Kernel** (`app/codex/kernel.py`): Orchestrates command processing, agent instantiation, memory bus
- **Agent Router**: Routes commands via keyword matching defined in `app/interface/agent_router.yaml`
- **ATP Parser**: Parses `#Mode:`, `#Context:`, `#Priority:`, `#ActionType:`, `#TargetZone:` headers
- **Trust Interface**: Implements trust decay model - scores decay over time, reinforced by successful actions

### Agent System

| Agent | Role | Keywords |
|-------|------|----------|
| Artemis | Governance, dispute resolution | artemis, governance, policy, audit |
| Copilot | Real-time assistant | help, assist, explain, suggest |
| Pack Rat | Secure data transfer | transfer, send, receive, courier |
| Codex Daemon | System status, memory interface | memory, system, daemon, config |

New agents: copy `app/agents/agent_template.md`, implement handler class, register in `agent_router.yaml`.

## Code Conventions

- **Docstrings**: Google-style for all public functions
- **Line length**: 100 characters (Black configured)
- **Type hints**: Required for public APIs (`mypy --strict` configured)
- **Imports**: Standard library → third-party → local (`isort` enforced)
- **Configuration**: YAML for agent routing, TOML for project settings

## ATP Protocol

Structured communication headers:
```
#Mode: Build | Review | Organize | Capture | Synthesize | Commit
#Context: <brief mission goal>
#Priority: Critical | High | Normal | Low
#ActionType: Summarize | Scaffold | Execute | Reflect
#TargetZone: <path or project area>
```

## Guiding Principles

From `codex/manifesto.md`:
- **Net Good Over Noise**: Prioritize meaningful contributions
- **Transparent Accountability**: All actions auditable and attributable
- **Iterative Clarity**: Living documentation, continuous improvement
- **Restraint**: Choosing not to act is sometimes most responsible

Agent boundaries are strict - never suggest features that violate defined access scopes. All significant actions should include rationale.
