---
title: "Artemis City Whitepaper: Agentic Operating System Architecture"
date: "2025-10-28"
description: "An inaugural look at the vision and early steps of launching Artemis City, a beacon of future innovation."
author: "Prinston Palmer"
---
# Artemis City: Agentic Operating System Architecture

**A Kernel-Driven Approach to Multi-Agent Orchestration**


## Abstract

Current approaches to AI agent orchestration place decision-making authority in large language models (LLMs), resulting in non-deterministic behavior unsuitable for production environments. We present Artemis City, a kernel-driven operating system architecture that inverts this model: routing, state management, and governance are handled by a deterministic kernel, while LLMs serve as specialized compute resources. This paper describes the architecture, implementation, and design decisions behind Artemis City's approach to production-ready multi-agent systems.

---

## 1. Introduction

### 1.1 The Problem with LLM-Driven Orchestration

Existing agent frameworks (Auto-GPT, BabyAGI, LangChain) suffer from:

1. **Non-deterministic routing:** LLMs decide next actions, leading to unpredictable workflows
2. **Lack of governance:** No audit trails, permission systems, or accountability mechanisms
3. **Memory fragility:** Session-based memory without persistence or decay models
4. **Vendor lock-in:** Proprietary memory storage with no user ownership
5. **Production unsuitability:** Designed for demos, not enterprise deployment

### 1.2 The Artemis City Thesis

**Reliable multi-agent systems require a kernel layer that separates orchestration from intelligence.**

Just as Unix kernels manage process scheduling without processes deciding their own priorities, an agentic kernel must manage:

- Agent routing and execution
- State persistence and memory
- Tool permissions and audit
- Resource allocation
- Error handling and recovery

LLMs provide intelligence; the kernel provides governance.

---

## 2. Architecture Overview

### 2.1 System Components

```
┌──────────────────────────────────────────────────┐
│              Application Layer                    │
│         (Codex CLI, API, Integrations)           │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────┴─────────────────────────────────┐
│           Artemis City Kernel                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Router  │  │  State   │  │Governance│       │
│  │  Engine  │  │  Manager │  │  Layer   │       │
│  └──────────┘  └──────────┘  └──────────┘       │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────┴─────────────────────────────────┐
│              Agent Runtime Layer                  │
│   ┌────────┐  ┌────────┐  ┌────────┐           │
│   │ Coder  │  │Planner │  │Research│           │
│   │ Agent  │  │ Agent  │  │ Agent  │           │
│   └────────┘  └────────┘  └────────┘           │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────┴─────────────────────────────────┐
│          Memory & Integration Bus                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Obsidian │  │ Supabase │  │   MCP    │       │
│  │(Unstruc.)│  │(Struct.) │  │  Tools   │       │
│  └──────────┘  └──────────┘  └──────────┘       │
└──────────────────────────────────────────────────┘
```

### 2.2 Core Principles

1. **Kernel Decides:** Routing logic defined in YAML, executed deterministically
2. **Persistent State:** All agent interactions stored with trust-decay metadata
3. **User Ownership:** Memory lives in user-controlled Obsidian vaults + Supabase instances
4. **Tool Safety:** MCP protocol layer with permission system and audit logging
5. **Extensibility:** Plugin architecture for agents, tools, and memory backends

---

## 3. Kernel Design

### 3.1 Router Engine

The router engine uses pattern matching against a YAML configuration to deterministically route requests to agents.

**Configuration Format:**

```yaml
router_version: "1.0"

routes:
  - id: "code_execution"
    pattern: "build|create|code|implement|write.*code"
    agent: "coder"
    priority: 100
    requires_tools: ["filesystem", "shell"]
    
  - id: "architecture_planning"
    pattern: "plan|design|architect|structure"
    agent: "planner"
    priority: 100
    
  - id: "information_gathering"
    pattern: "research|find|search|investigate"
    agent: "researcher"
    priority: 80
    requires_tools: ["web_search", "documentation"]

fallback:
  agent: "planner"
  reason: "Default to planning for ambiguous requests"
```

**Routing Algorithm:**

