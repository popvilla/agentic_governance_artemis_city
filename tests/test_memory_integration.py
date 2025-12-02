"""
Unit tests for Memory Integration layer.

Tests the MemoryClient, TrustInterface, and ContextLoader components.
"""

import pytest
from memory.integration import MemoryClient, TrustInterface, TrustScore, TrustLevel


class TestMemoryClient:
    """Test Memory Client functionality."""

    def test_memory_client_initialization(self):
        """Test that MemoryClient can be initialized."""
        client = MemoryClient(base_url="http://localhost:3000")
        assert client is not None
        assert client.base_url == "http://localhost:3000"

    def test_memory_client_default_url(self):
        """Test MemoryClient with default URL."""
        client = MemoryClient()
        assert client is not None
        # Should have a default URL
        assert hasattr(client, "base_url")


class TestTrustInterface:
    """Test Trust Interface functionality."""

    def test_trust_score_creation(self):
        """Test creating a trust score."""
        score = TrustScore(
            value=0.85,
            level=TrustLevel.HIGH,
            last_updated="2025-12-02T00:00:00Z"
        )
        assert score.value == 0.85
        assert score.level == TrustLevel.HIGH

    def test_trust_levels(self):
        """Test trust level enum values."""
        assert TrustLevel.LOW is not None
        assert TrustLevel.MEDIUM is not None
        assert TrustLevel.HIGH is not None
        assert TrustLevel.VERIFIED is not None

    def test_trust_interface_initialization(self):
        """Test that TrustInterface can be initialized."""
        interface = TrustInterface()
        assert interface is not None


class TestContextLoader:
    """Test Context Loader functionality."""

    def test_context_loader_initialization(self):
        """Test that ContextLoader can be initialized."""
        from memory.integration import ContextLoader
        loader = ContextLoader()
        assert loader is not None

    def test_load_empty_context(self):
        """Test loading empty context."""
        from memory.integration import ContextLoader
        loader = ContextLoader()
        # Should handle empty context gracefully
        result = loader.load_context([])
        assert result is not None or result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
