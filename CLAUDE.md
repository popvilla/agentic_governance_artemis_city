# CLAUDE.md - AI Assistant Guide for Artemis City

> **Purpose:** This document provides comprehensive context for AI assistants (like Claude) working with the Artemis City codebase. It explains the project structure, philosophy, key conventions, and development workflows to ensure consistent and informed assistance.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Core Philosophy & Principles](#core-philosophy--principles)
3. [Repository Structure](#repository-structure)
4. [Agent System Architecture](#agent-system-architecture)
5. [Key Protocols & Models](#key-protocols--models)
6. [Development Workflows](#development-workflows)
7. [Coding Conventions](#coding-conventions)
8. [Important Files Reference](#important-files-reference)
9. [Working with This Codebase](#working-with-this-codebase)
10. [Communication Patterns](#communication-patterns)

---

## Project Overview

**Artemis City** is an architectural framework designed to align agentic reasoning with transparent, accountable action across distributed intelligence systems—both human and machine. This is **Version Zero**, providing foundational scaffolding for:

- Defining agents with clear roles and boundaries
- Managing memory with trust decay models
- Establishing secure communication interfaces
- Simulating environments for testing agent interactions

### Key Metadata
- **Project Name:** Artemis City (agentic-codex)
- **Version:** 0.1.0
- **License:** MIT
- **Primary Language:** Python 3.13+
- **Main Entry Point:** `interface/codex_cli.py`
- **Demo Scripts:** `demo_artemis.py`, `demo_memory_integration.py`
- **Author:** Prinston Palmer

### Mission Statement
Balance **trust**, **entropy**, and **collaboration** to achieve "net good over noise" through iterative clarity and accountable collaboration.

---

## Core Philosophy & Principles

The project follows the **Codex Manifesto** (`codex/manifesto.md`), which establishes these core tenets:

### 1. **Iterative Clarity, Not Static Truth**
- The Codex is a living document
- Evolves with understanding and experience
- Embrace continuous improvement

### 2. **Net Good Over Noise**
- Prioritize actions that contribute positively to system goals
- Filter information through ethical boundaries
- Focus on meaningful contributions

### 3. **Transparent Accountability**
- Every agent's actions are auditable and attributable
- Clear documentation of roles and responsibilities
- Traceable decision-making processes

### 4. **Collaborative Autonomy**
- Agents operate with defined autonomy within a collaborative framework
- Clear boundaries prevent scope creep
- Interdependencies are explicitly defined

### 5. **Resilience through Entropy Management**
- Acknowledge natural decay and drift in complex systems
- Implement countermeasures proactively
- Use Trust Decay Model to manage reliability

---

## Repository Structure

```
Artemis-City/
│
├── agents/                    # Agent definitions and specifications
│   ├── agent_template.md      # Template for creating new agents
│   ├── artemis.md            # Mayor protocol, governance agent
│   ├── copilot.md            # Companion, elastic augmentation agent
│   ├── pack_rat.md           # Courier role, secure data transfer agent
│   ├── codex_daemon.md       # System anchor, memory interface agent
│   ├── artemis/              # Artemis agent Python implementation
│   │   ├── __init__.py       # Exports ArtemisPersona, ReflectionEngine, SemanticTagger
│   │   ├── persona.py        # ArtemisPersona class and ResponseMode enum
│   │   ├── reflection.py     # ReflectionEngine, ConceptGraph, ConceptNode
│   │   └── semantic_tagging.py # SemanticTagger, SemanticTag, Citation
│   └── atp/                  # Artemis Transmission Protocol implementation
│       ├── __init__.py       # Exports ATPMessage, ATPParser, ATPValidator
│       ├── atp_models.py     # ATPMessage, ATPMode, ATPPriority, ATPActionType
│       ├── atp_parser.py     # ATPParser for parsing ATP-formatted messages
│       └── atp_validator.py  # ATPValidator, ValidationResult
│
├── codex/                     # Core principles and philosophy
│   └── manifesto.md          # Foundational principles document
│
├── core/                      # Core system functionality
│   ├── __init__.py
│   └── instructions/         # Instruction management system
│       ├── __init__.py       # Exports InstructionLoader, InstructionSet, cache utilities
│       ├── instruction_loader.py  # InstructionLoader, InstructionSet dataclass
│       └── instruction_cache.py   # InstructionCache for caching loaded instructions
│
├── interface/                 # User-facing components
│   ├── codex_cli.py          # Main CLI for interacting with agents
│   ├── agent_router.yaml     # Keyword-based routing configuration
│   └── translator_protocol.md # Communication encoding standards
│
├── launch/                    # Governance and release management
│   ├── open_source_covenant.md # Open source principles
│   └── release_gatecheck.md   # Release validation criteria
│
├── memory/                    # Memory management frameworks
│   ├── trust_decay_model.md  # Trust scoring and decay mechanics
│   ├── memory_lawyer.md      # Memory validation protocols
│   ├── validation_simulations.md # Testing frameworks
│   └── integration/          # Memory integration Python implementation
│       ├── __init__.py       # Exports MemoryClient, TrustInterface, ContextLoader
│       ├── memory_client.py  # MemoryClient, MCPResponse, MCPOperation
│       ├── trust_interface.py # TrustInterface, TrustScore, TrustLevel
│       └── context_loader.py # ContextLoader, ContextEntry
│
├── sandbox_city/             # Simulation environment
│   ├── index.md              # Overview of sandbox environment
│   ├── semantic_zones.md     # Zone definitions
│   └── networked_scripts/
│       └── mail_delivery_sim.py # Secure mail transfer simulation
│
├── Artemis Agentic Memory Layer/  # External memory layer integration
│   ├── README.md             # Memory layer documentation
│   ├── docker-compose.yml    # Docker configuration for memory services
│   └── pyproject.toml        # Memory layer Python configuration
│
├── demo_artemis.py           # Demo script for Artemis agent features
├── demo_memory_integration.py # Demo script for memory integration
├── ARTEMIS_FEATURES.md       # Artemis agent feature documentation
├── MEMORY_INTEGRATION.md     # Memory integration documentation
├── WARP.md                   # Warp terminal integration documentation
├── CLAUDE.md                 # AI assistant guide (this file)
├── .gitignore                # Comprehensive ignore patterns
├── LICENSE                   # MIT License
├── README.md                 # User-facing documentation
├── requirements.txt          # Python dependencies (PyYAML>=6.0)
├── package.json              # Project metadata
└── pyproject.toml            # Python project configuration
```

---

## Agent System Architecture

### Agent Definition Framework

All agents follow a standardized template (`agents/agent_template.md`) with these required fields:

| Field | Description |
|-------|-------------|
| **Agent Name** | Unique identifier (e.g., "Artemis", "Pack Rat") |
| **System Access Scope** | Boundaries of resource/data access |
| **Semantic Role** | Primary function and purpose |
| **Energy Signature** | Computational footprint (low/moderate/high-compute) |
| **Linked Protocols** | Communication and operational protocols |
| **Drift Countermeasures** | Mechanisms to prevent behavioral deviation |
| **Trust Threshold Triggers** | Conditions that trigger trust re-evaluation |

### Current Agents

#### 1. **Artemis** (Mayor Protocol, Governance)
- **Role:** System overseer, governance, dispute resolution
- **Access:** Full read access to agent/memory logs, write to governance protocols
- **Energy:** Moderate, event-driven (policy violations, disputes, audits)
- **Keywords:** `artemis`, `governance`, `policy`, `audit`, `dispute`, `review`

#### 2. **Copilot** (Companion, Elastic Augmentation)
- **Role:** Real-time assistant, contextual information provider
- **Access:** Read current agent context and public memory, write to communication channels
- **Energy:** Moderate, on-demand, scales with interaction
- **Keywords:** `help`, `assist`, `explain`, `augment`, `clarify`, `suggest`

#### 3. **Pack Rat** (Courier Role, Safe Transfer)
- **Role:** Secure data transfer between agents/components
- **Access:** Read/write to secure transfer zones, limited read to communication channels
- **Energy:** Low-compute, transaction-based
- **Keywords:** `transfer`, `send`, `receive`, `courier`, `data`, `secure`

#### 4. **CompSuite** (formerly Codex Daemon - System Anchor, Memory Interface)
- **Role:** System status monitoring, memory interface, configuration management
- **Access:** System-level access to memory and configuration
- **Energy:** Low-compute, continuous monitoring
- **Keywords:** `memory`, `system`, `daemon`, `config`, `status`, `health`

### Agent Routing Mechanism

The CLI uses keyword-based routing defined in `interface/agent_router.yaml`:

1. User inputs command
2. System matches keywords against agent definitions
3. Command routed to appropriate agent
4. Agent performs action within defined scope
5. Results returned through interface

---

## Key Protocols & Models

### 1. **Trust Decay Model** (`memory/trust_decay_model.md`)

Dynamic trust evaluation framework with these components:

- **Initial Trust Score:** Baseline trust for new agents/memories/protocols
- **Decay Rate:** Natural erosion over time without reinforcement
- **Reinforcement Events:** Successful tasks, validations, protocol adherence increase trust
- **Negative Events:** Failures, violations, inconsistencies decrease trust
- **Trust Thresholds:** Trigger re-evaluation, restricted access, or increased scrutiny

**Applications:**
- Agent Trust: Influences resource access and reliability
- Memory Trust: Determines weight given to memory entries
- Protocol Trust: Confidence in protocol effectiveness

### 2. **Translator Protocol** (`interface/translator_protocol.md`)

Ensures consistent communication across languages and encoding systems:

- **Standard Encoding:** UTF-8 for all internal communications
- **Transliteration Rules:** Algorithms for converting text between writing systems
- **Language Detection:** Identify source language of incoming text
- **Error Reporting:** Automated alerts for encoding/transliteration issues
- **Human Review Loop:** Triggered for complex or ambiguous cases

### 3. **Artemis Transmission Protocol (ATP)**

Structured communication system with signal tags:

| Tag | Purpose |
|-----|---------|
| `#Mode:` | Overall intent (Build, Review, Organize, Capture, Synthesize, Commit) |
| `#Context:` | Brief mission goal or purpose |
| `#Priority:` | Urgency level (Critical, High, Normal, Low) |
| `#ActionType:` | Expected response (Summarize, Scaffold, Execute, Reflect) |
| `#TargetZone:` | Project/folder area for the work |
| `#SpecialNotes:` | Unusual instructions, warnings, or exceptions |

---

## Development Workflows

### Setting Up Development Environment

```bash
# 1. Clone repository
git clone <repository-url>
cd Artemis-City

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Running the CLI

**Interactive Mode:**
```bash
python interface/codex_cli.py
```

**Single Command Mode:**
```bash
python interface/codex_cli.py "ask artemis about system status"
```

### Running Simulations

```bash
python sandbox_city/networked_scripts/mail_delivery_sim.py
```

### Testing Workflow

Currently, the project uses manual testing:
- Test CLI routing with various commands
- Run simulations to verify agent interactions
- Validate protocol compliance manually

**Note:** Test infrastructure is pending (`package.json` shows "no test specified")

---

## Coding Conventions

### Python Style Guidelines

1. **Documentation:**
   - Use Google-style docstrings for all public functions
   - Include Args, Returns, and Raises sections
   - Document module-level functionality at the top

2. **Code Organization:**
   - Keep functions focused and single-purpose
   - Use descriptive variable and function names
   - Maintain clear separation of concerns

3. **Error Handling:**
   - Fail gracefully with informative messages
   - Return empty/default values when appropriate
   - Log errors for debugging

4. **Configuration:**
   - Use YAML for configuration files
   - Keep configuration separate from code
   - Validate configuration on load

### Example from `codex_cli.py`:

```python
def load_agent_router_config(config_path):
    """Loads agent routing configurations from a specified YAML file.

    This function reads a YAML file that defines the routing logic for different
    agents based on command keywords. It's designed to fail gracefully by
    returning an empty dictionary if the file doesn't exist.

    Args:
        config_path (str): The full path to the agent router YAML config file.

    Returns:
        dict: A dictionary containing the agent router configuration. Returns an
              empty dictionary if the configuration file cannot be found.
    """
    if not os.path.exists(config_path):
        print(f"Error: Agent router config not found at {config_path}")
        return {}
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
```

### Agent Definition Conventions

When creating new agents:

1. Copy `agents/agent_template.md`
2. Fill in all required fields completely
3. Ensure semantic role is clear and concise
4. Define precise access boundaries
5. Specify concrete drift countermeasures
6. List specific trust threshold triggers
7. Update `interface/agent_router.yaml` with keywords

### File Naming Conventions

- **Agents:** lowercase with underscores (e.g., `pack_rat.md`)
- **Python scripts:** lowercase with underscores (e.g., `codex_cli.py`)
- **Documentation:** lowercase with underscores (e.g., `trust_decay_model.md`)
- **Configuration:** lowercase with underscores (e.g., `agent_router.yaml`)

---

## Important Files Reference

### Configuration Files

| File | Purpose | Format |
|------|---------|--------|
| `interface/agent_router.yaml` | Agent keyword routing | YAML |
| `requirements.txt` | Python dependencies | Text |
| `package.json` | Project metadata | JSON |
| `pyproject.toml` | Python project config | TOML |
| `.gitignore` | Version control exclusions | Text |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | User-facing project documentation |
| `CLAUDE.md` | AI assistant guide (this file) |
| `ARTEMIS_FEATURES.md` | Artemis agent feature documentation |
| `MEMORY_INTEGRATION.md` | Memory integration documentation |
| `WARP.md` | Warp terminal integration documentation |
| `codex/manifesto.md` | Core principles and philosophy |
| `agents/agent_template.md` | Template for new agents |
| `launch/open_source_covenant.md` | Open source principles |
| `interface/translator_protocol.md` | Communication standards |
| `memory/trust_decay_model.md` | Trust scoring mechanics |

### Executable Files

| File | Purpose |
|------|---------|
| `interface/codex_cli.py` | Main CLI entry point |
| `demo_artemis.py` | Demo script for Artemis agent features |
| `demo_memory_integration.py` | Demo script for memory integration |
| `sandbox_city/networked_scripts/mail_delivery_sim.py` | Mail delivery simulation |

### Python Modules

| Module | Purpose |
|--------|---------|
| `agents/artemis/` | ArtemisPersona, ReflectionEngine, SemanticTagger |
| `agents/atp/` | ATPMessage, ATPParser, ATPValidator |
| `core/instructions/` | InstructionLoader, InstructionCache |
| `memory/integration/` | MemoryClient, TrustInterface, ContextLoader |

---

## Working with This Codebase

### When Adding New Features

1. **Understand the Philosophy:**
   - Read `codex/manifesto.md` first
   - Ensure alignment with core tenets
   - Prioritize "net good over noise"

2. **Define Scope Clearly:**
   - Identify which agents are affected
   - Check system access boundaries
   - Document expected behavior

3. **Follow Existing Patterns:**
   - Use existing code as examples
   - Maintain consistent documentation style
   - Follow Google-style docstrings

4. **Consider Trust & Security:**
   - How does this affect trust scores?
   - What drift countermeasures are needed?
   - Are access boundaries respected?

### When Creating New Agents

1. Start with `agents/agent_template.md`
2. Define semantic role precisely
3. Set appropriate energy signature
4. Link relevant protocols
5. Specify drift countermeasures
6. Add keywords to `agent_router.yaml`
7. Test routing through CLI
8. Document in this file

### When Modifying Existing Agents

1. Review current agent definition
2. Check impact on linked protocols
3. Update trust threshold triggers if needed
4. Modify `agent_router.yaml` if keywords change
5. Test routing thoroughly
6. Update documentation

### When Working with Memory/Trust

1. Understand Trust Decay Model first
2. Consider how changes affect trust scores
3. Document trust implications
4. Implement appropriate logging
5. Test edge cases for trust thresholds

---

## Communication Patterns

### For AI Assistants Working with This Codebase

1. **Always Consider Context:**
   - This is a multi-agent system
   - Actions have trust implications
   - Transparency is paramount

2. **Respect Agent Boundaries:**
   - Don't suggest features that violate access scopes
   - Maintain separation of concerns
   - Follow defined protocols

3. **Prioritize Documentation:**
   - All changes should be documented
   - Use Google-style docstrings
   - Update relevant markdown files

4. **Think in Terms of Roles:**
   - Which agent would handle this?
   - What is the semantic purpose?
   - How does this align with the manifesto?

5. **Consider Entropy Management:**
   - How might this drift over time?
   - What countermeasures are needed?
   - How is trust maintained?

### When Uncertain

1. Ask clarifying questions about scope
2. Reference the Codex Manifesto for guidance
3. Check existing agent definitions for patterns
4. Suggest consulting relevant protocol documents
5. Propose human review for critical decisions

---

## Version Control & Git Conventions

### Ignored Files (see `.gitignore`)

The project maintains a comprehensive `.gitignore` covering:

- **Secrets:** `.env`, `.Renviron`, `.httr-oauth`
- **Python artifacts:** `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/`
- **Build outputs:** `build/`, `dist/`, `*.egg-info/`
- **IDE files:** `.vscode/`, `.idea/`, `*.swp`
- **OS files:** `.DS_Store`, `Thumbs.db`, `desktop.ini`
- **Logs and outputs:** `*.log`, `outputs/`, `logs/`

### Commit Message Guidelines

While not explicitly documented, follow these best practices:

- Use clear, descriptive commit messages
- Start with a verb (Add, Update, Fix, Remove, Rename)
- Reference agent names when relevant
- Mention protocol changes explicitly

**Examples:**
- "Add Pack Rat secure transfer validation"
- "Update Artemis governance review process"
- "Fix routing issue in codex_cli.py"
- "Rename Codex Daemon to CompSuite and update roles"

---

## Dependencies & Requirements

### Python Dependencies

Current dependencies (from `requirements.txt`):
- **PyYAML >= 6.0:** For YAML configuration parsing

### System Requirements

- **Python:** 3.13 or higher (as specified in pyproject.toml)
- **pip:** Python package installer (or uv)
- **Operating System:** Cross-platform (Linux, macOS, Windows)

### Optional Tools

- **Virtual environment:** `venv` or `virtualenv` (recommended)
- **Text editor/IDE:** Any Python-compatible editor

---

## Project Status & Roadmap

### Current State (Version 0.1.0)

**Completed:**
-  Agent architecture framework
-  Basic CLI with keyword routing and ATP integration
-  Core documentation (Manifesto, protocols, templates)
-  Trust Decay Model definition
-  Sandbox simulation environment
-  Initial agent definitions (Artemis, Copilot, Pack Rat, CompSuite)
-  Artemis agent Python implementation (persona, reflection, semantic tagging)
-  ATP (Artemis Transmission Protocol) parser and validator
-  Memory integration layer (MemoryClient, TrustInterface, ContextLoader)
-  Core instruction loading and caching system

**In Progress:**
-  Memory management implementation
-  Trust scoring system implementation
-  Expanded simulation scenarios
-  Memory layer integration with MCP servers

**Planned:**
- ⏳ Automated testing infrastructure
- ⏳ Contributing guidelines (`CONTRIBUTING.md`)
- ⏳ Advanced agent interactions
- ⏳ External API integrations
- ⏳ Enhanced security protocols

### Known Limitations

1. **No Automated Tests:** Test infrastructure needs implementation
2. **Simulated Routing:** CLI routing is keyword-based simulation, not full agent execution
3. **Manual Trust Management:** Trust Decay Model defined but not automated
4. **Limited Simulations:** Only mail delivery simulation currently implemented

---

## Quick Reference: Common Tasks

### Add a New Agent

```bash
1. cp agents/agent_template.md agents/new_agent.md
2. Edit agents/new_agent.md (fill all fields)
3. Update interface/agent_router.yaml (add keywords)
4. Test: python interface/codex_cli.py "command with keyword"
5. Update CLAUDE.md (this file) with agent details
```

### Modify Agent Routing

```bash
1. Edit interface/agent_router.yaml
2. Update keywords, roles, or action descriptions
3. Test routing: python interface/codex_cli.py
4. Verify all expected keywords route correctly
```

### Run All Simulations

```bash
# Currently only one simulation exists
python sandbox_city/networked_scripts/mail_delivery_sim.py
```

### Check System Dependencies

```bash
python --version  # Should be 3.8+
pip list          # Should show PyYAML>=6.0
```

---

## Additional Resources

### Key Concepts to Understand

1. **Agentic Reasoning:** Decision-making processes distributed across specialized agents
2. **Trust Decay:** Quantitative trust scoring that changes over time and with interactions
3. **Semantic Zones:** Conceptual areas within Sandbox City for testing
4. **Drift Countermeasures:** Mechanisms to prevent agent behavior deviation
5. **Energy Signatures:** Computational resource footprints of agents

### External References

- **MIT License:** https://opensource.org/licenses/MIT
- **PyYAML Documentation:** https://pyyaml.org/
- **Google Python Style Guide:** https://google.github.io/styleguide/pyguide.html

---

## Maintenance Notes

### For AI Assistants

**This file should be updated when:**
- New agents are added
- Agent definitions significantly change
- New protocols are introduced
- Major architectural changes occur
- Dependencies are added or updated
- Project version changes

**Keep this file:**
- Comprehensive but focused
- Clear and accessible
- Aligned with actual codebase state
- Updated with each major change

**Version History:**
- **1.0.0** (2025-11-14): Initial comprehensive CLAUDE.md created
- **1.1.0** (2025-11-23): Updated structure with new Python modules, demo scripts, and documentation files

---

**Last Updated:** 2025-11-23
**Document Version:** 1.1.0
**Codebase Version:** 0.1.0
**Maintained By:** AI Assistants & Project Contributors
