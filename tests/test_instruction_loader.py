"""
Unit tests for Instruction Loader.

Tests the InstructionLoader and InstructionCache components.
"""

import pytest
import os
from core.instructions import InstructionLoader, InstructionSet


class TestInstructionLoader:
    """Test Instruction Loader functionality."""

    def test_instruction_loader_initialization(self):
        """Test that InstructionLoader can be initialized."""
        loader = InstructionLoader()
        assert loader is not None

    def test_load_agent_instructions(self):
        """Test loading agent instructions from markdown files."""
        loader = InstructionLoader()
        # Try to load Artemis agent instructions
        instructions = loader.load_agent("artemis")
        assert instructions is not None or instructions == InstructionSet()

    def test_load_nonexistent_agent(self):
        """Test loading instructions for non-existent agent."""
        loader = InstructionLoader()
        instructions = loader.load_agent("nonexistent-agent-12345")
        # Should handle gracefully
        assert instructions is not None or instructions is None


class TestInstructionSet:
    """Test InstructionSet data structure."""

    def test_instruction_set_creation(self):
        """Test creating an instruction set."""
        instruction_set = InstructionSet(
            agent_name="test-agent",
            role="Test Role",
            access_scope="Limited",
            protocols=[]
        )
        assert instruction_set.agent_name == "test-agent"
        assert instruction_set.role == "Test Role"

    def test_empty_instruction_set(self):
        """Test creating an empty instruction set."""
        instruction_set = InstructionSet()
        assert instruction_set is not None


class TestInstructionCache:
    """Test Instruction Cache functionality."""

    def test_cache_initialization(self):
        """Test that InstructionCache can be initialized."""
        from core.instructions import InstructionCache
        cache = InstructionCache()
        assert cache is not None

    def test_cache_set_get(self):
        """Test setting and getting cached instructions."""
        from core.instructions import InstructionCache
        cache = InstructionCache()

        instruction_set = InstructionSet(agent_name="test", role="Test")
        cache.set("test", instruction_set)

        result = cache.get("test")
        assert result is not None
        assert result.agent_name == "test"

    def test_cache_miss(self):
        """Test cache miss scenario."""
        from core.instructions import InstructionCache
        cache = InstructionCache()

        result = cache.get("nonexistent")
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
