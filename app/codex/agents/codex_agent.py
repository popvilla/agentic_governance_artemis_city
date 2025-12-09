"""CodexAgent implementation for the Artemis City system.

This module provides the CodexAgent, the default general-purpose agent
that handles requests not specifically routed to other specialized agents.
It simulates LLM-based processing and logs interactions to memory.
"""

from codex.agents.base import Agent


class CodexAgent(Agent):
    """General-purpose agent for processing commands in Artemis City.

    The CodexAgent serves as the default handler for commands that
    are not specifically routed to other specialized agents. It
    processes requests and stores interactions in the memory bus
    for future reference.

    Inherits from:
        Agent: Abstract base class defining the agent interface.

    Example:
        >>> agent = CodexAgent("codex")
        >>> response = agent.handle({"content": "status"}, memory_bus)
    """

    def handle(self, request, memory):
        """Process a request and return a simulated LLM response.

        Extracts the content from the request, generates a simulated
        response, and stores the interaction in memory for audit
        and retrieval purposes.

        Args:
            request: Dictionary containing the request. Expected keys:
                - 'content': The command or message to process.
            memory: MemoryBus instance for storing the interaction.

        Returns:
            str: A formatted response indicating the request was processed.
        """
        content = request.get("content", "")

        # Simulate LLM call
        response = f"I am Codex. I processed your request: '{content}'. (LLM Simulation)"

        # Write to memory
        memory.write(response, metadata={"source": "CodexAgent", "trigger": content})

        return response
