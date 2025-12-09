# Hebbian Learning in Artemis City MCP

## Overview

The MCP system now includes a **Hebbian learning layer** that tracks connection strengths between agents and tasks. This implements the principle *"cells that fire together wire together"* to give the system the ability to learn from its own behavior.

## What It Does

Every time an agent executes a task, the system:
- **Strengthens** the connection (weight +1) if the task succeeds
- **Weakens** the connection (weight -1) if the task fails
- Tracks activation counts, success/failure rates, and timestamps

Over time, this creates a weighted graph that shows:
- Which agents are most reliable
- Which types of tasks each agent excels at
- Patterns in workflow execution
- Potential candidates for pruning (low-performing agents)

## How It Works

### Database Storage

Hebbian weights are stored in a local SQLite database at `data/hebbian_weights.db`.

Schema:
```sql
CREATE TABLE node_connections (
    id INTEGER PRIMARY KEY,
    origin_node TEXT,      -- Agent name (e.g., "Artemis Agent")
    target_node TEXT,      -- Task ID (e.g., "task_T123")
    weight REAL,           -- Connection strength
    activation_count INT,  -- Total times this connection activated
    success_count INT,     -- Successful activations
    failure_count INT,     -- Failed activations
    last_updated TEXT,     -- Timestamp
    created_at TEXT        -- Creation timestamp
)
```

### Update Rule

**Simple w = +1 / w = -1 model:**
```python
# On success:
ΔW = +1

# On failure:
ΔW = -1 (minimum weight = 0)
```

### Automatic Tracking

The orchestrator automatically updates weights after every task execution:

```python
# In orchestrator.py
def assign_and_execute_task(self, agent_name, task_context, ...):
    # Execute task
    results = agent.perform_task(task_context)

    # Update Hebbian weights
    if success:
        self.hebbian.strengthen_connection(agent_name, task_id)
    else:
        self.hebbian.weaken_connection(agent_name, task_id)
```

## CLI Usage

### Run Tasks (Weights Update Automatically)

```bash
# Run a single task
python main.py --instruction "Research AI ethics" --agent research_agent --title "Ethics Research"

# Hebbian weights are automatically updated after task completion
```

### View Network Summary

```bash
python main.py --show-hebbian
```

Output:
```
============================================================
🧠 HEBBIAN LEARNING NETWORK SUMMARY
============================================================
Total Connections: 3
Average Weight: 1.00
Max Weight: 1.00
Total Activations: 3
Success Rate: 100.00%
============================================================
```

### View Agent-Specific Stats

```bash
python main.py --agent-stats Artemis Agent
```

Output:
```
============================================================
🧠 HEBBIAN STATS FOR: Artemis Agent
============================================================
Average Weight: 1.00
Success Rate: 100.00%

Strongest Connections:
  1. user_instruction_20251207205022 (weight: 1.0)
============================================================
```

## Programmatic Access

You can access Hebbian data from Python code:

```python
from src.mcp.orchestrator import Orchestrator

orchestrator = Orchestrator()

# Get network summary
summary = orchestrator.hebbian.get_network_summary()
print(f"Total connections: {summary['total_connections']}")
print(f"Success rate: {summary['success_rate']:.2%}")

# Get agent performance
avg_weight = orchestrator.hebbian.get_agent_average_weight("Artemis Agent")
success_rate = orchestrator.hebbian.get_agent_success_rate("Artemis Agent")

# Get strongest connections for an agent
connections = orchestrator.hebbian.get_strongest_connections("Artemis Agent", limit=10)
for target, weight in connections:
    print(f"{target}: {weight}")

# Prune weak connections
pruned = orchestrator.hebbian.prune_weak_connections(threshold=0.5)
print(f"Pruned {pruned} weak connections")
```

## Future Enhancements

### 1. Weight-Based Routing
Use Hebbian weights to automatically select the best agent for a task:

