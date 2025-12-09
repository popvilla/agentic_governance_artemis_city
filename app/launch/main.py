"""Artemis City CLI with ATP (Artemis Transmission Protocol) support.

This module provides the main command-line interface for the Artemis City
system. It integrates ATP message parsing for structured communication,
agent routing, instruction loading, and the Artemis persona system.

The CLI supports both single-command and interactive modes, parsing ATP
headers from user input to provide structured context for agent routing
and response generation.

Example ATP-formatted command:
    #Mode: Build #Context: CLI enhancement #ActionType: Execute
"""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml  # noqa: E402

from agents.artemis import ArtemisPersona  # noqa: E402
from agents.atp import ATPParser  # noqa: E402
from core.instructions import get_global_cache  # noqa: E402


def load_agent_router_config(config_path):
    """Load agent routing configurations from a specified YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        dict: Parsed configuration dictionary, or empty dict if file
            not found or parsing fails.
    """
    if not os.path.exists(config_path):
        print(f"Error: Agent router config not found at {config_path}")
        return {}
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def handle_command(command, agent_router, atp_parser, instruction_cache, artemis_persona):
    """Route a command to the appropriate agent with ATP parsing and instruction loading.

    Parses ATP headers from the command, loads relevant instructions,
    and routes to the appropriate agent based on keyword matching.
    Updates Artemis persona context when routing to the Artemis agent.

    Args:
        command: The command string to process, optionally with ATP headers.
        agent_router: Dictionary containing agent routing configuration.
        atp_parser: ATPParser instance for extracting ATP headers.
        instruction_cache: InstructionCache for loading agent instructions.
        artemis_persona: ArtemisPersona instance for context tracking.
    """
    # Parse ATP message
    atp_message = atp_parser.parse(command)

    # Show ATP info if headers present
    if atp_message.has_atp_headers:
        print("\n[ATP Protocol Detected]")
        print(f"  Mode: {atp_message.mode.value}")
        if atp_message.context:
            print(f"  Context: {atp_message.context}")
        if atp_message.priority.value != "Normal":
            print(f"  Priority: {atp_message.priority.value}")
        if atp_message.action_type.value != "Unknown":
            print(f"  Action: {atp_message.action_type.value}")
        if atp_message.target_zone:
            print(f"  Target: {atp_message.target_zone}")
        print()

    # Load instructions for current context
    instruction_set = instruction_cache.get(agent_name=None)

    if instruction_set.scopes:
        print(f"[Loaded {len(instruction_set.scopes)} instruction scope(s)]")
        for scope in instruction_set.scopes:
            print(f"  - {scope.level}: {scope.path}")
        print()

    # Determine command to process
    command_text = atp_message.content if atp_message.content else command

    print(f"Processing: '{command_text}'")

    # Route to agent
    routed = False
    for agent_name, config in agent_router.get('agents', {}).items():
        if any(keyword in command_text.lower() for keyword in config.get('keywords', [])):
            print(f"\n→ Routing to {agent_name} ({config.get('role', 'unknown role')}):")
            print(f"  Expected action: {config.get('action_description', 'processing...')}")
            routed = True

            # If routing to artemis, show persona context
            if agent_name == "artemis":
                artemis_persona.add_context_memory(command_text)
                print("\n[Artemis Context]")
                print(f"  Mode: {artemis_persona.current_mode.value}")
                recent_contexts = artemis_persona.get_recent_context(3)
                if recent_contexts:
                    print(f"  Recent interactions: {len(recent_contexts)}")

            break

    if not routed:
        print("\n→ No specific agent matched. Using general system processing.")


def main():
    """Initialize and run the Artemis City CLI with ATP support.

    Sets up the ATP parser, instruction cache, Artemis persona, and
    agent router. Supports single-command execution or interactive
    mode with ATP header parsing.

    Command-line Arguments:
        command: Optional single command to execute.
        --no-atp: Disable ATP parsing for commands.
        --project-root: Specify the project root directory for
            instruction loading.
    """
    parser = argparse.ArgumentParser(description="Agentic Codex CLI Interface with ATP Support")
    parser.add_argument(
        "command",
        nargs="?",
        help="The command to send to the Codex (e.g., 'status', 'ask artemis')",
    )
    parser.add_argument("--no-atp", action="store_true", help="Disable ATP parsing")
    parser.add_argument("--project-root", help="Specify project root directory")
    args = parser.parse_args()

    print("--- Artemis City CLI (ATP Enabled) ---")
    print("Type 'exit', 'quit', or press Ctrl+C to close.")
    print()

    # Initialize ATP parser
    atp_parser = ATPParser()

    # Initialize instruction cache
    instruction_cache = get_global_cache()

    # Initialize Artemis persona
    artemis_persona = ArtemisPersona()

    # Load agent router configuration
    script_dir = os.path.dirname(__file__)
    agent_router_path = os.path.join(script_dir, 'interface', 'agent_router.yaml')
    agent_router_config = load_agent_router_config(agent_router_path)

    # Show active instruction scopes
    project_root = args.project_root or os.path.dirname(script_dir)
    instruction_cache._loader.project_root = project_root
    active_scopes = instruction_cache._loader.get_active_scopes()
    if active_scopes:
        print("[Active Instruction Scopes]")
        for scope_path in active_scopes:
            print(f"  ✓ {scope_path}")
        print()

    if args.command:
        handle_command(
            args.command, agent_router_config, atp_parser, instruction_cache, artemis_persona
        )
    else:
        # Interactive mode
        print("Ready for commands. ATP headers supported: #Mode:, #Context:, etc.")
        print("Example: #Mode: Build #Context: CLI enhancement #ActionType: Execute")
        print()

        while True:
            try:
                user_input = input("artemis> ").strip()
                if user_input.lower() in ["exit", "quit"]:
                    print("\nExiting Artemis City CLI. Goodbye!")
                    break
                if not user_input:
                    continue

                print()  # Blank line for readability
                handle_command(
                    user_input, agent_router_config, atp_parser, instruction_cache, artemis_persona
                )
                print()  # Blank line after output

            except KeyboardInterrupt:
                print("\n\nExiting Artemis City CLI. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                import traceback

                traceback.print_exc()


if __name__ == "__main__":
    main()
