from codex.agents.base import Agent

class CodexAgent(Agent):
    def handle(self, request, memory):
        content = request.get("content", "")
        
        # Simulate LLM call
        response = f"I am Codex. I processed your request: '{content}'. (LLM Simulation)"
        
        # Write to memory
        memory.write(response, metadata={"source": "CodexAgent", "trigger": content})
        
        return response
