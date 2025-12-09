import json
import os
from pathlib import Path
from codex.agent_router import AgentRouter
from codex.memory_bus import MemoryBus
from codex.agents.codex_agent import CodexAgent
from codex.agents.planner_agent import PlannerAgent

STATE_FILE = "state_kernel.json"

class Kernel:
    """
    Artemis-City Core Kernel.
    Orchestrates command processing, routing, and agent execution.
    """
    
    def __init__(self):
        self.booted = False
        self.state = {}
        self.router = None
        self.memory = None
        self.boot()

    def boot(self):
        """Initialize kernel subsystems: Router, Memory, Agents."""
        self._load_state()
        self.router = AgentRouter()
        self.memory = MemoryBus()
        self.booted = True
    
    def _load_state(self):
        """Load the kernel state from disk."""
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r') as f:
                    self.state = json.load(f)
            except Exception as e:
                print(f"[Kernel] Failed to load state: {e}")
                self.state = {"history": [], "boot_count": 0}
        else:
            self.state = {"history": [], "boot_count": 0}
        
        self.state["boot_count"] = self.state.get("boot_count", 0) + 1
        self._save_state()

    def _save_state(self):
        """Save the kernel state to disk."""
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"[Kernel] Failed to save state: {e}")

    def process(self, request):
        """
        Main execution entry point.
        
        Args:
            request (dict): A structured request object (e.g. {'type': 'command', 'content': '...'})
            
        Returns:
            str: The result of the execution.
        """
        content = request.get("content", "")
        request_type = request.get("type", "command")
        
        # Log to history
        if "history" not in self.state:
            self.state["history"] = []
        self.state["history"].append(request)
        self._save_state()
        
        if request_type == "command":
             return self._handle_command(content)
        elif request_type == "exec":
             return f"[Kernel] Executing plan: {request.get('path')}"
        
        return f"[Kernel] Unknown request type: {request_type}"

    def _get_agent_instance(self, agent_name):
        # Simple factory for now
        if agent_name == "planner":
            return PlannerAgent(agent_name)
        elif agent_name == "codex_daemon" or agent_name == "codex":
            return CodexAgent(agent_name)
        # Fallback
        return CodexAgent("generic")

    def _handle_command(self, command):
        if not self.router:
            return "[Kernel] Router not initialized."
            
        route = self.router.route(command)
        agent_name = route.get("agent")
        # metadata = route.get("metadata", {})
        
        agent = self._get_agent_instance(agent_name)
        
        request = {"content": command, "type": "command"}
        result = agent.handle(request, self.memory)
        
        return f"[Kernel] {agent_name} responded:\n{result}"
