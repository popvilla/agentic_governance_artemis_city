"This module provides a command-line interface for interacting with the Agentic Codex."
import argparse
import os
import re

import yaml


def normalize_agent_router_config(cfg):
    """Normalize the agent router configuration."""
    cfg = cfg or {}
    agents = cfg.get('agents', {})
    if not isinstance(agents, dict):
        agents = {}
    for _, agent in agents.items():
        if not isinstance(agent, dict):
            continue
        kws = agent.get('keywords', [])
        # Keep only string keywords and normalize to lowercase
        agent['keywords'] = [k.lower() for k in kws if isinstance(k, str)]
    cfg['agents'] = agents
    return cfg


def validate_agent_router_config(cfg):
    """Validate the basic shape of the agent router configuration."""
    if not isinstance(cfg, dict):
        print("[Warning] agent_router.yaml did not parse to a dictionary. Using empty config.")
        return {'agents': {}}
    if 'agents' not in cfg or not isinstance(cfg['agents'], dict):
        print("[Warning] agent_router.yaml is missing an 'agents' dictionary. Using empty config.")
        return {'agents': {}}
    return cfg


def load_agent_router_config(config_path):
    """Load agent routing configurations from a specified YAML file."""
    if not os.path.exists(config_path):
        print(f"[Error] Agent router config not found at {config_path}")
        return {'agents': {}}
    try:
        with open(config_path, 'r') as f:
            raw = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"[Error] Failed to read agent router config: {e}")
        return {'agents': {}}
    cfg = validate_agent_router_config(raw)
    return normalize_agent_router_config(cfg)


def matches_command(command_lower, keywords):
    """Return True if any keyword matches as a whole word/phrase in the command."""
    return any(re.search(rf'\b{re.escape(k)}\b', command_lower) for k in keywords)


def handle_command(command, agent_router):
    """Route a command to the appropriate agent based on predefined keywords."""
    print(f"[CLI] Received command: '{command}'")
    command_lower = command.lower()
    for agent_name, config in agent_router.get('agents', {}).items():
        keywords = config.get('keywords', [])
        if matches_command(command_lower, keywords):
            print(f"[Router] Routing to {agent_name} ({config.get('role', 'unknown role')}):")
            print(f"  - Input: '{command}'")
            print(f"  - Expected action: {config.get('action_description', 'processing...')}")
            return
    print(
        "[Router] No specific agent found for this command. "
        "Defaulting to general system processing."
    )


def main():
    """Initialize and run the Agentic Codex Command-Line Interface (CLI)."""
    parser = argparse.ArgumentParser(description="Agentic Codex CLI Interface")
    parser.add_argument(
        "command",
        nargs="?",
        help="The command to send to the Codex (e.g., 'status', 'ask artemis')",
    )
    parser.add_argument("--config", help="Path to agent router YAML", default=None)
    args = parser.parse_args()

    print("--- Agentic Codex CLI ---")
    print("Type 'exit' or 'quit' to close.")

    # Load agent router configuration
    script_dir = os.path.dirname(__file__)
    default_agent_router_path = os.path.join(script_dir, 'agent_router.yaml')
    agent_router_path = args.config or default_agent_router_path
    print(f"[CLI] Using agent router config: {agent_router_path}")
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
                print(f"[Error] An error occurred: {e}")


if __name__ == "__main__":
    main()