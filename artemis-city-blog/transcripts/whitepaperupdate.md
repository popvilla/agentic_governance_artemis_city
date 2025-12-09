# Whitebook Update Notes

Source reviewed: `mediafiles/Whitebook_Artemiscity` (raw whitebook) and `posts/Whitepaper - Agentic OS Architecture.md` (blog render).

## Key Critiques
- **Memory bus is underspecified**: No end-to-end sync protocol between Obsidian graph and Supabase vectors (freshness guarantees, conflict resolution, batching, write-ahead logging, latency budgets, or how queries see “most recent” state mid-flight).
- **Governance for self-modification is missing**: The roadmap mentions plastic workflows and self-updates but lacks CI/CD-style gates, approvers, rollback paths, or reliability thresholds tied to agent scores.
- **Sandboxing and observability gaps**: Sandbox enforcement is mentioned but not defined (what is jailed, how tools are whitelisted, how violations are logged/blocked when `main.py` runs).
- **Cost, latency, and reliability KPIs absent**: No budgets for token/compute/storage, p95/p99 routing latency targets, cache strategy, or measurement plan to prove savings vs. baseline agent stacks.
- **Quantum lock concept undefined**: “Quantum lock theory” is referenced without an explanation, threat model, or place in the architecture (e.g., data sealing, provenance, or tamper-evidence).
- **Decay and retention policy lacks auditability**: Forgetting is proposed but there is no policy for when/how edges/nodes decay, how to review/restore them, or how decay events are logged for compliance.
- **References and evidentiary quality**: Heavy reliance on popular articles and Stack Overflow; few peer-reviewed sources for governance, memory safety, or routing claims.
- **Examples and artifacts missing**: No concrete kernel/memory/gov sequence diagrams, sample registry schema, or minimal configuration that shows the OS in action.
- **Community/onboarding accuracy**: Discord invite link is outdated; no mention of where to find change log or issue tracker for the whitebook itself.

## Recommended Updates
- **Define memory sync contract**: Add a section detailing write path (agent -> bus -> Obsidian + Supabase upsert), read path (consistent reads and staleness bounds), conflict handling, batching, WAL/checkpointing, and metrics (lag, failure rate). Include a timing diagram.
- **Add CI-style governance for self-changes**: Specify triggers for self-updates, required approvals based on agent reputation, pre-merge checks (lint, safety evals, simulated rollouts), rollback/kill-switch behavior, and audit logging.
- **Document sandbox policy**: Describe default jail, allowed syscalls/tools, privilege escalation rules, and how violations surface in logs; include an example `main.py` run showing sandbox annotations.
- **Publish KPI targets and instrumentation**: Set initial SLOs (e.g., p95 routing latency, max token spend per task, memory sync lag), define dashboards, and tie them to the Hebbian/router roadmap to prove efficiency gains.
- **Clarify quantum lock scope**: Either remove or concretely define as a security control (e.g., signed state checkpoints, data integrity proofs) with integration points and validation flow.
- **Ship decay/retention policy**: Outline decay intervals, thresholds, archival vs. delete behavior, restoration hooks, and log schema for decayed items to keep provenance.
- **Strengthen sources**: Swap weak citations with peer-reviewed or vendor docs for governance, observability, and memory safety; cite concrete implementations where possible.
- **Add runnable artifacts**: Include a minimal config (agent registry, kernel rule, memory example), a sequence diagram for kernel→agent→memory→governance, and a sample governance incident log.
- **Refresh community pointers**: Update Discord invite to `https://discord.gg/T2Huqg4c` and add a short “How to contribute feedback” note pointing to changelog/issues.
