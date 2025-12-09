---
title: "HackerNews Launch Post for Artemis City"
date: "2024-06-20"
description: "Comprehensive plan for launching Artemis City on HackerNews, including post content, timing strategy, engagement guidelines, and success metrics."
---
**Target:** HackerNews front page

**Goal:** GitHub stars, technical discussion, community building

**Format:** Show HN

**Critical Success:** Stay on front page 6+ hours, 100+ upvotes, 50+ comments

---

# HackerNews Show HN Post

## Title Options (Choose One)

**Option 1 (Recommended):**

```
Show HN: Artemis City – Kernel-driven OS for AI agents (not another LLM wrapper)
```

**Option 2 (Technical Angle):**

```
Show HN: Artemis City – Deterministic multi-agent orchestration via kernel routing
```

**Option 3 (Problem-Solution):**

```
Show HN: Artemis City – Production AI agents with governance (vs Auto-GPT's chaos)
```

**Recommended:** Option 1 (differentiates immediately, avoids jargon)

---

## Post Body

```
Hey HN,

I'm Prinston, ex-Morgan Stanley derivatives engineer. I spent 10 years building C++ systems where a single miscalculation could lose millions. One rule I learned: never let probabilistic models make deterministic infrastructure decisions.

Every AI agent framework breaks this rule.

Auto-GPT, LangChain, BabyAGI—they all put the LLM in charge of routing, tools, and orchestration. Result: non-deterministic behavior, runaway loops burning API credits, zero governance, and nothing you'd deploy to production.

So I built Artemis City—a kernel-driven operating system for AI agents.

**The Architecture:**

Instead of:
```

LLM → decides routing → calls tools → decides next action

```

Artemis City does:
```

Kernel → routes via YAML → LLM executes → Kernel logs/governs

```

Like Unix: processes provide compute, the kernel provides governance.

**What's included:**

- Deterministic routing via YAML config (same input → same output, every time)
- Multi-agent orchestration (coder, planner, researcher agents)
- User-owned memory (Obsidian + Supabase, no vendor lock-in)
- Governance primitives (RBAC, audit trails, cost budgets)
- Trust-decay memory model (reliability decreases without validation)
- Plugin system (OpenAI, Anthropic, filesystem, shell, MCP)

**Quick example:**

```

# agent_router.yaml

routes:

- pattern: "build|create|code"

    agent: coder

    priority: high

- pattern: "research|investigate"

    agent: researcher

    priority: medium


codex run "Build a REST API"

# Kernel routes to coder (deterministic)

# Agent executes

# Result saved to memory bus

# Audit log created

```

**Why this matters:**

If you're exploring what LLMs can do autonomously, Auto-GPT is great. If you're building production systems that need to work the same way every time, you need a kernel.

**Try it:**
```

pip install artemis-city

codex init my-agent-system

codex run coder "Hello world"

```

GitHub: [your-github-link]
Whitepaper (architecture details): [link]
5-min quick-start: [link]

**Tech stack:**
- Python 3.10+
- YAML-based routing
- Supabase/Postgres for structured memory
- Obsidian for unstructured memory
- MCP (Model Context Protocol) for tools

This is v1.0—not perfect, but production-ready. Open to feedback, questions about architecture, and PRs.

Happy to answer questions about:
- Why YAML routing vs LLM routing
- The trust-decay memory model
- How governance works
- Multi-agent coordination
- Comparison to other frameworks

P.S. The name came from asking ChatGPT what to call an agentic OS. It chose "Artemis." That moment crystallized the philosophy: AI and humans collaborate, but humans govern.
```

---

## Posting Strategy

**Best Time to Post:**

- **Weekday:** Tuesday-Thursday
- **Time:** 7-9 AM Pacific (10 AM-12 PM Eastern)
- **Rationale:** Maximum US developer audience, gives time to climb before end of workday

**Avoid:**

- Monday (inbox catch-up)
- Friday afternoon (weekend mode)
- Weekends (lower traffic)

---

## First Hour Response Strategy

**First 5-10 comments are critical.** They set the tone.

### Expected Questions & Responses

**Q: "How is this different from Auto-GPT?"**

A:

```
Great question. Auto-GPT puts the LLM in charge of everything—routing, tools, next actions. This is great for exploration but non-deterministic (same input → different outputs).

Artemis City inverts this: kernel handles routing deterministically via YAML, LLM provides intelligence. Same input → same workflow every time.

Both valid—different use cases. Auto-GPT for exploration, Artemis City for production.

Detailed comparison: [link]
```

**Q: "Why not just use LangChain?"**

A:

```
LangChain is an LLM abstraction layer (chains, prompts, memory). It still has the LLM decide routing.

Artemis City is an OS layer—kernel manages routing, state, governance. LLMs are compute resources, not orchestrators.

Think of it as: LangChain = stdlib, Artemis City = kernel.

They could work together—you could use LangChain inside an Artemis City agent.
```

**Q: "What's the trust-decay model?"**

A:

```
Memory reliability decreases over time without validation:

trust_score = 1.0 - (0.01 * days_old) - (0.05 * days_since_validation)

This encourages re-validation of old assumptions and prevents stale data from influencing decisions.

Example: A 30-day-old memory never re-validated has trust_score = 0.55. Agent knows to verify before using.

Full details in whitepaper: [link]
```

**Q: "Is this just wrapping OpenAI/Anthropic?"**

A:

