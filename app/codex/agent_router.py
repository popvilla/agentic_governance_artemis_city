import yaml
import os
import re
from pathlib import Path

class AgentRouter:
    """
    Routes commands to specific agents based on configuration rules.
    """
    
    def __init__(self, config_path=None):
        if config_path is None:
             # Default to sibling file
             config_path = os.path.join(os.path.dirname(__file__), "agent_router.yaml")
        self.config_path = config_path
        self.routes = {}
        self.load_config()

    def load_config(self):
        """Load routing rules from YAML."""
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
        """
        Determine the target agent for a command.
        
        Returns:
            dict: {'agent': 'agent_name', 'metadata': {...}}
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
