"""PlannerAgent implementation for task planning in Artemis City.

This module provides the PlannerAgent, a specialized agent responsible
for breaking down complex requests into actionable plans. It generates
structured task plans and stores them in the memory system.
"""

from codex.agents.base import Agent


class PlannerAgent(Agent):
    """Specialized agent for generating task plans.

    The PlannerAgent analyzes incoming requests and generates
    structured plans with discrete steps. Plans are stored in
    memory for execution tracking and reference.

    Inherits from:
        Agent: Abstract base class defining the agent interface.

    Example:
        >>> planner = PlannerAgent("planner")
        >>> plan = planner.handle({"content": "refactor module"}, memory)
    """

    def handle(self, request, memory):
        """Generate a structured plan for the requested task.

        Creates a simple three-step plan (Analyze, Execute, Verify)
        for the given request and stores it in memory.

        Args:
            request: Dictionary containing the request. Expected keys:
                - 'content': Description of the task to plan.
            memory: MemoryBus instance for storing the generated plan.

        Returns:
            str: A formatted plan string with numbered steps.
        """
        content = request.get("content", "")
        plan = f"Plan for '{content}':\n1. Analyze\n2. Execute\n3. Verify"

        memory.write(plan, metadata={"source": "PlannerAgent", "type": "plan"})

        return plan
