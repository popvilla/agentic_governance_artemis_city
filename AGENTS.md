# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Artemis City** is a comprehensive framework for aligning agentic reasoning with transparent, accountable action. It provides agent definitions with clear roles/boundaries, memory management with trust decay models, secure communication via ATP (Artemis Transmission Protocol), and simulation environments.

**Core Mission**: Balance trust, entropy, and collaboration through iterative clarity and accountable collaboration ("net good over noise").

## Common Development Commands

### Environment Setup

```bash
# Set up secure environment (REQUIRED FIRST STEP)
./setup_secrets.sh

# Create and activate Python virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Install Python dependencies
pip install -r requirements.txt

# Install with development tools
pip install -e '.[dev]'

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### Running the Application

```bash
# CLI - Interactive mode
python app/launch/main.py

# CLI - Single command mode
python app/launch/main.py "ask artemis about system status"

# CLI - With ATP headers
python app/launch/main.py "#Mode: Build #Context: Feature request #ActionType: Execute"
```

### Testing

```bash
# Run all tests
pytest

# Run with verbosity
pytest tests/ -v

# Run specific test file
pytest tests/test_atp.py -v

# Run by marker
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests only
pytest -m e2e              # End-to-end tests

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Integration tests (requires MCP server running)
pytest tests/integration/ -m integration
```

### Code Quality

```bash
# Python formatting
black app/ tests/
isort app/ tests/

# Python linting
flake8 app/ tests/
mypy app/

# TypeScript/JavaScript (if working with MCP server components)
npm run lint
npm run lint:fix
npm run format
npm run typecheck

# Run all validation
npm run validate           # TypeScript checks
npm run validate:all       # Both Python and TypeScript

# Pre-commit on all files
pre-commit run --all-files
```

### Development Workflow

```bash
# Format Python code before committing
black app/ tests/ && isort app/ tests/

# Run full quality check
pytest tests/ -v && flake8 app/ tests/ && black --check app/ tests/

# Check complexity (JSF AV Rule 3 - max 20)
radon cc app --min D --show-complexity
```

## High-Level Architecture

### System Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLI Interface Layer                           │
│          (app/launch/main.py, app/interface/)                   │
│     - User interaction                                           │
│     - ATP header parsing                                         │
│     - Command routing entry point                                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    Protocol Layer                                │
│                  (app/agents/atp/)                               │
│     - ATPParser: Parses #Mode:, #Context:, #Priority:, etc.     │
│     - ATPValidator: Validates ATP message structure             │
│     - ATPMessage: Structured message representation             │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    Kernel Layer                                  │
│                  (app/codex/kernel.py)                           │
│     - Central orchestrator for all subsystems                    │
│     - AgentRouter: Keywords → agent mapping                      │
│     - MemoryBus: Persistent memory operations                    │
│     - State management with boot counting                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    Agent Layer                                   │
│      (app/agents/, app/codex/agents/)                            │
│     - ArtemisPersona: Governance, reflection, semantic tagging   │
│     - PlannerAgent: Planning and scaffolding                     │
│     - CodexAgent: Generic agent base                             │
│     - Base agent contracts in app/codex/agents/base.py           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    Integration Layer                             │
│                  (app/integration/)                              │
│     - MemoryClient: Obsidian vault operations (MCP protocol)     │
│     - TrustInterface: Trust decay model implementation           │
│     - ContextLoader: Hierarchical instruction loading            │
│     - PostalService: Secure agent-to-agent data transfer         │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Patterns

**1. Command Processing Flow**

```
User Input (with ATP headers)
    → ATPParser extracts headers + content
    → Kernel routes based on keywords (agent_router.yaml)
    → Agent instance created via _get_agent_instance()
    → Agent.handle(request, memory) processes command
    → MemoryBus persists state if needed
    → Response returned through layers
```

**2. Memory Flow**

```
Agent operation
    → TrustInterface checks agent permissions (trust score)
    → MemoryClient makes REST call to Obsidian (if external MCP server)
    → OR MemoryBus handles local persistence
    → Trust score updated based on success/failure
    → Operation logged to kernel state
```

**3. Instruction Loading Flow**

```
Hierarchical precedence (lowest to highest):
    1. Global instructions (system-wide)
    2. Project instructions (project root)
    3. Local instructions (current directory)
    4. Agent-specific instructions

