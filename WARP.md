# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Artemis City** is an architectural framework for agentic reasoning with transparent, accountable action across distributed intelligence systems. This is **Version Zero** (v0.1.0), providing foundational scaffolding for defining agents, managing memory with trust decay, establishing secure communication, and simulating agent interactions.

The project consists of two major components:
1. **Artemis City Core**: Python-based agent system with CLI interface
2. **Artemis Agentic Memory Layer**: TypeScript/Node.js REST API server for Obsidian vault integration

## Essential Commands

### Artemis City Core (Python)

```bash
# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run CLI interactively
python interface/codex_cli.py

# Run CLI with single command
python interface/codex_cli.py "ask artemis about system status"

# Run mail delivery simulation
python sandbox_city/networked_scripts/mail_delivery_sim.py

# Start with npm (convenience wrapper)
npm start
```

### Artemis Agentic Memory Layer (Node.js)

**Note:** Directory name includes trailing space: `"Artemis Agentic Memory Layer "`

```bash
# Navigate to memory layer
cd "Artemis Agentic Memory Layer "

# Install dependencies
npm install

# Development mode (hot-reload)
npm run dev

# Production build and run
npm run build
npm start

# Linting
npm run lint

# Docker deployment
docker-compose up --build
```

## Architecture Overview

### Core Python System

**Component Flow:**
```
User Input → CLI (codex_cli.py)
         ↓
   Agent Router (agent_router.yaml)
         ↓
   Agent Modules (agents/*.md definitions)
         ↓
   Memory/Trust Systems
         ↓
   Sandbox Simulations (testing)
```

**Key Components:**

1. **CLI Interface** (`interface/codex_cli.py`)
   - Entry point for all user interactions
   - Keyword-based routing via YAML config
   - Interactive REPL and single-command modes

2. **Agent Router** (`interface/agent_router.yaml`)
   - Maps keywords to agent handlers
   - Defines semantic roles and actions
   - Currently routes to: artemis, pack_rat, codex_daemon, copilot

3. **Agent System** (`agents/`)
   - All agents follow standardized template with required fields:
     - System Access Scope (permissions/boundaries)
     - Semantic Role (primary function)
     - Energy Signature (computational footprint)
     - Linked Protocols (communication standards)
     - Drift Countermeasures (behavioral safeguards)
     - Trust Threshold Triggers (security conditions)
   
4. **Core Agents:**
   - **Artemis**: Governance, policy enforcement, dispute resolution
   - **Pack Rat**: Secure data transfer between agents
   - **CompSuite** (formerly Codex Daemon): System monitoring, memory interface
   - **Copilot**: Real-time contextual assistance

5. **Memory Management** (`memory/`)
   - **Trust Decay Model**: Dynamic trust scoring with decay/reinforcement
   - **Memory Lawyer**: Memory validation protocols
   - Applies to agents, memories, and protocols

6. **Sandbox City** (`sandbox_city/`)
   - Isolated simulation environment for testing agent interactions
   - Network scripts for secure transfer simulations
   - Semantic zones for compartmentalized testing

### Artemis Agentic Memory Layer (Node.js)

**Layered Architecture:**
```
Client → Express → Auth Middleware → Router
                         ↓
                     Tool Layer (8 operations)
                         ↓
                 Obsidian REST API Service
                         ↓
                  Obsidian Vault (knowledge store)
```

**Key Features:**
- REST API for programmatic Obsidian vault access
- Bearer token authentication (MCP_API_KEY)
- 8 core operations: getContext, appendContext, updateNote, searchNotes, listNotes, deleteNote, manageFrontmatter, manageTags, searchReplace
- Standardized response format: `{ success, data?, message?, error? }`
- Comprehensive logging at all layers (DEBUG/INFO/WARN/ERROR)

**Configuration:**
- Environment variables in `.env` file (PORT, MCP_API_KEY, OBSIDIAN_BASE_URL, OBSIDIAN_API_KEY, MCP_LOG_LEVEL)
- Requires Obsidian Local REST API plugin running
- Docker networking: Use `host.docker.internal:27124` on Mac/Windows

