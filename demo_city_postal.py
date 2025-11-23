#!/usr/bin/env python3
"""Artemis City Postal Service Demo.

Welcome to Artemis City - a living, breathing agent ecosystem where:
- Agents are citizens with postal clearances
- Memory operations are mail deliveries
- The Obsidian vault is the City Archives
- Pack Rat handles all secure mail routing
- Trust scores determine citizen clearance levels
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from memory.integration import get_post_office, get_trust_interface


def city_welcome():
    """Welcome message for Artemis City."""
    print("\n" + "=" * 70)
    print("  WELCOME TO ARTEMIS CITY")
    print("=" * 70)
    print()
    print("A living agent ecosystem where:")
    print("    Agents are citizens with unique clearance levels")
    print("   Memory operations are mail deliveries")
    print("    The Obsidian vault serves as City Archives")
    print("   Pack Rat handles all secure postal routing")
    print("    Trust Office manages citizen clearances")
    print()
    print("=" * 70)
    print()


def demo_mail_delivery():
    """Demonstrate inter-agent mail delivery."""
    print("\n" + "=" * 70)
    print("SCENARIO 1: Inter-Agent Mail Delivery")
    print("=" * 70)
    print()
    print("Artemis wants to send a governance update to all agents...")
    
    post_office = get_post_office()
    
    # Artemis sends mail to multiple recipients
    recipients = ["pack_rat", "copilot", "codex_daemon"]
    
    for recipient in recipients:
        packet = post_office.send_mail(
            sender="artemis",
            recipient=recipient,
            subject="Weekly Governance Update",
            content=f"""
Fellow citizen {recipient},

This week's governance highlights:
- ATP protocol integration complete
- Memory layer now operational
- Postal service establishing delivery routes
- All systems nominal

The city thrives through our collaboration.

— Artemis, Mayor of Artemis City
            """.strip(),
            priority="normal"
        )

        print(f"\n   {packet}")
        input("\n   Press Enter to continue to next delivery...")
    
    print("\n All mail delivered successfully!")


def demo_mailbox_check():
    """Demonstrate checking agent mailboxes."""
    print("\n\n" + "=" * 70)
    print("SCENARIO 2: Checking Mailboxes")
    print("=" * 70)
    print()
    print("Pack Rat checks their mailbox for new deliveries...")
    
    post_office = get_post_office()
    
    # Check Pack Rat's mailbox
    mail = post_office.check_mailbox("pack_rat")
    
    if mail:
        print(f"\n    Pack Rat has mail!")
        print(f"   Review the items above for details")
    else:
        print(f"\n   📭 No mail yet (vault may be empty or MCP not connected)")
    
    input("\n   Press Enter to continue...")


def demo_archival_system():
    """Demonstrate City Archives filing."""
    print("\n\n" + "=" * 70)
    print("SCENARIO 3: City Archives")
    print("=" * 70)
    print()
    print("Artemis files a reflection in the City Archives...")
    
    post_office = get_post_office()
    
    reflection = """
# Weekly Reflection - City Operations

## Accomplishments
- Postal service operational
- Inter-agent communication established
- Trust clearances functioning
- Pack Rat handling deliveries efficiently

## Observations
- Citizens collaborating effectively
- Archive system organizing knowledge well
- Trust decay model maintaining security

## Next Steps
- Enhance routing efficiency
- Add more archive sections
- Monitor citizen clearance levels

