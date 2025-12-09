"""Agent routing system for the Artemis City framework.

This module provides keyword-based command routing to direct user
requests to the appropriate agent handlers. The routing configuration
is loaded from a YAML file that defines agents and their associated
keywords.

The AgentRouter supports flexible keyword matching using word boundaries
to ensure accurate routing without false positives from partial matches.
"""

import yaml
import os
import re
from pathlib import Path


class AgentRouter:
    """Routes commands to specific agents based on keyword configuration.

    The AgentRouter loads routing rules from a YAML configuration file
    and matches incoming commands against agent-specific keywords. When
    a match is found, the router returns the target agent name and
    associated metadata.

    Attributes:
        config_path: Path to the YAML configuration file.
        routes: Dictionary mapping agent names to their routing rules.
        config: Full parsed configuration from the YAML file.

    Example:
        >>> router = AgentRouter()
        >>> result = router.route("ask artemis about status")
        >>> print(result['agent'])  # 'artemis'
    """

    def __init__(self, config_path=None):
        """Initialize the AgentRouter with configuration.

        Args:
            config_path: Optional path to the agent router YAML file.
                If not provided, defaults to 'agent_router.yaml' in
                the same directory as this module.
        """
        if config_path is None:
             # Default to sibling file
             config_path = os.path.join(os.path.dirname(__file__), "agent_router.yaml")
        self.config_path = config_path
        self.routes = {}
        self.load_config()

    def load_config(self):
        """Load routing rules from the YAML configuration file.

        Reads and parses the YAML file specified by config_path,
        extracting agent routing rules. If the file doesn't exist
        or fails to parse, falls back to empty routes with a
        warning message.
        """
        if not os.path.exists(self.config_path):
            print(f"[Router] Config not found at {self.config_path}, using defaults.")
            self.routes = {}
            return

        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
                self.routes = self.config.get("agents", {})
        except Exception as e:
            print(f"[Router] Error loading config: {e}")
            self.routes = {}

    def route(self, command):
        """Determine the target agent for a command based on keywords.

        Matches the command against agent keywords using word boundary
        matching to find the appropriate handler. Returns the first
        matching agent or defaults to 'codex_daemon' if no match found.

        Args:
            command: The command string to route.

        Returns:
            dict: A dictionary containing:
                - 'agent': Name of the target agent
                - 'metadata': Agent configuration including role and
                    action description
        """
        command_lower = command.lower()
        
        for agent_name, rules in self.routes.items():
            keywords = rules.get("keywords", [])
            # Check for whole word matches
            if any(re.search(rf'\b{re.escape(k)}\b', command_lower) for k in keywords):
                return {
                    "agent": agent_name,
                    "metadata": rules
                }
        
        return {"agent": "codex_daemon", "metadata": {"role": "Default Handler", "action_description": "General processing"}}
