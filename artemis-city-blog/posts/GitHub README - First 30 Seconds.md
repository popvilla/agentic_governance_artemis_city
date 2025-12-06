---
title: "GitHub README - First 30 Seconds"
date: "2024-04-15"
description: "Crafting a README that immediately differentiates Artemis City from Auto-GPT clones and drives users to the quick-start guide."
---
**Goal:** Differentiate from Auto-GPT clones in first 30 seconds, drive to quick-start

**Critical Success:** Visitor immediately understands "kernel-driven vs LLM-driven"

---

```markdown
# 🏛️ Artemis City

**The Kernel for AI Agents**

> Deterministic, kernel-driven orchestration for multi-agent systems.
> Not another LLM wrapper—a governance layer that makes agents production-ready.

[![GitHub Stars]([<https://img.shields.io/github/stars/popvilla/Artemis-City?style=social>)](<https://github.com/popvilla/Artemis-City>)](<https://img.shields.io/github/stars/popvilla/Artemis-City?style=social>)](<https://github.com/popvilla/Artemis-City>))
[![Discord]([<https://img.shields.io/discord/XXXXX?color=7289da&label=Discord&logo=discord>)](<https://discord.gg/artemis-city>)](<https://img.shields.io/discord/XXXXX?color=7289da&label=Discord&logo=discord>)](<https://discord.gg/artemis-city>))
[![License]([<https://img.shields.io/badge/license-MIT-blue.svg>)](LICENSE)](<https://img.shields.io/badge/license-MIT-blue.svg>)](LICENSE))

---

## 🎯 What Makes Artemis City Different

| **Other Frameworks** | **Artemis City** |
|---------------------|------------------|
| LLM decides next action | **Kernel decides** via YAML routing |
| No memory between runs | **Persistent state** + trust-decay model |
| Vendor lock-in | **User-owned memory** (Supabase + Obsidian) |
| Single-agent demos | **Multi-agent orchestration** |
| Hope for reliability | **Governance primitives** (audit, permissions) |

**If you're building production multi-agent systems, you need a kernel, not hope.**

---

## ⚡ Quick Start (5 minutes)

```

# Install Artemis City

pip install artemis-city

# Initialize your first agent system

codex init my-agent-system

cd my-agent-system

# Run your first agent workflow

codex run coder "Build a simple REST API"

```

**→ [Full Quick-Start Guide](docs/[quickstart.md](<http://quickstart.md>))**

---

## 🏗️ Architecture

```

┌─────────────────────────────────────────┐

│ Artemis City Kernel │

│ (Routing, State, Governance, Memory) │

└─────────────┬───────────────────────────┘

│

┌───────┴───────┐

│ Agent Router │ ← YAML-defined (deterministic)

└───────┬───────┘

│

┌─────────┼─────────┐

▼ ▼ ▼

[Coder] [Planner] [Researcher]

│ │ │

└─────────┼─────────┘

│

┌─────────┴─────────┐

│ Memory Bus │

│ Obsidian + Supabase│

│ + MCP Tools │

└───────────────────┘

```

**Key Components:**
- **Kernel:** Central runtime managing routing, state, and governance
- **Router:** YAML-defined agent routing (no LLM guessing)
- **Memory Bus:** Persistent memory via Supabase + Obsidian
- **MCP Integration:** Tool/service protocol layer
- **Agents:** Coder, planner, researcher (extensible via plugins)

---

## 🎨 Example: Multi-Agent Workflow

```

# agent_router.yaml

routes:

- pattern: "build|create|code"
    
    agent: coder
    
    priority: high
    
- pattern: "plan|design|architecture"
    
    agent: planner
    
    priority: high
    
- pattern: "research|find|search"
    
    agent: researcher
    
    priority: medium
    

from artemis_city import Kernel

# Initialize kernel with routing config

kernel = Kernel(config="agent_router.yaml")

# Kernel decides which agent handles the request

result = kernel.execute(

"Design a microservices architecture and implement the auth service"

)

# Planner agent creates architecture

# Coder agent implements the service

# All state persisted to memory bus

```

---

## 🔥 Core Features

### 🎯 **Kernel-Driven Routing**
YAML-defined routing logic. The kernel decides, not the LLM.

### 💾 **Persistent Memory**
User-owned memory layer (Supabase + Obsidian). No vendor lock-in.

### 🛡️ **Governance Primitives**
Audit trails, tool permissions, trust-decay model for accountability.

### 🔌 **Plugin Ecosystem**
Extensible via plugins. Day-one support for OpenAI, Anthropic, filesystem, shell, Supabase.

### 🏢 **Production-Ready**
Built for reliability, not demos. State management, error handling, observability.

---
## 📚 Documentation

- **[Quick-Start Guide](docs/[quickstart.md](<http://quickstart.md>))** — Up and running in 5 minutes
- **[Architecture Overview](docs/[architecture.md](<http://architecture.md>))** — How Artemis City works
- **[Agent Templates](docs/[agents.md](<http://agents.md>))** — Pre-built agents (coder, planner, researcher)
- **[Plugin Development](docs/[plugins.md](<http://plugins.md>))** — Build your own plugins
- **[Memory Bus Guide](docs/[memory.md](<http://memory.md>))** — Supabase + Obsidian integration
- **[API Reference](docs/[api.md](<http://api.md>))** — Complete API documentation

---

## 🤝 Community

**Discord:** [Join the community](<https://discord.gg/artemis-city>)
**GitHub Discussions:** [Ask questions, share projects](<https://github.com/popvilla/Artemis-City/discussions>)
**Twitter/X:** [@artemis_city](<https://twitter.com/artemis_city>)

---

## 🛣️ Roadmap

**v1.0 (This Week):** ✅
- Kernel + Router + CLI
- Agent templates (coder, planner, researcher)
- Plugin system
- Memory bus (Supabase + Obsidian)

**v1.1 (Month 1):**
- Enhanced governance (RBAC, audit dashboard)
- Plugin marketplace
- Video tutorials
- Community showcase gallery

**v2.0 (Month 3):**
- Artemis City Cloud (managed orchestration)
- Enterprise features (SSO, compliance)
- Advanced routing (conditional, parallel)
- Performance optimizations

---

## 🌟 Why "Artemis City"?

The name came from an AI-human collaboration. When asked what to call an agentic operating system, ChatGPT chose "Artemis"—Greek goddess of the hunt, protector, guide.

That moment crystallized our philosophy: **AI and humans collaborate, but humans govern.**

[Read the full origin story →](<https://artemis-city.dev/blog/origin-story>)

---

## 📄 License

MIT License — Open-source kernel, commercial governance layer.

---

## 🚀 Get Started

```

pip install artemis-city

codex init my-first-agent

```

**→ [5-Minute Quick-Start Guide](docs/[quickstart.md](<http://quickstart.md>))**

---

*Built by developers who understand that production AI systems need governance, not hope.*
```