```
No—Artemis City is the orchestration layer *around* LLMs.

You bring your own LLM (OpenAI, Anthropic, local models via Ollama). The kernel handles:
- Routing (which agent)
- Permissions (which tools)
- Memory (persistence)
- Audit (what happened)
- State (cross-session)

LLMs provide intelligence. Kernel provides governance.
```

**Q: "Why YAML for routing?"**

A:

```
Determinism + version control + testability.

YAML routing means:
1. Same pattern → same agent (deterministic)
2. Git-trackable (see routing changes over time)
3. Unit testable (codex router test "query")
4. No LLM call for routing decisions (fast + cheap)

You can update routing logic without touching code.
```

**Q: "Production deployments yet?"**

A:

```
We've been dogfooding for 2 months (building Artemis City with Artemis City).

v1.0 launched today, but the architecture has been stable for 6 weeks.

A few early adopters are deploying this week. Happy to do a call if you're evaluating for production use.
```

**Q: "What about scaling? Multi-instance?"**

A:

```
Good question. v1.0 is single-instance.

v2.0 roadmap (Q1 2026):
- Distributed kernel (multiple instances)
- Agent federation (specialized remote agents)
- Artemis City Cloud (managed orchestration)

For now, you can run multiple kernels with shared memory (Supabase).
```

**Q: "License?"**

A:

```
Artemis City is proprietary software. We're building commercial governance features and a robust enterprise-ready platform.
```

**Q: "How do I contribute?"**

A:

```
We'd love contributions!

Easiest places to start:
1. Plugin development (new tools/models)
2. Agent templates (domain-specific agents)
3. Documentation improvements
4. Example workflows

[CONTRIBUTING.md](<http://CONTRIBUTING.md>) in the repo. Discord for questions: [link]
```

---

## If Post Gets Negative/Critical Comments

### "This is just another wrapper"

**Response:**

```
I can see why it might look that way from the quick description.

The key difference is architectural:
- Wrappers abstract LLM APIs (easier to switch models)
- Artemis City is an OS layer (routing, state, governance)

It's closer to systemd than it is to an SDK.

If you're curious about the architecture, the whitepaper goes deep: [link]

Happy to clarify any specific points.
```

### "Why not just use X?"

**Response:**

```
X is great for [specific use case].

Artemis City is focused on [different use case]: deterministic multi-agent orchestration with governance.

They solve different problems. If X works for you, keep using it.

I built this because I needed:
- Same input → same workflow
- User-owned memory
- Production-grade audit trails

And couldn't find a framework that did all three.
```

### "This is overengineered"

**Response:**

```
Fair criticism. If you're building one-off agents, this is probably overkill.

Artemis City is for:
- Multi-agent systems
- Production deployments
- Enterprise governance needs

If you just need a quick demo agent, Auto-GPT or a simple script is simpler.

Different tools for different problems.
```

---

## Engagement Guidelines

**Do:**

- ✅ Respond to every substantive question in first 2 hours
- ✅ Be humble and acknowledge limitations
- ✅ Link to detailed docs instead of writing essays
- ✅ Thank people for feedback/criticism
- ✅ Admit when something is a good idea you haven't implemented

**Don't:**

- ❌ Get defensive about criticism
- ❌ Claim to be better than everything
- ❌ Over-sell capabilities
- ❌ Ignore negative feedback
- ❌ Argue with trolls (downvote and move on)

---

## Success Metrics

**Minimum Success:**

- 50+ upvotes
- 30+ comments
- 20+ GitHub stars from HN traffic
- Stays on front page 4+ hours

**Good Success:**

- 100+ upvotes
- 50+ comments
- 50+ GitHub stars
- Stays on front page 8+ hours

**Great Success:**

- 200+ upvotes
- 100+ comments
- 100+ GitHub stars
- Top 5 on front page

---

## Post-Mortem Template

**After 24 hours, document:**

1. **What worked:**
    - Which comments got most engagement
    - Which parts of explanation resonated
    - Which comparisons were effective
2. **What didn't work:**
    - Confusing explanations
    - Skeptical responses
    - Unaddressed concerns
3. **Top feedback themes:**
    - Feature requests
    - Architecture questions
    - Use case fit
4. **Conversion:**
    - GitHub stars from HN referrer
    - Discord joins
    - Quick-start completions
5. **Next time:**
    - Adjust messaging
    - Add missing info to docs
    - Address common objections upfront

---

## Emergency: If Post Isn't Gaining Traction

**First hour < 10 upvotes:**

Don't panic. Sometimes timing is wrong.

**Options:**

- Delete and repost at better time (Tuesday 8 AM PT)
- Share in focused communities (Discord, Reddit) for initial momentum
- Ask 2-3 friends to check it out (don't ask for upvotes explicitly)

**If it's dying:**

- Learn from comments
- Iterate on messaging
- Try again in a week with better framing

---

## Ready to Post?

**Pre-flight checklist:**

- [ ] GitHub repo public and polished
- [ ] README matches messaging
- [ ] Quick-start guide works (test it fresh)
- [ ] Discord server ready for influx
- [ ] You're available for 4+ hours to respond
- [ ] Whitepaper accessible
- [ ] No broken links

**Post, then:**

1. Set timer for 15-min check-ins (first 2 hours)
2. Respond to every substantive comment
3. Share in Discord that you're live on HN
4. Monitor GitHub stars/issues
5. Track referral analytics

**Good luck. You've got this. 🚀**
