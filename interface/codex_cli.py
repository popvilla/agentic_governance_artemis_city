import argparse
import yaml
import os

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

def handle_command(command, agent_router):
    """Routes a command to the appropriate agent based on predefined keywords.

    This function simulates routing by matching keywords in the command string
    against the patterns defined in the agent router configuration. If a keyword
    match is found, it prints the details of the agent that would handle the
    command. If no agent matches, it defaults to a general system response.

    Args:
        command (str): The user-provided command string to be processed.
        agent_router (dict): The configuration dictionary that maps agents to
                             keywords and roles.
    """
    print(f"CLI received command: '{command}'")
    routed = False
    for agent_name, config in agent_router.get('agents', {}).items():
        if any(keyword in command.lower() for keyword in config.get('keywords', [])):
            print(f"Routing command to {agent_name} ({config.get('role', 'unknown role')}):")
            print(f"  - Input: '{command}'")
            print(f"  - Expected action: {config.get('action_description', 'processing...')}")
            routed = True
            break
    if not routed:
        print("No specific agent found for this command. Defaulting to general system processing.")

def main():
    """Initializes and runs the Agentic Codex Command-Line Interface (CLI).

    This function serves as the main entry point for the application. It sets
    up an argument parser to handle commands passed at startup and enters an
    interactive loop to accept commands from the user. It loads the agent
    router configuration to correctly handle command routing.
    """
    parser = argparse.ArgumentParser(description="Agentic Codex CLI Interface")
    parser.add_argument("command", nargs="?", help="The command to send to the Codex (e.g., 'status', 'ask artemis')")
    args = parser.parse_args()

    print("--- Agentic Codex CLI ---")
    print("Type 'exit' or 'quit' to close.")

    # Load agent router configuration
    script_dir = os.path.dirname(__file__)
    agent_router_path = os.path.join(script_dir, 'agent_router.yaml')
    agent_router_config = load_agent_router_config(agent_router_path)

    if args.command:
        handle_command(args.command, agent_router_config)
    else:
        while True:
            try:
                user_input = input("codex> ").strip()
                if user_input.lower() in ["exit", "quit"]:
                    print("Exiting Codex CLI. Goodbye!")
                    break
                if not user_input:
                    continue
                handle_command(user_input, agent_router_config)
            except KeyboardInterrupt:
                print("\nExiting Codex CLI. Goodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()