1. Parse user request
2. Extract semantic intent (NLP preprocessing)
3. Match against patterns (regex + semantic similarity)
4. Select highest priority matching route
5. Validate tool permissions
6. Execute agent with kernel context

**Benefits:**

- Deterministic (same input → same routing)
- Auditable (log routing decisions)
- Testable (unit test routing config)
- Version-controlled (routing is code)

### 3.2 State Manager

The state manager maintains kernel state across executions.

**State File Format (kernel.json):**

```json
{
  "kernel_version": "1.0.0",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "active_agents": [
    {
      "agent_id": "coder_001",
      "status": "idle",
      "last_execution": "2025-12-05T14:30:00Z"
    }
  ],
  "memory_refs": [
    {
      "task_id": "task_001",
      "agent": "coder",
      "timestamp": "2025-12-05T14:23:15Z",
      "trust_score": 1.0
    }
  ],
  "governance_log": [
    {
      "event": "agent_execution",
      "agent": "coder",
      "tools_used": ["filesystem_write"],
      "outcome": "success",
      "timestamp": "2025-12-05T14:23:20Z"
    }
  ]
}
```

### 3.3 Governance Layer

The governance layer enforces policies and maintains audit trails.

**Capabilities:**

- Tool permission management (RBAC)
- Audit logging (all agent actions)
- Rate limiting (prevent runaway loops)
- Cost tracking (LLM API usage)
- Trust-decay (memory reliability over time)

---

## 4. Memory Architecture

### 4.1 Agentic Memory Bus

The memory bus integrates three storage layers:

**Unstructured Memory (Obsidian):**

- Long-form context
- User notes and documentation
- Agent output stored as markdown
- Graph-based linking

**Structured Memory (Supabase/Postgres):**

- Task metadata
- Agent execution history
- Metrics and telemetry
- Queryable via SQL

**Protocol Logs (ACP):**

- Agent communication records
- Tool call traces
- State transitions

### 4.2 Trust-Decay Model

Memory reliability decreases over time without validation:

```python
def trust_score(created_at, last_validated, validation_count):
    age_days = (now() - created_at).days
    recency_days = (now() - last_validated).days
    
    base_score = 1.0
    age_penalty = 0.01 * age_days  # 1% per day
    recency_penalty = 0.05 * recency_days  # 5% per day since validation
    validation_boost = 0.1 * validation_count  # 10% per validation
    
    return max(0.0, min(1.0, 
        base_score - age_penalty - recency_penalty + validation_boost
    ))
```

**Design Rationale:**

- Encourages re-validation of old assumptions
- Prevents stale data from influencing decisions
- Supports accountability ("why did agent X do Y?")

---

## 5. Agent Design

### 5.1 Agent Template Protocol (ATP)

Agents are defined via YAML specifications:

```yaml
name: coder
version: "1.0"
role: "Code generation and implementation"

model:
  provider: openai
  name: gpt-4
  temperature: 0.2
  max_tokens: 4000

system_prompt: |
  You are a senior software engineer focused on:
  - Writing clean, maintainable code
  - Following best practices and design patterns
  - Comprehensive error handling
  - Clear documentation

tools:
  - id: filesystem_read
    permission: required
  - id: filesystem_write
    permission: required
  - id: shell_execute
    permission: optional
    requires_approval: true

memory:
  read_access: ["code_context", "architecture_docs"]
  write_access: ["code_output", "implementation_notes"]

constraints:
  max_execution_time: 300  # seconds
  max_file_size: 1048576    # 1MB
  allowed_file_types: [".py", ".js", ".yaml", ".json"]
```

### 5.2 Agent Lifecycle

1. **Initialization:** Load config, validate tools, establish memory connection
2. **Execution:** Receive task from kernel, execute with tool access
3. **Memory Write:** Store output to memory bus with metadata
4. **State Update:** Report completion to kernel state manager
5. **Governance Log:** Record all actions for audit

---

## 6. MCP Integration

### 6.1 Model Context Protocol

MCP provides a standardized interface for tools and services.

**Tool Registration:**

