#!/usr/bin/env python3
"""Demo script showcasing memory layer integration.

This demonstrates:
- Memory client connecting to MCP server
- Trust interface for access control
- Context loading from Obsidian vault
- Agent-vault interaction patterns
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from memory.integration import (
    MemoryClient,
    TrustInterface,
    get_trust_interface,
    ContextLoader,
    TrustLevel
)


def demo_memory_client():
    """Demonstrate memory client operations."""
    print("=" * 70)
    print("DEMO 1: Memory Client (MCP Server Connection)")
    print("=" * 70)
    
    # Initialize client
    try:
        client = MemoryClient()
        print(f"\n✓ Memory client initialized")
        print(f"  Base URL: {client.base_url}")
        print(f"  API Key: {'*' * 20} (hidden)")
    except ValueError as e:
        print(f"\n✗ Failed to initialize: {e}")
        print("\nTo use memory layer, set environment variables:")
        print("  export MCP_BASE_URL=http://localhost:3000")
        print("  export MCP_API_KEY=your_mcp_api_key")
        return None
    
    # Health check
    print("\n" + "-" * 70)
    print("\nHealth Check:")
    is_healthy = client.health_check()
    if is_healthy:
        print("  ✓ MCP server is accessible")
    else:
        print("  ✗ MCP server is not accessible")
        print("  Make sure:")
        print("    1. Obsidian is running")
        print("    2. Local REST API plugin is enabled")
        print("    3. MCP server is running (npm run dev in Memory Layer)")
        return None
    
    return client


def demo_trust_interface():
    """Demonstrate trust interface and access control."""
    print("\n" + "=" * 70)
    print("DEMO 2: Trust Interface & Access Control")
    print("=" * 70)
    
    trust = get_trust_interface()
    
    # Show initialized agents
    print("\n[Pre-configured Agent Trust Scores]")
    for agent_id in ['artemis', 'pack_rat', 'codex_daemon', 'copilot']:
        score = trust.get_trust_score(agent_id)
        print(f"  {agent_id:15} | Score: {score.score:.2f} | Level: {score.level.value:8}")
    
    # Create new agent
    print("\n" + "-" * 70)
    print("\n[Creating New Agent]")
    new_agent = "test_agent"
    score = trust.get_trust_score(new_agent)
    print(f"  {new_agent:15} | Score: {score.score:.2f} | Level: {score.level.value:8}")
    
    # Check permissions
    print("\n" + "-" * 70)
    print("\n[Permission Matrix]")
    operations = ['read', 'write', 'delete', 'search', 'tag']
    
    print(f"{'Operation':<12} | {'artemis':<8} | {'test_agent':<11} | {'low_trust':<10}")
    print("-" * 60)
    
    # Set low trust agent
    low_trust_score = trust.get_trust_score("low_trust", "agent")
    low_trust_score.score = 0.4
    low_trust_score._update_level()
    
    for op in operations:
        artemis_ok = "✓" if trust.can_perform_operation('artemis', op) else "✗"
        test_ok = "✓" if trust.can_perform_operation('test_agent', op) else "✗"
        low_ok = "✓" if trust.can_perform_operation('low_trust', op) else "✗"
        print(f"{op:<12} | {artemis_ok:^8} | {test_ok:^11} | {low_ok:^10}")
    
    # Record events
    print("\n" + "-" * 70)
    print("\n[Recording Trust Events]")
    trust.record_success('test_agent')
    trust.record_success('test_agent')
    trust.record_failure('low_trust')
    
    updated_test = trust.get_trust_score('test_agent')
    updated_low = trust.get_trust_score('low_trust')
    
    print(f"  test_agent after 2 successes: {updated_test.score:.3f}")
    print(f"  low_trust after 1 failure:    {updated_low.score:.3f}")

    # Trust report
    print("\n" + "-" * 70)
    print("\n[Trust Report]")
    report = trust.get_trust_report()
    print(f"  Total entities: {report['total_entities']}")
    for level, entities in report['by_level'].items():
        print(f"\n  {level.upper()}:")
        for entity in entities:
            print(f"    - {entity['id']} (score: {entity['score']})")

    print()


def demo_context_loader(client: MemoryClient):
    """Demonstrate context loading from Obsidian."""
    print("\n" + "=" * 70)
    print("DEMO 3: Context Loader (Obsidian Vault)")
    print("=" * 70)
    
    loader = ContextLoader(client)
    
    # Search context
    print("\n[Searching Vault]")
    query = "artemis"
    print(f"  Query: '{query}'")
    
    entries = loader.search_context(query, limit=5)
    if entries:
        print(f"  Found {len(entries)} matching notes:")
        for entry in entries:
            print(f"    - {entry.path}")
            if entry.tags:
                print(f"      Tags: {', '.join(entry.tags)}")
    else:
        print("  No results found (vault may be empty or MCP server not accessible)")
    
    # Load agent history
    print("\n" + "-" * 70)
    print("\n[Loading Agent History]")
    agent_name = "artemis"
    print(f"  Agent: {agent_name}")
    
    history = loader.load_agent_history(agent_name, limit=3)
    if history:
        print(f"  Found {len(history)} historical entries")
        summary = loader.get_context_summary(history, max_entries=2)
        print(f"\n{summary}")
    else:
        print("  No history found (agent may not have stored context yet)")
    
    # Store context example
    print("\n" + "-" * 70)
    print("\n[Storing Agent Context]")
    context_text = "Executed ATP demo and memory integration test successfully."
    print(f"  Storing: {context_text[:50]}...")
    
    response = client.store_agent_context("demo_agent", context_text)
    if response.success:
        print(f"  ✓ Context stored: {response.message}")
    else:
        print(f"  ✗ Failed to store: {response.error}")

    print()


def demo_integrated_workflow(client: MemoryClient):
    """Demonstrate integrated agent-memory workflow."""
    print("\n" + "=" * 70)
    print("DEMO 4: Integrated Agent-Memory Workflow")
    print("=" * 70)
    
    trust = get_trust_interface()
    loader = ContextLoader(client)
    
    # Scenario: Artemis agent wants to store reflection
    print("\n[Scenario: Artemis Storing Reflection]")
    agent_name = "artemis"
    
    # Check permission
    can_write = trust.can_perform_operation(agent_name, 'write')
    print(f"  Agent: {agent_name}")
    print(f"  Permission to write: {'✓ Yes' if can_write else '✗ No'}")
    
    if not can_write:
        print("  Access denied - trust level too low")
        return
    
    # Store reflection
    reflection = """
    Reflected on current system state:
    - ATP protocol successfully implemented
    - Memory layer integration complete
    - Trust interface operational
    
    Next steps:
    - Enhance CLI with memory persistence
    - Add cross-session context loading
    """
    
    print("\n  Storing reflection...")
    response = client.store_agent_context(agent_name, reflection, "Reflections")
    
    if response.success:
        print(f"  ✓ Stored: {response.message}")
        trust.record_success(agent_name)
        print(f"  ✓ Trust reinforced")
        
        # Verify storage
        print("\n  Verifying storage...")
        history = loader.load_agent_history(agent_name, limit=1)
        if history:
            print(f"  ✓ Successfully retrieved {len(history)} entry")
        
    else:
        print(f"  ✗ Failed: {response.error}")
        trust.record_failure(agent_name)
        print(f"  ✗ Trust penalized")
    
    # Show updated trust
    updated_score = trust.get_trust_score(agent_name)
    print(f"\n  Updated trust score: {updated_score.score:.3f} ({updated_score.level.value})")
    
    print()


def demo_trust_decay():
    """Demonstrate trust decay over time."""
    print("\n" + "=" * 70)
    print("DEMO 5: Trust Decay Model")
    print("=" * 70)
    
    trust = get_trust_interface()
    
    print("\n[Trust Decay Simulation]")
    print("  Note: Decay is applied based on days since last update")
    
    # Get current score
    agent_name = "test_decay_agent"
    score = trust.get_trust_score(agent_name)
    
    print(f"\n  Initial score: {score.score:.3f}")
    print(f"  Decay rate: {score.decay_rate * 100}% per day")
    
    # Simulate decay
    from datetime import timedelta
    score.last_updated = score.last_updated - timedelta(days=30)
    
    decayed_score = score.apply_decay()
    print(f"\n  After 30 days without reinforcement:")
    print(f"  Decayed score: {decayed_score:.3f}")
    
    # Show how reinforcement prevents decay
    print("\n  With regular reinforcement:")
    for day in [0, 10, 20, 30]:
        score.last_updated = score.last_updated - timedelta(days=day)
        if day % 10 == 0 and day > 0:
            score.reinforce(0.02)
            print(f"    Day {day}: Reinforced +0.02")
        score_value = score.apply_decay()
        print(f"    Day {day}: Score = {score_value:.3f}")

    print()


def main():
    """Run all memory integration demos."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "MEMORY LAYER INTEGRATION DEMO" + " " * 24 + "║")
    print("║" + " " * 12 + "Artemis City ↔ Obsidian MCP Server" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Demo 1: Memory Client
    client = demo_memory_client()
    if client:
        input("\nPress Enter to continue...")
    
    # Demo 2: Trust Interface
    demo_trust_interface()
    input("\nPress Enter to continue...")
    
    # Demo 3: Context Loader (only if client is available)
    if client:
        demo_context_loader(client)
        input("\nPress Enter to continue...")
        
        # Demo 4: Integrated Workflow
        demo_integrated_workflow(client)
        input("\nPress Enter to continue...")
    
    # Demo 5: Trust Decay (works without MCP server)
    demo_trust_decay()
    
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("\nMemory layer integration is ready!")
    print("\nKey Features Demonstrated:")
    print("  ✓ REST client for MCP server")
    print("  ✓ Trust-based access control")
    print("  ✓ Context loading from Obsidian")
    print("  ✓ Agent-vault interaction")
    print("  ✓ Trust decay model")
    print("\nNext Steps:")
    print("  1. Start MCP server: cd 'Artemis Agentic Memory Layer' && npm run dev")
    print("  2. Set environment: export MCP_BASE_URL=... MCP_API_KEY=...")
    print("  3. Run CLI with memory: python interface/codex_cli.py")
    print()


if __name__ == "__main__":
    main()
