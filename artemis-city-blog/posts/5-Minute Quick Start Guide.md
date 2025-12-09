---
title: "5-Minute Quick Start Guide"
date: "2024-06-10"
description: "Get up and running with Artemis City in under 5 minutes. This step-by-step guide walks you through installation, initialization, and running your first multi-agent workflows."
---
## Prerequisites

-   Python 3.10+
-   pip or uv
-   OpenAI API key (or Anthropic, or local model)

------------------------------------------------------------------------

## Step 1: Install (30 seconds)

``` bash
pip install artemis-city
```

Or with uv:

``` bash
uv pip install artemis-city
```

**Verify installation:**

``` bash
codex --version
# Output: Artemis City Codex v1.0.0
```

------------------------------------------------------------------------

## Step 2: Initialize Your First Agent System (1 minute)

``` bash
codex init my-agent-system
```

**This creates:**

```  
my-agent-system/
├── agent_router.yaml    # Routing configuration
├── kernel.json          # Kernel state file
├── .env                 # API keys
├── agents/              # Agent definitions
│   ├── coder.yaml
│   ├── planner.yaml
│   └── researcher.yaml
└── memory/              # Memory bus storage
```

**Configure your API key:**

``` bash
cd my-agent-system
echo "OPENAI_API_KEY=your-key-here" > .env
```

------------------------------------------------------------------------

## Step 3: Run Your First Agent (30 seconds)

``` bash
codex run coder "Create a Python function that calculates Fibonacci numbers"
```

**What happens:**

1.  Kernel loads routing config
2.  Routes request to `coder` agent
3.  Agent executes task
4.  Result saved to memory bus
5.  Output displayed

**Expected output:**

```  
🏛️  Artemis City Kernel v1.0.0
🎯 Routing to agent: coder (confidence: 0.95)
⚡ Executing task...

✅ Task completed

📄 Output:
```

def fibonacci(n):

"""Calculate the nth Fibonacci number."""

if n \<= 1:

return n

return fibonacci(n-1) + fibonacci(n-2)

```  

💾 Saved to memory: memory/tasks/task_[001.md](<http://001.md>)
⏱️  Completed in 3.2s
```

------------------------------------------------------------------------

## Step 4: Try Multi-Agent Orchestration (2 minutes)

``` bash
codex run "Plan a REST API for a todo app, then implement the create endpoint"
```

**What happens:**

1.  Kernel routes "plan" to **planner** agent
2.  Planner creates architecture
3.  Kernel routes "implement" to **coder** agent
4.  Coder builds the endpoint
5.  Both stored in memory with linked context

------------------------------------------------------------------------

## Step 5: Check Your Memory Bus (1 minute)

``` bash
codex memory list
```

**Output:**

```  
📚 Memory Bus Contents:

1. [2025-12-05 14:23] task_001 - Fibonacci function
   Agent: coder | Status: ✅ complete

2. [2025-12-05 14:28] task_002 - REST API planning
   Agent: planner | Status: ✅ complete

3. [2025-12-05 14:29] task_003 - Create endpoint implementation
   Agent: coder | Status: ✅ complete
   Links: → task_002
```

**View a specific memory:**

``` bash
codex memory show task_003
```

------------------------------------------------------------------------

## 🎯 What You Just Did

✅ Installed Artemis City

✅ Initialized a kernel-driven agent system

✅ Ran a single-agent task

✅ Orchestrated multiple agents

✅ Explored the persistent memory bus

**Total time:** Under 5 minutes

------------------------------------------------------------------------

## 🚀 Next Steps

### Customize Agent Routing

Edit `agent_router.yaml`:

``` yaml
routes:
  - pattern: "build|create|code|implement"
    agent: coder
    priority: high

  - pattern: "plan|design|architect"
    agent: planner
    priority: high

  - pattern: "research|find|search|investigate"
    agent: researcher
    priority: medium

  - pattern: ".*"  # Catch-all
    agent: planner  # Default to planning
    priority: low
```

### Create a Custom Agent

``` bash
codex agent create reviewer
```

Edit `agents/reviewer.yaml`:

``` yaml
name: reviewer
role: Code review and quality assurance
model: gpt-4
temperature: 0.3
system_prompt: |
  You are a senior code reviewer focused on:
  - Code quality and best practices
  - Security vulnerabilities
  - Performance optimizations
  - Documentation completeness
tools:
  - filesystem_read
  - lint_analyzer
```

### Connect to Obsidian (User-Owned Memory)

``` bash
codex memory connect obsidian /path/to/your/vault
```

Now all agent memory is stored in your Obsidian vault.

### Add Supabase (Structured Memory)

``` bash
codex memory connect supabase
```

Follow prompts to enter your Supabase URL and API key.

------------------------------------------------------------------------

## 📚 Learn More

-   [**Architecture Deep-Dive**](architecture.md) — How the kernel works
-   [**Agent Development Guide**](agents.md) — Build custom agents
-   [**Plugin System**](plugins.md) — Extend functionality
-   [**Memory Bus Details**](memory.md) — Obsidian + Supabase integration
-   [**API Reference**](api.md) — Complete API docs

------------------------------------------------------------------------

## 🤝 Join the Community

**Discord:** [discord.gg/T2Huqg4c](https://discord.gg/T2Huqg4c)

**GitHub Discussions:** [github.com/popvilla/Artemis-City/discussions](https://github.com/popvilla/Artemis-City/discussions)

------------------------------------------------------------------------

## ❓ Troubleshooting

**Issue:** `codex: command not found`

**Solution:** Add to PATH or use:

``` bash
python -m artemis_city.cli <command>
```

------------------------------------------------------------------------

**Issue:** API key errors

**Solution:** Verify `.env` file:

``` bash
cat .env
# Should show: OPENAI_API_KEY=sk-...
```

------------------------------------------------------------------------

**Issue:** Agent not routing correctly

**Solution:** Test routing:

``` bash
codex router test "your query here"
# Shows which agent would handle the request
```

------------------------------------------------------------------------

## 🎉 You're Ready!

You now have a kernel-driven, multi-agent system with persistent memory.

**Build something amazing. Share it in Discord. We can't wait to see what you create.**
