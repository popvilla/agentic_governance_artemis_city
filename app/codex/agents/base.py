"""Base agent class for the Artemis City agent framework.

This module defines the abstract base class that all agents in the
Artemis City system must inherit from. It establishes the standard
interface for agent initialization and request handling.
"""

from abc import ABC, abstractmethod


class Agent(ABC):
    """Abstract base class for all Artemis City agents.

    Defines the standard interface that all agents must implement,
    ensuring consistent initialization and request handling across
    the agent system.

    Attributes:
        name: The unique identifier name for this agent instance.
        config: Configuration dictionary for agent-specific settings.

    Example:
        >>> class MyAgent(Agent):
        ...     def handle(self, request, memory):
        ...         return f"Processed: {request['content']}"
        >>> agent = MyAgent("my_agent")
    """

    def __init__(self, name, config=None):
        """Initialize the agent with a name and optional configuration.

        Args:
            name: Unique identifier for this agent instance.
            config: Optional dictionary of agent configuration settings.
                Defaults to empty dictionary if not provided.
        """
        self.name = name
        self.config = config or {}

    @abstractmethod
    def handle(self, request, memory):
        """Handle an incoming request and return a response.

        This method must be implemented by all concrete agent subclasses.
        It processes the incoming request using the provided memory bus
        for any necessary memory operations.

        Args:
            request: Dictionary containing the request details.
                Expected to have at minimum a 'content' key with the
                command or message to process.
            memory: MemoryBus instance for reading/writing memory
                during request processing.

        Returns:
            str: The response content after processing the request.
        """
        pass
