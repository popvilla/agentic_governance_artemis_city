"""
Command-line interface for interacting with the Agentic Codex.

This module provides a CLI for routing commands to appropriate agents
based on keyword matching. It loads agent routing configurations from
YAML files and supports both single-command and interactive modes.

Follows JSF AV Rules 45-67 for naming conventions.

Module Dependencies:
    - argparse (standard library)
    - os (standard library)
    - re (standard library)
    - yaml (PyYAML)

Author: Artemis-City Contributors
Date: 2024
"""

from __future__ import annotations

import argparse
import os
import re
from typing import Any, Dict, List, Optional

import yaml

# Type alias for agent router configuration (JSF AV Rule 209)
AgentRouterConfig = Dict[str, Any]


def normalize_agent_router_config(
    config: Optional[AgentRouterConfig],
) -> AgentRouterConfig:
    """Normalize the agent router configuration for consistent processing.

    Ensures all agent keywords are lowercased strings, filtering out
    any non-string values. Creates empty dictionaries for missing
    or invalid configurations.

    Args:
        config: Raw configuration dictionary from YAML parsing.

    Returns:
        Normalized configuration with lowercased string keywords.
    """
    config = config or {}
    agents = config.get('agents', {})
    if not isinstance(agents, dict):
        agents = {}
    for _, agent in agents.items():
        if not isinstance(agent, dict):
            continue
        keywords = agent.get('keywords', [])
        # Keep only string keywords and normalize to lowercase
        agent['keywords'] = [k.lower() for k in keywords if isinstance(k, str)]
    config['agents'] = agents
    return config


def validate_agent_router_config(config: Any) -> AgentRouterConfig:
    """Validate the basic shape of the agent router configuration.

    Checks that the configuration is a dictionary containing an 'agents'
    key with a dictionary value. Logs warnings for invalid configurations.

    Args:
        config: Configuration value to validate (may be any type from YAML).

    Returns:
        The validated configuration, or a default empty configuration
        if validation fails.
    """
    if not isinstance(config, dict):
        print("[Warning] agent_router.yaml did not parse to a dictionary. Using empty config.")
        return {'agents': {}}
    if 'agents' not in config or not isinstance(config['agents'], dict):
        print("[Warning] agent_router.yaml is missing an 'agents' dictionary. Using empty config.")
        return {'agents': {}}
    return config


def load_agent_router_config(config_path: str) -> AgentRouterConfig:
    """Load agent routing configurations from a specified YAML file.

    Reads, validates, and normalizes the agent router configuration
    from the specified path. Returns an empty configuration if the
    file doesn't exist or fails to parse.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Validated and normalized configuration dictionary with
        an 'agents' key containing agent routing rules.
    """
    if not os.path.exists(config_path):
        print(f"[Error] Agent router config not found at {config_path}")
        return {'agents': {}}
    try:
        with open(config_path, 'r', encoding='utf-8') as file_handle:
            raw_config = yaml.safe_load(file_handle) or {}
    except yaml.YAMLError as yaml_error:
        print(f"[Error] Failed to parse agent router config: {yaml_error}")
        return {'agents': {}}
    except OSError as os_error:
        print(f"[Error] Failed to read agent router config: {os_error}")
        return {'agents': {}}
    validated_config = validate_agent_router_config(raw_config)
    return normalize_agent_router_config(validated_config)


def matches_command(command_lower: str, keywords: List[str]) -> bool:
    """Check if any keyword matches as a whole word/phrase in the command.

    Uses word boundary regex matching to avoid false positives from
    partial matches (e.g., 'art' matching 'artemis').

    Args:
        command_lower: Lowercased command string to check.
        keywords: List of keywords to match against.

    Returns:
        True if any keyword matches as a complete word in the command.
    """
    return any(re.search(rf'\b{re.escape(keyword)}\b', command_lower) for keyword in keywords)


def handle_command(command: str, agent_router: AgentRouterConfig) -> None:
    """Route a command to the appropriate agent based on predefined keywords.

    Matches the command against all configured agents' keywords and
    routes to the first matching agent. Prints routing information
    and expected actions.

    Args:
        command: The command string to route.
        agent_router: Dictionary containing agent routing configuration
            with an 'agents' key.
    """
    print(f"[CLI] Received command: '{command}'")
    command_lower = command.lower()
    for agent_name, agent_config in agent_router.get('agents', {}).items():
        keywords = agent_config.get('keywords', [])
        if matches_command(command_lower, keywords):
            role = agent_config.get('role', 'unknown role')
            action = agent_config.get('action_description', 'processing...')
            print(f"[Router] Routing to {agent_name} ({role}):")
            print(f"  - Input: '{command}'")
            print(f"  - Expected action: {action}")
            return
    print(
        "[Router] No specific agent found for this command. "
        "Defaulting to general system processing."
    )


def main() -> None:
    """Initialize and run the Agentic Codex Command-Line Interface.

    Sets up argument parsing, loads agent router configuration, and
    either processes a single command or enters interactive mode.
    In interactive mode, accepts commands until 'exit' or 'quit'
    is entered.

    Command-line Arguments:
        command: Optional single command to execute.
        --config: Optional path to custom agent router YAML file.
    """
    parser = argparse.ArgumentParser(description="Agentic Codex CLI Interface")
    parser.add_argument(
        "command",
        nargs="?",
        help="The command to send to the Codex (e.g., 'status', 'ask artemis')",
    )
    parser.add_argument(
        "--config",
        help="Path to agent router YAML configuration",
        default=None,
    )
    args = parser.parse_args()

    print("--- Agentic Codex CLI ---")
    print("Type 'exit' or 'quit' to close.")

    # Load agent router configuration
    script_directory = os.path.dirname(__file__)
    default_config_path = os.path.join(script_directory, 'agent_router.yaml')
    config_path = args.config or default_config_path
    print(f"[CLI] Using agent router config: {config_path}")
    router_config = load_agent_router_config(config_path)

    if args.command:
        handle_command(args.command, router_config)
    else:
        _run_interactive_loop(router_config)


def _run_interactive_loop(router_config: AgentRouterConfig) -> None:
    """
    Run the interactive command input loop.

    Continuously prompts for user input and routes commands until
    the user exits or an interrupt is received.

    Args:
        router_config: Loaded agent router configuration.
    """
    while True:
        try:
            user_input = input("codex> ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting Codex CLI. Goodbye!")
                break
            if not user_input:
                continue
            handle_command(user_input, router_config)
        except KeyboardInterrupt:
            print("\nExiting Codex CLI. Goodbye!")
            break
        except EOFError:
            print("\nExiting Codex CLI. Goodbye!")
            break


if __name__ == "__main__":
    main()
