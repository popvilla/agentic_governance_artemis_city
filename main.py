import argparse
import yaml
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.atp import ATPParser, ATPValidator
from core.instructions import get_global_cache
from agents.artemis import ArtemisPersona

def load_agent_router_config(config_path):
    """Loads agent routing configurations from a specified YAML file.

    This function reads a YAML file that defines the routing logic for different
    agents based on command keywords. It's designed to fail gracefully by
    returning an empty dictionary if the file doesn't exist.

    Args:
        config_path (str): The full path to the agent router YAML config file.

    Returns:
        dict: A dictionary containing the agent router configuration. Returns an
              empty dictionary if the configuration file cannot be found.
    """
    if not os.path.exists(config_path):
        print(f"Error: Agent router config not found at {config_path}")
        return {}
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def handle_command(command, agent_router, atp_parser, instruction_cache, artemis_persona):
    """Routes a command to the appropriate agent with ATP parsing and instruction loading.

    This function:
    1. Parses ATP headers from the command
    2. Loads relevant instructions for the current context
    3. Routes to the appropriate agent
    4. Formats response with Artemis personality if applicable

    Args:
        command (str): The user-provided command string to be processed.
        agent_router (dict): The configuration dictionary that maps agents to keywords and roles.
        atp_parser (ATPParser): ATP parser instance
        instruction_cache: Instruction cache instance
        artemis_persona (ArtemisPersona): Artemis persona instance
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
    current_agent = None
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
            current_agent = agent_name
            print(f"\n→ Routing to {agent_name} ({config.get('role', 'unknown role')}):")
            print(f"  Expected action: {config.get('action_description', 'processing...')}")
            routed = True
            
            # If routing to artemis, show persona context
            if agent_name == "artemis":
                artemis_persona.add_context_memory(command_text)
                print(f"\n[Artemis Context]")
                print(f"  Mode: {artemis_persona.current_mode.value}")
                recent_contexts = artemis_persona.get_recent_context(3)
                if recent_contexts:
                    print(f"  Recent interactions: {len(recent_contexts)}")
            
            break
    
    if not routed:
        print("\n→ No specific agent matched. Using general system processing.")

def main():
    """Initializes and runs the Agentic Codex Command-Line Interface (CLI).

    This function serves as the main entry point for the application with
    enhanced ATP protocol support, instruction loading, and Artemis persona.
    """
    parser = argparse.ArgumentParser(description="Agentic Codex CLI Interface with ATP Support")
    parser.add_argument("command", nargs="?", help="The command to send to the Codex (e.g., 'status', 'ask artemis')")
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
            args.command, 
            agent_router_config, 
            atp_parser,
            instruction_cache,
            artemis_persona
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
                    user_input,
                    agent_router_config,
                    atp_parser,
                    instruction_cache,
                    artemis_persona
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