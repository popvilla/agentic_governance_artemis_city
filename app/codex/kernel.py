"""Artemis City Core Kernel.

This module implements the central kernel for the Artemis City system,
responsible for orchestrating command processing, agent routing, and
memory management. The kernel acts as the primary coordinator for all
agent interactions within the system.

The kernel maintains persistent state across sessions and provides the
main entry point for processing user requests through its agent network.
"""

import json
import os

from codex.agent_router import AgentRouter
from codex.agents.codex_agent import CodexAgent
from codex.agents.planner_agent import PlannerAgent
from codex.memory_bus import MemoryBus

STATE_FILE = "state_kernel.json"


class Kernel:
    """Artemis City Core Kernel for orchestrating agent operations.

    The Kernel is the central coordinator of the Artemis City system,
    managing command routing, agent instantiation, and persistent state.
    It initializes and coordinates all subsystems including the AgentRouter
    for command routing, MemoryBus for persistent memory operations, and
    individual agent instances.

    Attributes:
        booted: Boolean indicating whether the kernel has completed initialization.
        state: Dictionary containing kernel state including command history
            and boot count.
        router: AgentRouter instance for routing commands to appropriate agents.
        memory: MemoryBus instance for persistent memory operations.

    Example:
        >>> kernel = Kernel()
        >>> result = kernel.process({"type": "command", "content": "status"})
        >>> print(result)
    """

    def __init__(self):
        """Initialize the Kernel and boot all subsystems.

        Creates a new Kernel instance and immediately boots all subsystems
        including the agent router and memory bus. State is loaded from
        disk if available, or initialized with defaults.
        """
        self.booted = False
        self.state = {}
        self.router = None
        self.memory = None
        self.boot()

    def boot(self):
        """Initialize kernel subsystems: Router, Memory, and Agents.

        Loads persistent state from disk, initializes the AgentRouter
        for command routing, and creates the MemoryBus for memory
        operations. Sets the booted flag to True upon completion.
        """
        self._load_state()
        self.router = AgentRouter()
        self.memory = MemoryBus()
        self.booted = True

    def _load_state(self):
        """Load the kernel state from disk.

        Attempts to load previously saved kernel state from STATE_FILE.
        If the file doesn't exist or fails to load, initializes with
        default state containing empty history and zero boot count.
        Increments boot_count and saves state on each load.
        """
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
        """Save the kernel state to disk.

        Persists the current kernel state to STATE_FILE in JSON format.
        Logs an error message if the save operation fails.
        """
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"[Kernel] Failed to save state: {e}")

    def process(self, request):
        """Main execution entry point for processing requests.

        Routes incoming requests to appropriate handlers based on request
        type. Logs all requests to the state history for auditability.

        Args:
            request: A dictionary containing the request details.
                Expected keys:
                - 'type': Request type ('command' or 'exec')
                - 'content': Command content (for 'command' type)
                - 'path': Plan file path (for 'exec' type)

        Returns:
            str: The result message from processing the request,
                including the agent response or error message.
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
        """Create and return an agent instance based on agent name.

        Factory method that instantiates the appropriate agent class
        based on the provided agent name. Falls back to a generic
        CodexAgent if the agent name is not recognized.

        Args:
            agent_name: Name of the agent to instantiate. Supported values:
                - 'planner': Returns PlannerAgent
                - 'codex_daemon' or 'codex': Returns CodexAgent
                - Other: Returns generic CodexAgent

        Returns:
            Agent: An instance of the appropriate Agent subclass.
        """
        if agent_name == "planner":
            return PlannerAgent(agent_name)
        elif agent_name == "codex_daemon" or agent_name == "codex":
            return CodexAgent(agent_name)
        return CodexAgent("generic")

    def _handle_command(self, command):
        """Handle a command by routing to the appropriate agent.

        Uses the AgentRouter to determine which agent should handle
        the command, instantiates the agent, and delegates execution.

        Args:
            command: The command string to process.

        Returns:
            str: The formatted response from the handling agent,
                or an error message if the router is not initialized.
        """
        if not self.router:
            return "[Kernel] Router not initialized."

        route = self.router.route(command)
        agent_name = route.get("agent")
        # metadata = route.get("metadata", {})

        agent = self._get_agent_instance(agent_name)

        request = {"content": command, "type": "command"}
        result = agent.handle(request, self.memory)

        return f"[Kernel] {agent_name} responded:\n{result}"