## Key Protocols & Patterns

### Artemis Transmission Protocol (ATP)

Structured communication system using signal tags:
- `#Mode:` - Intent (Build, Review, Organize, Capture, Synthesize, Commit)
- `#Context:` - Mission goal/purpose
- `#Priority:` - Urgency (Critical, High, Normal, Low)
- `#ActionType:` - Expected response (Summarize, Scaffold, Execute, Reflect)
- `#TargetZone:` - Project/folder area
- `#SpecialNotes:` - Special instructions/warnings

### Trust Decay Model

Quantitative trust management with:
- Initial trust scores for agents/memories/protocols
- Natural decay over time without reinforcement
- Reinforcement from successful actions
- Penalties for failures/violations
- Threshold-based triggers for re-evaluation

### Translator Protocol

Ensures consistent communication:
- UTF-8 standard encoding
- Language detection and transliteration
- Automated error reporting
- Human review loop for ambiguous cases

## Development Guidelines

### Python Code Conventions

1. **Documentation:**
   - Google-style docstrings for all functions
   - Include Args, Returns, and Raises sections
   - Module-level documentation at top of file

2. **Error Handling:**
   - Fail gracefully with informative messages
   - Return sensible defaults when appropriate
   - Log errors for debugging

3. **Configuration:**
   - YAML for agent/router configuration
   - Validate configuration on load
   - Keep config separate from code logic

### TypeScript/Node.js Conventions (Memory Layer)

1. **Documentation:**
   - JSDoc comments for all public functions
   - Document parameters, returns, and examples
   - Module-level overview comments

2. **Architecture Patterns:**
   - Layered architecture with clear separation
   - Middleware for cross-cutting concerns
   - Standardized response format across all endpoints

3. **Logging:**
   - Use centralized logger utility
   - Appropriate log levels (DEBUG/INFO/WARN/ERROR)
   - Request/response logging via middleware

## Agent Development

### Creating New Agents

1. Copy `agents/agent_template.md`
2. Fill all required fields (see template for details)
3. Add agent to `interface/agent_router.yaml` with keywords
4. Define routing logic keywords
5. Document drift countermeasures and trust thresholds

### Agent Testing

- Use Sandbox City for isolated simulation
- Test keyword routing via CLI
- Verify trust decay triggers
- Validate protocol adherence
- Check access scope boundaries

## Important Notes

- **Python Version**: Requires Python 3.8+ (3.13+ in pyproject.toml)
- **Node Version**: Requires Node.js 18+ for memory layer
- **No Automated Tests**: Currently manual testing only (both package.json show "no test specified")
- **License**: MIT for both components
- **Memory Layer Directory**: Name includes trailing space - use quotes in commands
- **Security**: Never commit `.env` files (API keys, secrets)
- **Philosophy**: Follow Codex Manifesto principles - iterative clarity, net good over noise, transparent accountability, collaborative autonomy, resilience through entropy management

## Core Philosophy (Codex Manifesto)

1. **Iterative Clarity, Not Static Truth** - Living document, continuous improvement
2. **Net Good Over Noise** - Prioritize meaningful contributions, filter through ethical boundaries
3. **Transparent Accountability** - Auditable actions, traceable decision-making
4. **Collaborative Autonomy** - Defined autonomy within collaborative framework
5. **Resilience through Entropy Management** - Proactive countermeasures against system decay

## File Organization

- **agents/**: Agent definitions (markdown specs)
- **codex/**: Core principles and manifesto
- **interface/**: CLI and router configuration
- **launch/**: Governance and release management
- **memory/**: Trust and validation frameworks
- **sandbox_city/**: Simulation environment
- **Artemis Agentic Memory Layer/**: Node.js REST API server for Obsidian integration

## Integration Points

The Memory Layer serves as the knowledge bus between agents and persistent storage:
- Agents query/update Obsidian vault via REST API
- All operations authenticated with MCP_API_KEY
- Trust scores can influence memory read/write permissions
- Enables multi-agent workflows with shared versioned knowledge base