get_global_cache() → InstructionCache → ContextLoader
    → Merges all scopes in precedence order
    → Returns InstructionSet with merged content
```

## Key Architectural Concepts

### ATP (Artemis Transmission Protocol)

Structured communication format using signal tags:

- **#Mode:** Overall intent (Build, Review, Organize, Capture, Synthesize, Commit)
- **#Context:** Mission goal (free text description)
- **#Priority:** Urgency level (Critical, High, Normal, Low)
- **#ActionType:** Expected response (Summarize, Scaffold, Execute, Reflect)
- **#TargetZone:** Project area (path or scope)
- **#SpecialNotes:** Exceptions or special instructions

**Implementation**: All parsing happens in `app/agents/atp/atp_parser.py` using regex patterns. The parser extracts headers and remaining content, returning an `ATPMessage` object.

### Agent Router

**Location**: `app/interface/agent_router.yaml`

Maps agent names to:

- **role**: Human-readable agent purpose
- **keywords**: List of trigger words for routing
- **action_description**: What agent does when invoked

**Current agents**:

- **artemis**: Governance, policy, audits (keywords: artemis, governance, policy, audit)
- **pack_rat**: Secure data transfer (keywords: transfer, send, receive, courier)
- **codex_daemon**: System status, memory interface (keywords: memory, system, daemon, status)
- **copilot**: Assistance, explanations (keywords: help, assist, explain, suggest)

To add a new agent: Add entry to yaml → implement handler class → register in Kernel._get_agent_instance()

### Trust Decay Model

**Purpose**: Dynamic trust evaluation framework ensuring agents maintain accountability.

**Key concepts**:

- **Initial Trust Score**: Baseline for new entities (typically 0.5-0.7)
- **Decay Rate**: Trust erodes over time without reinforcement
- **Reinforcement Events**: Successful actions increase trust
- **Trust Thresholds**: Trigger access restrictions when crossed

**Implementation**: `app/integration/trust_interface.py` provides:

- `can_perform_operation(agent_name, operation)`: Permission check
- `record_success(agent_name)`: Reinforce trust
- `record_failure(agent_name)`: Decay trust faster

**Trust Levels**:

- FULL (0.9-1.0): All operations
- HIGH (0.7-0.9): Read, write, search, tag, update
- MEDIUM (0.5-0.7): Read, write, search, tag
- LOW (0.3-0.5): Read, search only
- UNTRUSTED (<0.3): No operations

### Memory Integration

**External MCP Server** (if used): REST API to Obsidian vault

- Endpoint: Configurable via OBSIDIAN_BASE_URL
- Authentication: Bearer token (MCP_API_KEY)
- Operations: read, write, search, delete, frontmatter, tags
- Client: `app/integration/memory_client.py`

**Internal Memory Bus**: `app/codex/memory_bus.py`

- Simple in-memory or file-based persistence
- Used by kernel for state management
- Pluggable backend design

### Kernel State Management

**Location**: `state_kernel.json` (created at runtime)

**Contents**:

- `boot_count`: Number of times kernel has initialized
- `history`: Array of all processed requests
- Additional agent-specific state as needed

**Lifecycle**:

1. `_load_state()`: Read from disk or initialize defaults
2. `process()`: Handle request and append to history
3. `_save_state()`: Persist to disk after each operation

### Instruction Hierarchy

**Purpose**: Context-aware agent behavior based on scope.

**Loader**: `app/core/instructions.py` (assumed based on imports in main.py)

**Precedence** (highest wins):

1. Agent-specific instructions
2. Local directory instructions
3. Project-level instructions  
4. Global system instructions

**Usage in code**:

```python
instruction_cache = get_global_cache()
instruction_set = instruction_cache.get(agent_name="artemis")
# instruction_set.scopes contains merged instructions
```

## Code Organization

```
app/
├── agents/              # Agent implementations
│   ├── artemis/         # ArtemisPersona, reflection engine, semantic tagging
│   │   ├── persona.py
│   │   ├── reflection.py
│   │   └── semantic_tagging.py
│   └── atp/             # ATP protocol parser and models
│       ├── atp_parser.py
│       ├── atp_validator.py
│       └── atp_models.py
├── codex/               # Core system components
│   ├── kernel.py        # Central orchestrator
│   ├── agent_router.py  # Command → agent routing logic
│   ├── memory_bus.py    # Memory operations
│   └── agents/          # Base agent contracts
│       ├── base.py      # Agent abstract base class
│       ├── codex_agent.py
│       └── planner_agent.py
├── integration/         # External service integrations
│   ├── memory_client.py       # MCP/Obsidian REST client
│   ├── trust_interface.py     # Trust decay model
│   ├── context_loader.py      # Instruction hierarchies
│   └── postal_service.py      # Agent-to-agent messaging
├── interface/           # User-facing components
│   ├── codex_cli.py     # CLI implementation
│   └── agent_router.yaml # Agent routing configuration
├── launch/              # Entry points
│   └── main.py          # Main CLI entry with ATP support
└── sandbox_city/        # Testing/simulation environment
    └── networked_scripts/
