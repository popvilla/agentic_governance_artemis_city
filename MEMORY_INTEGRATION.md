``` # Memory Layer Integration

This document describes the integration between **Artemis City** core and the **Artemis Agentic Memory Layer** (MCP Server), enabling agents to interact with Obsidian vault as a persistent knowledge base.

## Overview

The memory integration bridge connects the Python-based Artemis City agent system with the Node.js MCP server, allowing:

- **Persistent Context Storage**: Agents can store and retrieve context across sessions
- **Trust-Based Access Control**: Memory operations filtered by agent trust scores  
- **Structured Knowledge Base**: Obsidian vault acts as versioned source of truth
- **Agent-Vault Interaction**: Search, tag, and organize knowledge programmatically

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                       Artemis City Core                        │
│  ┌──────────────┐   ┌─────────────────┐   ┌────────────────┐ │
│  │  Agents      │   │  ATP Protocol   │   │  Instructions  │ │
│  │  (Artemis,   │◄──┤  (Structured    │◄──┤  (Hierarchy)   │ │
│  │   Pack Rat)  │   │   Messages)     │   │                │ │
│  └──────┬───────┘   └─────────────────┘   └────────────────┘ │
│         │                                                      │
│         ▼                                                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │           Memory Integration Bridge                      │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │ │
│  │  │ Memory       │  │ Trust        │  │ Context      │  │ │
│  │  │ Client       │◄─┤ Interface    │──► Loader       │  │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │ │
│  └──────────────────┬───────────────────────────────────────┘ │
└─────────────────────┼───────────────────────────────────────┘
                      │ REST API (Bearer Token)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Artemis Agentic Memory Layer (MCP Server)          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │  Express │──►│ Auth     │──►│ Router   │──►│ Tools    │   │
│  │  Server  │   │ Middleware│   │ (8 ops)  │   │ Layer    │   │
│  └──────────┘   └──────────┘   └──────────┘   └────┬─────┘   │
│                                                      ▼          │
│                                            ┌─────────────────┐ │
│                                            │ Obsidian REST   │ │
│                                            │ API Service     │ │
│                                            └────────┬────────┘ │
└─────────────────────────────────────────────────────┼─────────┘
                                                      │
                                                      ▼
                                            ┌─────────────────┐
                                            │   Obsidian      │
                                            │   Vault         │
                                            │  (Knowledge)    │
                                            └─────────────────┘
```

## Components

### 1. Memory Client (`memory/integration/memory_client.py`)

Python REST client for the MCP server with full coverage of 8 MCP operations.

**Features:**
- Bearer token authentication
- Standardized response format (MCPResponse)
- Automatic error handling
- Built-in HTTP client (no external dependencies)

**Operations:**
- `get_context(path)` - Read note content
- `append_context(path, content)` - Append to note
- `update_note(path, content)` - Replace note content
- `search_notes(query)` - Search vault
- `list_notes(folder)` - List notes in folder
- `delete_note(path)` - Delete note
- `manage_frontmatter(path, action, key, value)` - YAML frontmatter ops
- `manage_tags(path, action, tags)` - Tag management
- `search_replace(path, search, replace)` - Find and replace

**Example:**
```python
from memory.integration import MemoryClient

client = MemoryClient(
    base_url="http://localhost:3000",
    api_key="your_mcp_api_key"
)

# Read a note
response = client.get_context("Daily/2025-11-23.md")
if response.success:
    print(response.data['content'])

# Store agent context
client.store_agent_context(
    "artemis",
    "Completed ATP integration successfully"
)
```

### 2. Trust Interface (`memory/integration/trust_interface.py`)

Trust-based access control for memory operations with decay model.

**Features:**
- Trust scores for agents (0.0-1.0)
- Trust levels (FULL, HIGH, MEDIUM, LOW, UNTRUSTED)
- Operation permission matrix
- Natural trust decay over time
- Reinforcement/penalty system

**Trust Levels & Permissions:**

| Level       | Score Range | Allowed Operations                           |
|-------------|-------------|----------------------------------------------|
| FULL        | 0.9-1.0     | read, write, delete, search, tag, update     |
| HIGH        | 0.7-0.9     | read, write, search, tag, update             |
| MEDIUM      | 0.5-0.7     | read, write, search, tag                     |
| LOW         | 0.3-0.5     | read, search                                 |
| UNTRUSTED   | 0.0-0.3     | none                                         |

**Example:**
```python
from memory.integration import get_trust_interface

trust = get_trust_interface()

# Check permission
if trust.can_perform_operation('artemis', 'write'):
    # Perform write operation
    trust.record_success('artemis')  # Reinforce trust
else:
    print("Access denied - insufficient trust")

# Get trust report
report = trust.get_trust_report()
print(f"Total entities: {report['total_entities']}")
```

### 3. Context Loader (`memory/integration/context_loader.py`)

High-level interface for loading and organizing context from vault.

