from codex.agents.base import Agent

class PlannerAgent(Agent):
    def handle(self, request, memory):
        content = request.get("content", "")
        plan = f"Plan for '{content}':\n1. Analyze\n2. Execute\n3. Verify"
        
        memory.write(plan, metadata={"source": "PlannerAgent", "type": "plan"})
        
        return plan