```

## Coding Standards (JSF-Adapted)

This project follows JSF (Joint Strike Fighter) C++ standards adapted for Python:

### Critical Rules

1. **Complexity Limit**: Cyclomatic complexity ≤ 20 (most functions ≤ 10)
   - Enforced by pre-commit hook: `radon cc app --min D`

2. **Function Length**: ≤ 200 logical lines (aim for ~50)

3. **Function Parameters**: ≤ 7 parameters
   - Use configuration dicts/dataclasses if more needed

4. **Type Safety**: Google-style docstrings with types for all public functions
   - Type checking enforced via mypy in pre-commit

5. **Resource Management**: Always use context managers for file operations

   ```python
   # Correct
   with open(path, 'r') as f:
       data = yaml.safe_load(f)
   ```

6. **Error Handling**: Explicit, never silent
   - Log errors at minimum
   - Raise specific exceptions
   - No bare `except:` clauses

7. **No Magic Numbers**: Use named constants

   ```python
   MAIL_DELIVERY_FAILURE_RATE = 0.10
   ```

8. **Safe YAML**: Always `yaml.safe_load()`, never `yaml.load()`

### Documentation Requirements

- **All public functions**: Google-style docstrings with Args, Returns, Raises
- **Module docstrings**: Purpose, usage example, dependencies
- **Inline comments**: Explain "why", not "what"
- **Minimum 80% docstring coverage** (enforced by interrogate pre-commit hook)

### Code Style

- **Formatter**: Black with 100-char line length
- **Import sorting**: isort with black profile
- **Linter**: flake8 with plugins (docstrings, bugbear, comprehensions, simplify)
- **Type checking**: mypy in strict mode for app/ (not tests/)
- **Pre-commit**: All checks must pass before commit

## Testing Strategy

### Test Organization

- `tests/`: All test files prefixed with `test_`
- `tests/integration/`: Tests requiring external services
- **Markers**: unit, integration, e2e, slow, requires_server

### Key Test Areas

1. **ATP Parsing** (`test_atp.py`):
   - Header extraction
   - Content parsing
   - Validation rules

2. **Artemis Persona** (`test_artemis_persona.py`):
   - Context memory
   - Reflection engine
   - Mode switching

3. **Instruction Loading** (`test_instruction_loader.py`):
   - Hierarchical merging
   - Scope precedence
   - Cache invalidation

4. **Memory Integration** (`test_memory_integration.py`):
   - Trust-based access control
   - MCP client operations
   - Error handling

### Running Specific Tests

```bash
# Single test class
pytest tests/test_atp.py::TestATPParser -v

# Single test method
pytest tests/test_atp.py::TestATPParser::test_parse_with_headers -v

# Tests matching pattern
pytest -k "artemis" -v

# Exclude slow tests
pytest -m "not slow"
```

## Security Considerations

### Secret Management

- **Never commit** `.env` files (protected by `.gitignore` and pre-commit hooks)
- **Use** `setup_secrets.sh` for initial environment setup
- **Generate API keys**: `openssl rand -hex 32`
- **File permissions**: `chmod 600 .env`
- **Pre-commit checks**:
  - `detect-secrets`: Scans for accidentally committed secrets
  - Custom patterns for API_KEY, SECRET, PASSWORD
  - Blocks .env files (except .env.example)

### Input Validation

- All command inputs validated at CLI boundary
- Agent router keywords sanitized (lowercase matching)
- File paths validated to prevent directory traversal
- YAML loading always uses `safe_load()`

### Trust Model Integration

Before any sensitive operation:

```python
from integration import get_trust_interface