**Features:**
- Load notes as ContextEntry objects
- Search vault with relevance scoring
- Load by tags or folders
- Agent history tracking
- Related content discovery
- Date range filtering

**Example:**
```python
from memory.integration import ContextLoader

loader = ContextLoader()

# Search vault
entries = loader.search_context("ATP protocol", limit=5)
for entry in entries:
    print(f"{entry.path}: {entry.get_summary()}")

# Load agent history
history = loader.load_agent_history("artemis", limit=10)
summary = loader.get_context_summary(history)
print(summary)

# Find related notes
related = loader.get_related_context("Agents/artemis.md")
```

## Setup & Configuration

### Prerequisites

1. **Obsidian** with Local REST API plugin installed and enabled
2. **MCP Server** (Artemis Agentic Memory Layer) running
3. **Environment variables** configured

### Environment Variables

Add to your `.env` file or export:

```bash
# MCP Server configuration
export MCP_BASE_URL="http://localhost:3000"
export MCP_API_KEY="your_super_secret_mcp_key_123"

# Optional: Override Obsidian connection
export OBSIDIAN_BASE_URL="https://localhost:27124"
export OBSIDIAN_API_KEY="your_obsidian_plugin_api_key"
```

### Starting the MCP Server

```bash
# Navigate to memory layer
cd "Artemis Agentic Memory Layer"

# Install dependencies (first time)
npm install

# Start in development mode
npm run dev

# Or build and run in production
npm run build
npm start
```

The server will start on `http://localhost:3000` (or configured PORT).

### Verifying Connection

```bash
# Health check
curl http://localhost:3000/health

# Test with authentication
curl -X POST http://localhost:3000/api/getContext \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_mcp_api_key" \
  -d '{"path": "test.md"}'
```

## Usage Patterns

### Pattern 1: Agent Storing Reflections

```python
from memory.integration import MemoryClient, get_trust_interface

trust = get_trust_interface()
client = MemoryClient()

agent_name = "artemis"

# Check permission
if trust.can_perform_operation(agent_name, 'write'):
    # Store reflection
    reflection = "Today's synthesis: ATP integration complete"
    response = client.store_agent_context(agent_name, reflection)
    
    if response.success:
        trust.record_success(agent_name)
    else:
        trust.record_failure(agent_name)
```

### Pattern 2: Loading Historical Context

```python
from memory.integration import ContextLoader

loader = ContextLoader()

# Load agent's recent context
history = loader.load_agent_history("artemis", limit=5)

# Filter by date range
recent = loader.filter_by_date_range(
    history,
    start_date="2025-11-01",
    end_date="2025-11-30"
)

# Generate summary
summary = loader.get_context_summary(recent)
print(summary)
```

### Pattern 3: Cross-Agent Knowledge Sharing

```python
from memory.integration import MemoryClient, ContextLoader

client = MemoryClient()
loader = ContextLoader()

# Pack Rat stores transfer log
client.store_agent_context(
    "pack_rat",
    "Transfer completed: ATP specs to Artemis",
    folder="Agents/Transfers"
)

# Artemis loads Pack Rat's logs
pack_rat_logs = loader.load_tagged_context("pack_rat", limit=10)

# Artemis references them in reflection
for log in pack_rat_logs:
    print(f"Pack Rat activity: {log.get_summary()}")
```

### Pattern 4: Trust-Filtered Context

```python
from memory.integration import get_trust_interface, ContextLoader

trust = get_trust_interface()
loader = ContextLoader()

# Load all agent histories
all_history = []
for agent in ['artemis', 'pack_rat', 'copilot']:
    history = loader.load_agent_history(agent, limit=5)
    for entry in history:
        all_history.append({
            'entity_id': agent,
            'entity_type': 'agent',
            'data': entry
        })

# Filter by trust level
trusted_only = trust.filter_by_trust(all_history, min_trust_level=TrustLevel.HIGH)

print(f"Filtered from {len(all_history)} to {len(trusted_only)} trusted entries")
```

## Integration with Existing Components

### With ATP Protocol

ATP messages can include memory references:

```python
from agents.atp import ATPParser
from memory.integration import ContextLoader

parser = ATPParser()
loader = ContextLoader()

# Parse ATP command
message = parser.parse("""
#Mode: Synthesize
#Context: Weekly reflection
#ActionType: Reflect
#TargetZone: Reflections/Weekly

Load this week's context and synthesize
""")

# Load context from target zone
entries = loader.load_folder_context("Reflections/Weekly")

# Process with message context
print(f"Synthesizing {len(entries)} entries for {message.context}")
```

### With Artemis Persona

Artemis can store and load context for continuity:

```python
from agents.artemis import ArtemisPersona, ReflectionEngine
from memory.integration import MemoryClient, ContextLoader

persona = ArtemisPersona()
client = MemoryClient()
loader = ContextLoader()

# Load historical context
history = loader.load_agent_history("artemis", limit=20)

# Feed to reflection engine
engine = ReflectionEngine()
for entry in history:
    engine.add_conversation(entry.content)

# Generate synthesis
synthesis = engine.synthesize()

# Store synthesis back to vault
client.store_agent_context("artemis", synthesis, "Reflections")
```