```python
def select_best_agent_for_task(self, task_type):
    candidates = self.get_agents_for_task_type(task_type)

    # Score by historical performance
    best_agent = max(candidates, key=lambda a:
        self.hebbian.get_agent_average_weight(a)
    )

    return best_agent
```

### 2. Governance Kill-Switch
Block poorly performing agents:

```python
WEIGHT_THRESHOLD = 5.0

for agent_name in orchestrator.agents:
    avg_weight = orchestrator.hebbian.get_agent_average_weight(agent_name)

    if avg_weight < WEIGHT_THRESHOLD:
        orchestrator.blocklist_agent(agent_name)
        logger.warning(f"Agent {agent_name} blocked due to low Hebbian score")
```

### 3. Advanced Update Rules

**Tanh activation:**
```python
ΔW = tanh(learning_rate * activation_product)
```

**Time decay:**
```python
# Connections weaken over time if not reinforced
weight = weight * decay_factor ** days_since_last_activation
```

### 4. Vector Space Embeddings
Convert the Hebbian graph into a vector space for semantic routing:

```python
def get_agent_embedding(agent_name):
    """Get agent as vector of connection weights"""
    connections = hebbian.get_all_connections_for_agent(agent_name)
    return np.array([c['weight'] for c in connections])

# Compute similarity between agents
similarity = cosine_similarity(
    get_agent_embedding("Artemis Agent"),
    get_agent_embedding("research_agent")
)
```

### 5. Pattern Detection
Identify emergent workflows:

```python
# Find task sequences that frequently occur together
common_patterns = hebbian.find_sequential_patterns(min_frequency=5)

# Example output:
# [("research_agent", "summarizer_agent"),
#  ("Artemis Agent", "research_agent")]
```

## Architecture Integration

The Hebbian learning layer sits between the orchestrator and agents:

```
User Input
    ↓
Orchestrator (with Hebbian tracking)
    ↓
Agent Execution
    ↓
Results + Weight Update
    ↓
Obsidian Memory + SQLite Weights
```

### Layer Progression

From the planning documents, Artemis City now has:

1. ✅ **Morphology Layer** - Obsidian graph, nodes, connections
2. ✅ **Activation Layer** - Agents executing, tasks flowing
3. ✅ **Hebbian Weighting Layer** - Connection strengthening/weakening (NEW!)
4. ⏳ **Learning Layer** - Weight-based routing and agent selection (NEXT)
5. ⏳ **Cognitive Layer** - Emergent reasoning and self-optimization (FUTURE)

## Database Location

The Hebbian weights database is stored at:
```
<project_root>/data/hebbian_weights.db
```

This file is:
- Created automatically on first run
- Persists between runs
- Can be deleted to reset all weights
- Portable (can be backed up/shared)

## Logs

Hebbian weight updates are logged with the 🧠 emoji:

```
2025-12-07 20:50:22,335 - MCP_System - INFO - 🧠 Hebbian: Artemis Agent → user_instruction_20251207205022 strengthened (weight: 1.0)
```

## Philosophy

This implementation follows the planning documents' vision:

> "The structure is built; it didn't have a brain in terms of how do I interpret my movement and what is the value of it."

The Hebbian layer gives Artemis City the ability to:
- **Interpret** its own behavior
- **Value** different pathways
- **Learn** from experience
- **Evolve** through reinforcement
- **Prune** ineffective patterns

This is **proto-cognition** - the system learning to understand itself.

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `python main.py --show-hebbian` | Show network summary |
| `python main.py --agent-stats <name>` | Show agent statistics |
| `python main.py --instruction "..." --agent <name>` | Run task (auto-updates weights) |

## No External Dependencies Required

The Hebbian learning system uses:
- ✅ SQLite (built into Python)
- ✅ No Supabase required
- ✅ No external services
- ✅ Works with existing `python main.py` workflow

Everything is self-contained and ready to use!