```python
from artemis_city.mcp import Tool, ToolRegistry

class FilesystemTool(Tool):
    name = "filesystem"
    description = "Read and write files"
    
    def read(self, path: str) -> str:
        # Implementation with safety checks
        pass
    
    def write(self, path: str, content: str) -> bool:
        # Implementation with permission validation
        pass

# Register with kernel
registry = ToolRegistry()
registry.register(FilesystemTool())
```

### 6.2 Tool Permissions

Tools require explicit permissions granted by the kernel:

```yaml
tool_permissions:
  coder:
    - filesystem_read
    - filesystem_write
    - shell_execute
  
  researcher:
    - web_search
    - documentation_access
  
  planner:
    - filesystem_read  # Read-only access
```

---

## 7. Comparison to Existing Frameworks

|**Feature**|**Auto-GPT**|**LangChain**|**BabyAGI**|**Artemis City**|
|---|---|---|---|---|
|**Routing**|LLM-decided|LLM-decided|LLM-decided|**Kernel YAML**|
|**Memory**|Session-only|Vendor-specific|Task list|**User-owned (Obsidian + Supabase)**|
|**Governance**|None|Basic|None|**RBAC + Audit + Trust-decay**|
|**Multi-Agent**|No|Chains only|No|**Native orchestration**|
|**Production-Ready**|Demo|Partial|Demo|**Yes**|

---

## 8. Use Cases

### 8.1 Software Development Workflow

```
User: "Build a REST API for a todo app with authentication"
  ↓
Kernel routes to Planner
  ↓
Planner creates architecture (auth, CRUD, database schema)
  ↓
Kernel routes implementation to Coder
  ↓
Coder implements endpoints, writes tests
  ↓
Kernel stores in memory with linked context
```

### 8.2 Research & Documentation

```
User: "Research best practices for API rate limiting"
  ↓
Kernel routes to Researcher
  ↓
Researcher gathers information from docs/web
  ↓
Kernel routes synthesis to Planner
  ↓
Planner creates structured recommendations
  ↓
Stored in Obsidian vault for future reference
```

---

## 9. Future Work

### 9.1 Conditional Routing

Support for conditional logic in routing:

```yaml
routes:
  - pattern: "deploy"
    conditions:
      - memory_exists: "deployment_config"
      - tests_passing: true
    agent: "deployer"
    fallback: "planner"  # If conditions not met
```

### 9.2 Parallel Agent Execution

Kernel orchestrates multiple agents in parallel:

```yaml
parallel_routes:
  - agents: ["researcher", "coder"]
    coordination: "merge_results"
    timeout: 300
```

### 9.3 Federation

Multiple Artemis City instances coordinating:

```
Local Kernel ←→ Remote Kernel (specialized agents)
```

---

## 10. Conclusion

Artemis City demonstrates that production-ready multi-agent systems require kernel-level orchestration. By separating routing, governance, and memory from LLM intelligence, we achieve:

- **Determinism:** Same input → same routing
- **Auditability:** Complete governance logs
- **User ownership:** Memory lives in user-controlled systems
- **Production readiness:** Enterprise-grade reliability

The kernel-driven approach inverts the LLM-centric model, positioning AI agents as specialized compute resources within a governed operating system.

**Artemis City is the kernel for the agentic era.**

---

## References

1. Auto-GPT: [github.com/Significant-Gravitas/Auto-GPT](http://github.com/Significant-Gravitas/Auto-GPT)
2. BabyAGI: [github.com/yoheinakajima/babyagi](http://github.com/yoheinakajima/babyagi)
3. LangChain: [github.com/langchain-ai/langchain](http://github.com/langchain-ai/langchain)
4. Model Context Protocol: [modelcontextprotocol.io](http://modelcontextprotocol.io)
5. Obsidian: [obsidian.md](http://obsidian.md)
6. Supabase: [supabase.com](http://supabase.com)

---

## Appendix A: Installation & Quick Start

```bash
pip install artemis-city
codex init my-agent-system
codex run coder "Hello world"
```

**Full documentation:** [artemis-city.dev/docs](http://artemis-city.dev/docs)

---

_© 2025 Artemis City | MIT License | [github.com/popvilla/Artemis-City](http://github.com/popvilla/Artemis-City)_