### With Instruction Hierarchy

Memory can provide agent-specific instructions:

```python
from core.instructions import InstructionLoader
from memory.integration import ContextLoader

loader = ContextLoader()

# Load agent instructions from vault
agent_instructions = loader.load_note("Agents/artemis/instructions.md")

if agent_instructions:
    # Instructions loaded from Obsidian override local
    print("Using vault-stored instructions:")
    print(agent_instructions.content)
```

## Running the Demo

A comprehensive demonstration script showcases all features:

```bash
# Set environment variables first
export MCP_BASE_URL=http://localhost:3000
export MCP_API_KEY=your_mcp_api_key

# Make executable
chmod +x demo_memory_integration.py

# Run demo
python demo_memory_integration.py
```

The demo covers:
1. Memory client connection and health check
2. Trust interface and permission matrix
3. Context loading from Obsidian vault
4. Integrated agent-memory workflow
5. Trust decay model simulation

## Error Handling

All memory operations return standardized `MCPResponse` objects:

```python
response = client.get_context("Some/Note.md")

if response.success:
    # Operation succeeded
    data = response.data
    print(response.message)
else:
    # Operation failed
    print(f"Error: {response.error}")
    print(f"Status: {response.status_code}")
```

Common error scenarios:
- `status_code: 0` - Connection failed (MCP server not running)
- `status_code: 401` - Authentication failed (invalid API key)
- `status_code: 404` - Note not found
- `status_code: 500` - Server error

## Trust Decay Model

Trust scores naturally decay over time without reinforcement:

```python
trust = get_trust_interface()
score = trust.get_trust_score("agent_name")

# Decay formula: score * (1 - decay_rate)^days_elapsed
# Default decay rate: 1% per day

# Reinforcement (successful operations)
trust.record_success("agent_name", amount=0.02)  # +2%

# Penalty (failed operations)
trust.record_failure("agent_name", amount=0.05)  # -5%

# Minimum scores by level prevent complete decay
# FULL: 0.9, HIGH: 0.7, MEDIUM: 0.5, LOW: 0.3
```

## Security Considerations

1. **API Keys**: Never commit `.env` files or expose API keys
2. **Bearer Tokens**: MCP server validates all requests
3. **Trust Filtering**: Access control layer prevents unauthorized ops
4. **HTTPS**: Use HTTPS in production for encrypted transport
5. **Audit Logging**: All operations logged by MCP server

## Performance

- **Caching**: MemoryClient uses connection pooling
- **Batch Operations**: Load multiple notes in single call when possible
- **Trust Lookups**: O(1) dictionary lookups with decay calculation
- **Context Search**: Leverages Obsidian's search indexing

## Troubleshooting

### Connection Refused

**Problem**: `Connection error: Connection refused`

**Solution**:
1. Check MCP server is running: `curl http://localhost:3000/health`
2. Verify `MCP_BASE_URL` environment variable
3. Check firewall isn't blocking port 3000

### Authentication Failed (401)

**Problem**: `HTTP 401: Unauthorized`

**Solution**:
1. Verify `MCP_API_KEY` matches server configuration
2. Check `.env` file in MCP server directory
3. Restart MCP server after changing API key

### Obsidian Connection Failed

**Problem**: MCP server can't reach Obsidian

**Solution**:
1. Ensure Obsidian is running
2. Verify Local REST API plugin is enabled
3. Check `OBSIDIAN_BASE_URL` in MCP `.env`
4. For Docker: Use `host.docker.internal` on Mac/Windows

### Trust Denials

**Problem**: Operations blocked by trust interface

**Solution**:
1. Check agent trust score: `trust.get_trust_score(agent_name)`
2. Verify operation is allowed for trust level
3. Record successful operations to build trust
4. Manually adjust trust if needed (development only)

## Future Enhancements

Planned improvements aligned with the plan:

1. **Enhanced CLI Integration**
   - Automatic context loading on startup
   - Persistent conversation history
   - Cross-session memory

2. **MCP Configuration Helper**
   - Auto-discovery of MCP server
   - Configuration validation
   - Health monitoring

3. **Agent Communication**
   - Message protocol with context hashing
   - Shared workspace in vault
   - Cross-agent knowledge graphs

4. **Advanced Search**
   - Semantic search with embeddings
   - Relevance ranking algorithms
   - Context-aware suggestions

## References

- **MCP Server Documentation**: See `Artemis Agentic Memory Layer/README.md`
- **ATP Protocol**: See `agents/artemis_transmission_protocol (ATP)`
- **Trust Decay Model**: See `memory/trust_decay_model.md`
- **Agent Cards**: See `agents/*.md`

---

**Version**: 1.0.0  
**Author**: Prinston Palmer  
**Last Updated**: November 23, 2025  
**Status**: Production Ready
```