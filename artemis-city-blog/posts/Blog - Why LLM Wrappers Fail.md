---
title: "Why LLM Wrappers Fail (And What to Build Instead)"
date: "2024-06-12"
description: "The fundamental architectural problem with current agent frameworks"
---
**Target Audience:** Infrastructure engineers, AI developers, technical decision-makers

**Goal:** Establish technical credibility, explain the fundamental problem Artemis City solves

**CTA:** Read whitepaper, star GitHub, join Discord

**Distribution:** HackerNews, Reddit r/MachineLearning, personal blog, LinkedIn

---

# Why LLM Wrappers Fail (And What to Build Instead)

_The fundamental architectural problem with current agent frameworks_

---

Every week, a new "AI agent framework" launches on HackerNews. They all promise the same thing: **autonomous AI agents that Just Work™.**

Most fail within weeks of launch. Here's why.

---

## The Illusion of Autonomy

The typical agent framework architecture looks like this:

```
User Request → LLM → Tool Call → LLM → Next Action → LLM → ...
```

Sounds reasonable, right? **The LLM decides everything.**

This is the fundamental mistake.

---

## Problem 1: Non-Deterministic Routing

**Scenario:** You ask an agent to "build a REST API."

**Run 1:**

```
LLM: "Let me plan the architecture first"
→ Creates design doc
→ Writes code
→ Success
```

**Run 2 (same input):**

```
LLM: "I'll start coding immediately"
→ Writes spaghetti code
→ No architecture
→ Technical debt
```

**Run 3 (same input):**

```
LLM: "Let me research best practices"
→ Web searches for 20 minutes
→ Burns API credits
→ Never writes code
```

**Same input. Three different workflows. Zero predictability.**

This isn't a bug. **It's the architecture.**

---

## Problem 2: Runaway Loops

LLM-driven agents don't know when to stop.

**Real example from Auto-GPT:**

```
1. User: "Research Python best practices"
2. Agent: Searches web
3. Agent: Finds article
4. Agent: Decides it needs more context
5. Agent: Searches again
6. Agent: Finds another article
7. Agent: Decides previous search wasn't good enough
8. Agent: Searches again
...
9. User: Ctrl+C
```

**$47 in API costs. Zero useful output.**

Why? Because the LLM has no concept of "done." It just keeps generating next actions until you kill it.

---

## Problem 3: No Governance

LLMs decide which tools to call. **You don't.**

**What could go wrong?**

```python
# Agent decides to "clean up" your codebase
→ Calls filesystem_delete("/")
→ Your production database: gone
→ Your source code: gone
→ Your career: questioning life choices
```

No permissions system. No audit trail. No safety rails.

**You're trusting a probabilistic model to make deterministic infrastructure decisions.**

---

## Problem 4: Memory Theater

Most frameworks claim "persistent memory." Here's what they actually do:

**Session-based memory:**

```
Session 1: "I built a login system"
Session 2: "What login system?"
```

**Vector database memory:**

```
→ Stores everything as embeddings
→ Retrieves via semantic similarity
→ Hallucinates connections between unrelated memories
→ "I remember building that feature!" (Narrator: It didn't)
```

**The problem:** Memory is unstructured, unvalidated, and unreliable.

No trust-decay. No accountability. Just vibes.

---

## Problem 5: Vendor Lock-In

"Use our cloud memory storage!"

Translation: **Your agent's knowledge lives in our database. Forever.**

- Can't export in a usable format
- Can't use with other tools
- Can't audit what's stored
- Can't switch providers

Your AI agent is only as smart as their API availability.

---

## The Pattern: Backwards Architecture

Current frameworks put the **LLM at the center**:

```
       ┌─────────────┐
       │     LLM     │ ← Decides everything
       └──────┬──────┘
              │
  ┌───────────┼───────────┐
  ▼           ▼           ▼
Tools      Memory      Agents
```

This is like letting your CPU decide which process to run next. **Chaos.**

---

## What to Build Instead: Kernel-Driven Architecture

Invert the model. Put a **kernel at the center**:

```
       ┌─────────────┐
       │   KERNEL    │ ← Decides routing, permissions, state
       └──────┬──────┘
              │
  ┌───────────┼───────────┐
  ▼           ▼           ▼
Agents      Memory      Tools
  │           │           │
  └─────────┬─┴───────────┘
            │
          LLMs ← Compute resources, not decision makers
```