The city is alive and thriving.
    """.strip()
    
    response = post_office.send_to_archives(
        sender="artemis",
        archive_section="Reflections",
        title="Weekly_Operations_Report",
        content=reflection
    )
    
    if response.success:
        print("\n    Reflection successfully archived!")
    
    input("\n   Press Enter to continue...")


def demo_archive_search():
    """Demonstrate searching City Archives."""
    print("\n\n" + "=" * 70)
    print("SCENARIO 4: Archive Research")
    print("=" * 70)
    print()
    print("Copilot searches archives for governance information...")
    
    post_office = get_post_office()
    
    results = post_office.request_from_archives(
        requester="copilot",
        query="governance",
        section="Reflections"
    )
    
    if results:
        print(f"\n    Research successful!")
        print(f"   Copilot can now reference historical documents")
    else:
        print(f"\n   📭 No archived documents found yet")
        print(f"   (This is expected on first run)")
    
    input("\n   Press Enter to continue...")


def demo_trust_clearances():
    """Demonstrate trust-based clearance system."""
    print("\n\n" + "=" * 70)
    print("SCENARIO 5: Citizen Clearance Levels")
    print("=" * 70)
    print()
    print("The Trust Office manages citizen clearances...")
    
    trust = get_trust_interface()
    
    print("\n     CURRENT CITIZEN CLEARANCES")
    print("   " + "=" * 60)
    
    citizens = ["artemis", "pack_rat", "codex_daemon", "copilot"]
    
    for citizen in citizens:
        score = trust.get_trust_score(citizen)
        
        # Visualize trust level
        bar_length = int(score.score * 20)
        trust_bar = "█" * bar_length + "░" * (20 - bar_length)
        
        print(f"\n   {citizen:15}")
        print(f"     Level: {score.level.value:10} [{trust_bar}] {score.score:.2f}")
        print(f"     Clearances: ", end="")
        
        # Show what they can do
        can_read = "📖 Read" if trust.can_perform_operation(citizen, 'read') else ""
        can_write = "✍️  Write" if trust.can_perform_operation(citizen, 'write') else ""
        can_delete = "🗑️  Delete" if trust.can_perform_operation(citizen, 'delete') else ""
        
        clearances = [c for c in [can_read, can_write, can_delete] if c]
        print(" | ".join(clearances))
    
    print("\n   " + "=" * 60)
    
    input("\n   Press Enter to continue...")


def demo_postal_report():
    """Generate final postal service report."""
    print("\n\n" + "=" * 70)
    print("FINALE: Postal Service Report")
    print("=" * 70)
    print()
    print("Generating city-wide activity report...")
    
    post_office = get_post_office()
    report = post_office.get_postal_report()
    
    print("\n End of Day Summary")
    print("=" * 70)
    print()
    print("The Post Office processed all mail efficiently.")
    print("Pack Rat performed admirably in delivery duties.")
    print("All citizens maintained their clearance levels.")
    print("The City Archives grew with new knowledge.")
    print()
    print("Artemis City thrives through collaboration!")
    print()
    print("=" * 70)


def main():
    """Run the Artemis City postal service demonstration."""
    
    city_welcome()
    
    print("This demo showcases the living city theme where:")
    print("  • Agents communicate through postal mail")
    print("  • Pack Rat delivers all messages securely")
    print("  • Trust Office manages citizen clearances")
    print("  • City Archives preserve institutional knowledge")
    print()
    print("Note: MCP server must be running for full functionality.")
    print("      Demo will work offline with simulated responses.")
    print()
    
    try:
        input("Press Enter to begin the city tour...")
        
        # Run scenarios
        demo_mail_delivery()
        demo_mailbox_check()
        demo_archival_system()
        demo_archive_search()
        demo_trust_clearances()
        demo_postal_report()
        
        # Closing
        print("\n\n" + "=" * 70)
        print("  THANK YOU FOR VISITING ARTEMIS CITY")
        print("=" * 70)
        print()
        print("You've seen how agents in Artemis City:")
        print("   Send and receive mail through Pack Rat")
        print("   File documents in City Archives")
        print("   Maintain trust-based clearances")
        print("   Collaborate as citizens of a living ecosystem")
        print()
        print("The city is ready for your agents to move in!")
        print()
        print("To start using the postal service:")
        print("  1. Start MCP server: cd 'Artemis Agentic Memory Layer' && npm run dev")
        print("  2. Set environment: export MCP_BASE_URL=... MCP_API_KEY=...")
        print("  3. Import: from memory.integration import get_post_office")
        print("  4. Use: post_office.send_mail(sender, recipient, subject, content)")
        print()
        print("=" * 70)
        print()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye from Artemis City!")
        print()
    except Exception as e:
        print(f"\n\n  City services encountered an issue: {e}")
        print("This may be because MCP server is not running.")
        print("The demo requires MCP_BASE_URL and MCP_API_KEY environment variables.")
        print()


if __name__ == "__main__":
    main()
