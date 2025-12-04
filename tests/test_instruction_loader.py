"""
Unit tests for Instruction Loader.

Tests the InstructionLoader and InstructionCache components.
"""

import os

import pytest

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
        # Try to load instructions with agent name
        instructions = loader.load(current_dir=os.getcwd(), agent_name="artemis")
        assert instructions is not None
        assert isinstance(instructions, InstructionSet)

    def test_load_nonexistent_agent(self):
        """Test loading instructions for non-existent agent."""
        loader = InstructionLoader()
        # Load with non-existent agent (should still return InstructionSet)
        instructions = loader.load(current_dir=os.getcwd(), agent_name="nonexistent-agent-12345")
        assert instructions is not None
        assert isinstance(instructions, InstructionSet)


class TestInstructionSet:
    """Test InstructionSet data structure."""

    def test_instruction_set_creation(self):
        """Test creating an instruction set."""
        from core.instructions import InstructionScope

        scope = InstructionScope(
            level="test", path="/test/path.md", content="Test instructions", priority=1
        )
        instruction_set = InstructionSet(scopes=[scope])
        assert len(instruction_set.scopes) == 1
        assert instruction_set.scopes[0].level == "test"

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
        """Test cache auto-population on get."""
        import tempfile

        from core.instructions import InstructionCache

        cache = InstructionCache()

        # Use a temporary directory that exists
        with tempfile.TemporaryDirectory() as tmpdir:
            # First get populates cache
            result1 = cache.get(current_dir=tmpdir, agent_name="test")
            assert result1 is not None
            assert isinstance(result1, InstructionSet)

            # Second get should hit cache
            result2 = cache.get(current_dir=tmpdir, agent_name="test")
            assert result2 is result1  # Should be same object from cache

    def test_cache_miss(self):
        """Test cache behavior with different keys."""
        import tempfile

        from core.instructions import InstructionCache

        cache = InstructionCache()

        # Use a temporary directory that exists
        with tempfile.TemporaryDirectory() as tmpdir:
            # Get with one agent name
            result1 = cache.get(current_dir=tmpdir, agent_name="agent1")
            # Get with different agent name should load new set
            result2 = cache.get(current_dir=tmpdir, agent_name="agent2")
            # Both should return InstructionSet instances
            assert result1 is not None
            assert result2 is not None
            assert isinstance(result1, InstructionSet)
            assert isinstance(result2, InstructionSet)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
