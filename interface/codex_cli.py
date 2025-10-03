import argparse
import yaml
import os

def load_agent_router_config(config_path):
    """Loads the agent router configuration from a YAML file.

    Args:
        config_path (str): The path to the agent router YAML configuration file.

    Returns:
        dict: A dictionary containing the agent router configuration, or an empty
              dictionary if the file is not found.
    """
    if not os.path.exists(config_path):
        print(f"Error: Agent router config not found at {config_path}")
        return {}
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def handle_command(command, agent_router):
    """Simulates handling a command by routing it to the appropriate agent.

    This function checks the command against a list of keywords defined for each
    agent in the router configuration. If a match is found, it prints routing
    information. Otherwise, it defaults to general system processing.

    Args:
        command (str): The command string to be processed.
        agent_router (dict): A dictionary containing agent configurations, where
                             each agent has keywords and a role description.
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
    """The main entry point for the Agentic Codex CLI.

    This function initializes the command-line interface, parses arguments, and
    enters a loop to accept user commands. It loads the agent router
    configuration and uses it to handle commands either from an initial
    argument or from interactive input.
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