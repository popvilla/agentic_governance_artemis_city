#!/usr/bin/env python3
"""Demo script showcasing Artemis persona features.

This demonstrates:
- ATP protocol parsing
- Instruction hierarchy loading
- Artemis personality and response modes
- Reflection and concept synthesis
- Semantic tagging and citations
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.atp import ATPParser, ATPValidator
from core.instructions import InstructionLoader
from agents.artemis import ArtemisPersona, ReflectionEngine, SemanticTagger


def demo_atp_parsing():
    """Demonstrate ATP protocol parsing."""
    print("=" * 70)
    print("DEMO 1: ATP Protocol Parsing")
    print("=" * 70)
    
    parser = ATPParser()
    validator = ATPValidator()
    
    # Example ATP message
    atp_text = """
#Mode: Build
#Context: Implementing new agent communication layer
#Priority: High
#ActionType: Execute
#TargetZone: /agents/communication/

Create message protocol with context hashing for agent-to-agent communication.
    """
    
    message = parser.parse(atp_text)
    
    print("\nInput:")
    print(atp_text)
    
    print("\nParsed ATP Message:")
    print(f"  Mode: {message.mode.value}")
    print(f"  Context: {message.context}")
    print(f"  Priority: {message.priority.value}")
    print(f"  Action: {message.action_type.value}")
    print(f"  Target: {message.target_zone}")
    print(f"  Content: {message.content}")
    
    # Validate
    result = validator.validate(message)
    print(f"\nValidation: {'✓ PASSED' if result.is_valid else '✗ FAILED'}")
    if result.has_issues:
        print(result)
    
    print()


def demo_instruction_loading():
    """Demonstrate instruction hierarchy loading."""
    print("=" * 70)
    print("DEMO 2: Instruction Hierarchy Loading")
    print("=" * 70)
    
    loader = InstructionLoader()
    instruction_set = loader.load()
    
    print(f"\nProject Root: {loader.project_root}")
    print(f"\nLoaded {len(instruction_set.scopes)} scope(s):")
    
    for scope in instruction_set.scopes:
        print(f"\n  [{scope.level.upper()}] Priority: {scope.priority}")
        print(f"  Path: {scope.path}")
        print(f"  Content length: {len(scope.content)} characters")
    
    print()


def demo_artemis_persona():
    """Demonstrate Artemis personality and response modes."""
    print("=" * 70)
    print("DEMO 3: Artemis Personality & Response Modes")
    print("=" * 70)
    
    persona = ArtemisPersona()
    
    # Different contexts
    contexts = [
        {
            "query": "Explain the ATP protocol architecture",
            "atp_mode": "Review",
            "request_feedback": False
        },
        {
            "query": "How do I implement agent communication?",
            "atp_mode": "Build",
            "request_feedback": True
        }
    ]
    
    for i, context in enumerate(contexts, 1):
        print(f"\n--- Scenario {i} ---")
        print(f"Query: {context['query']}")
        
        # Format a response
        content = "The ATP protocol provides structured communication headers..."
        formatted = persona.format_response(content, context)
        
        print(f"\nResponse Mode: {persona.current_mode.value}")
        print(f"Verbose: {persona.should_be_verbose(context)}")
        print(f"\nFormatted Response:\n{formatted}")
    
    print("\n" + "-" * 70)
    print("\nPersonality Context for AI Systems:")
    print(persona.get_personality_context())
    
    print()


def demo_reflection_engine():
    """Demonstrate reflection and concept synthesis."""
    print("=" * 70)
    print("DEMO 4: Reflection Engine & Concept Synthesis")
    print("=" * 70)
    
    engine = ReflectionEngine()
    
    # Add conversations
    conversations = [
        "We're building an ATP protocol for structured communication between agents.",
        "The MemoryLayer needs to integrate with the ObsidianVault for knowledge storage.",
        "Artemis acts as the governance agent overseeing all system interactions.",
        "The ATP protocol includes Mode, Context, Priority, and ActionType headers.",
    ]
    
    print("\nAdding conversations...")
    for conv in conversations:
        engine.add_conversation(conv)
        print(f"  + {conv[:60]}...")
    
    print(f"\nStats: {engine.get_stats()}")
    
    # Synthesize
    print("\n" + "-" * 70)
    print("\nSynthesis:")
    print(engine.synthesize())
    
    # Find connections
    print("\n" + "-" * 70)
    print("\nConnections for 'ATP':")
    connections = engine.find_connections("ATP")
    for conn in connections:
        print(f"  ↔ {conn}")
    
    print()


def demo_semantic_tagging():
    """Demonstrate semantic tagging and citations."""
    print("=" * 70)
    print("DEMO 5: Semantic Tagging & Citations")
    print("=" * 70)
    
    tagger = SemanticTagger()
    
    # Tag some items
    print("\nTagging items...")
    tagger.tag_item("ATP Protocol", ["protocol", "communication", "architecture"], "concept")
    tagger.tag_item("agents/atp/atp_parser.py", ["atp", "parser", "python"], "file")
    tagger.tag_item("Artemis Agent", ["agent", "governance", "artemis"], "agent")
    tagger.tag_item("Memory Layer", ["memory", "storage", "architecture"], "concept")
    
    print(f"  Tagged 4 items across {len(tagger.tags)} unique tags")
    
    # Find by tag
    print("\n" + "-" * 70)
    print("\nItems tagged with 'architecture':")
    items = tagger.get_items_by_tag("architecture")
    for item in items:
        print(f"  - {item}")
    
    # Find related
    print("\n" + "-" * 70)
    print("\nItems related to 'ATP Protocol':")
    related = tagger.find_related_items("ATP Protocol")
    for item in related:
        print(f"  ↔ {item}")
    
    # Extract from text
    print("\n" + "-" * 70)
    print("\nExtracting tags and citations from text...")
    
    text = """
    The #ATP protocol is implemented in /agents/atp/atp_parser.py.
    @Artemis uses #semantic-tagging for knowledge organization.
    """
    
    tags = tagger.extract_tags_from_text(text)
    citations = tagger.extract_citations_from_text(text)
    
    print(f"\nExtracted {len(tags)} tags: {', '.join(tags)}")
    print(f"Extracted {len(citations)} citations:")
    for cit in citations:
        print(f"  - {cit.format()} ({cit.citation_type})")
    
    # Tag summary
    print("\n" + "-" * 70)
    print(tagger.generate_tag_summary())
    
    print(f"\nStats: {tagger.get_stats()}")
    
    print()


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "ARTEMIS PERSONA DEMO" + " " * 28 + "║")
    print("║" + " " * 15 + "Showcasing Core Features" + " " * 29 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    demos = [
        demo_atp_parsing,
        demo_instruction_loading,
        demo_artemis_persona,
        demo_reflection_engine,
        demo_semantic_tagging
    ]
    
    for demo_func in demos:
        try:
            demo_func()
            input("Press Enter to continue to next demo...")
            print("\n")
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user.")
            break
        except Exception as e:
            print(f"\n✗ Error in demo: {e}")
            import traceback
            traceback.print_exc()
            break
    
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("\nAll Artemis persona features demonstrated!")
    print("The system is ready for integration into your workflows.")
    print()


if __name__ == "__main__":
    main()