**The kernel controls:**

- **Routing:** YAML config, not LLM guessing
- **Permissions:** What tools each agent can access
- **State:** Persistent, queryable, auditable
- **Memory:** User-owned, structured, with trust-decay
- **Governance:** Audit logs, rate limits, cost tracking

**LLMs provide intelligence. The kernel provides reliability.**

---

## Concrete Example: Building a REST API

**LLM-Wrapper Framework:**

```
User: "Build a REST API"
  ↓
LLM: *flips coin* "I'll start with research"
  ↓
*30 minutes of web searches*
  ↓
LLM: "Let me think about architecture"
  ↓
*Generates 5-page design doc you didn't ask for*
  ↓
LLM: "Now I'll code"
  ↓
*API key rate limit hit*
  ↓
Result: Incomplete, unpredictable, expensive
```

**Kernel-Driven Framework (Artemis City):**

```
User: "Build a REST API"
  ↓
Kernel: *matches pattern "build|create"* → routes to coder agent
  ↓
Coder agent: Generates clean Flask/FastAPI code
  ↓
Kernel: Stores result in memory with metadata
  ↓
Result: Complete, deterministic, predictable
```

**Same input → same output. Every time.**

---

## Why This Matters for Production

If you're building demos, LLM wrappers are fine.

If you're building **production systems**, you need:

1. **Determinism:** Same input → same workflow
2. **Governance:** Audit trails, permissions, safety
3. **Reliability:** Agents that don't go rogue
4. **Observability:** Why did agent X do Y?
5. **User ownership:** Your memory, your control

**You need a kernel, not a wrapper.**

---

## The Unix Parallel

Unix doesn't let processes decide their own scheduling priority.

**Imagine if it did:**

```
Process: "I'm the most important! Give me all the CPU!"
Kernel: "Okay!"
→ System hangs
→ Nothing else runs
→ You reboot
```

**Instead, Unix has a kernel that manages:**

- Process scheduling
- Memory allocation
- I/O operations
- Permissions

**Processes provide compute. The kernel provides governance.**

Agentic systems need the same architecture.

---

## What We Built: Artemis City

We took the kernel-driven approach seriously:

**Routing:** YAML-defined patterns

```yaml
routes:
  - pattern: "build|create|code"
    agent: coder
    priority: high
```

**Governance:** RBAC + audit logs

```yaml
tool_permissions:
  coder:
    - filesystem_read
    - filesystem_write
  researcher:
    - web_search  # No write access
```

**Memory:** User-owned (Obsidian + Supabase)

```bash
codex memory connect obsidian ~/my-vault
# Your memory, your files, your control
```

**Trust-decay:** Memory reliability decreases without validation

```python
trust_score = 1.0 - (0.01 * days_old) - (0.05 * days_since_validation)
```

---

## The Results

**LLM Wrapper Framework:**

- Non-deterministic routing
- $50+ in burned API credits
- Unpredictable agent behavior
- No audit trail
- Vendor lock-in

**Artemis City (Kernel-Driven):**

- Deterministic routing (same input → same result)
- Predictable costs (no runaway loops)
- Governed agent execution (RBAC + audit)
- User-owned memory (Obsidian + Supabase)
- Production-ready reliability

---

## Try It Yourself

```bash
pip install artemis-city
codex init my-agent-system
codex run coder "Build a simple REST API"
```

**See the difference between wrappers and kernels.**

---

## The Bottom Line

LLM wrappers fail because they give control to the LLM.

**Production systems need governance, not autonomy.**

Build a kernel. Let agents be compute resources, not decision-makers.

**Your production environment will thank you.**

---

## Learn More

- [**GitHub**](https://github.com/popvilla/Artemis-City) — Production-ready kernel + router
- [**Whitepaper**](533) — Full architecture details
- [**5-Minute Quick Start**](534) — Get running in under 5 minutes
- [**Discord**](https://discord.gg/T2Huqg4c) — Join the community

---

_— Prinston Palmer_

_Ex-Morgan Stanley derivatives engineer_

_Founder, Artemis City_

_P.S. If you've burned $500 in OpenAI credits watching Auto-GPT spin in circles, you're not alone. There's a better way._