trust = get_trust_interface()
if trust.can_perform_operation('agent_name', 'write'):
    # Perform operation
    trust.record_success('agent_name')
else:
    # Deny operation
    trust.record_failure('agent_name')
```

## Development Patterns

### Adding a New Agent

1. **Define agent in** `app/interface/agent_router.yaml`:

   ```yaml
   my_agent:
     role: "Description of role"
     keywords: ["keyword1", "keyword2"]
     action_description: "What agent does"
   ```

2. **Implement agent class** in `app/codex/agents/`:

   ```python
   from codex.agents.base import Agent
   
   class MyAgent(Agent):
       def handle(self, request, memory):
           content = request.get("content", "")
           # Process and return response
           return f"Processed: {content}"
   ```

3. **Register in kernel** at `app/codex/kernel.py`:

   ```python
   def _get_agent_instance(self, agent_name):
       if agent_name == "my_agent":
           return MyAgent(agent_name)
       # ... existing agents
   ```

4. **Add tests** in `tests/test_my_agent.py`

### Modifying ATP Protocol

1. Update models in `app/agents/atp/atp_models.py`
2. Update parser regex in `app/agents/atp/atp_parser.py`
3. Update validator rules in `app/agents/atp/atp_validator.py`
4. Add tests in `tests/test_atp.py`
5. Document new headers in relevant docs

### Working with Memory

```python
# Using MemoryBus (local)
memory = MemoryBus()
memory.save("key", {"data": "value"})
data = memory.load("key")

# Using MemoryClient (external Obsidian)
from integration import MemoryClient

client = MemoryClient(
    base_url="http://localhost:3000",
    api_key="your_key"
)
client.store_agent_context("artemis", "Session completed")
context = client.retrieve_agent_context("artemis")
```

## CI/CD Pipeline

GitHub Actions workflows in `.github/workflows/`:

- **code-quality.yml**: Linting, formatting, type checking
- **dependencies.yml**: Security updates, dependency scanning
- **release.yml**: Automated releases with semantic versioning
- **jekyll-gh-pages.yml**: Documentation site deployment

All PRs must pass:

1. Pre-commit hooks (local)
2. Code quality checks (CI)
3. Test suite (pytest)
4. Type checking (mypy)

## Guiding Principles

From `codex/manifesto.md` (referenced in CODING_STANDARDS.md):

1. **Net Good Over Noise**: Prioritize meaningful contributions
2. **Transparent Accountability**: All actions auditable and attributable
3. **Iterative Clarity**: Living documentation, continuous improvement
4. **Restraint**: Choosing not to act is sometimes most responsible

**Agent boundaries are strict** - never suggest features that violate defined access scopes. All significant actions should include rationale in code comments or docstrings.

## Additional Resources

- **README.md**: User-facing documentation, quick start guide
- **CLAUDE.md**: Claude-specific guidance (similar to this file)
- **CODING_STANDARDS.md**: Detailed JSF-adapted coding standards
- **CONTRIBUTING.md**: Contribution guidelines
- **docs/**: Comprehensive documentation
  - `MEMORY_INTEGRATION.md`: Memory layer API reference
  - `LIVING_CITY.md`: Architectural philosophy
  - `trust_decay_model.md`: Trust mathematics
  - `kernel.md`: Kernel architecture details
  - `INSTALL.md`: Detailed installation guide
  - `CICD.md`: CI/CD documentation

## Common Gotchas

1. **PYTHONPATH**: When running tests or scripts, ensure `app/` is on PYTHONPATH or run from project root
2. **Agent router path**: main.py expects `agent_router.yaml` at `app/interface/agent_router.yaml` relative to script location
3. **State file**: `state_kernel.json` created in working directory - can accumulate, consider .gitignore
4. **MCP server**: Integration tests require external MCP server running (mark with `@pytest.mark.requires_server`)
5. **Pre-commit performance**: Radon complexity check can be slow - use `SKIP=radon-complexity git commit` if needed for draft commits
6. **Type checking**: mypy configured strictly for app/ but lenient for tests/ - don't add type hints to test files unless required
