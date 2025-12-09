"""
Unit tests for Memory Integration layer.

Tests the MemoryClient, TrustInterface, and ContextLoader components.
"""

import os
from datetime import datetime

import pytest

from integration import MemoryClient, TrustInterface, TrustLevel, TrustScore


class TestMemoryClient:
    """Test Memory Client functionality."""

    def test_memory_client_initialization(self):
        """Test that MemoryClient can be initialized."""
        # Set API key in environment for test
        os.environ['MCP_API_KEY'] = 'test-api-key'  # pragma: allowlist secret
        client = MemoryClient(base_url="http://localhost:3000")
        assert client is not None
        assert client.base_url == "http://localhost:3000"

    def test_memory_client_default_url(self):
        """Test MemoryClient with default URL."""
        # Set API key in environment for test
        os.environ['MCP_API_KEY'] = 'test-api-key'  # pragma: allowlist secret
        client = MemoryClient()
        assert client is not None
        # Should have a default URL
        assert hasattr(client, "base_url")


class TestTrustInterface:
    """Test Trust Interface functionality."""

    def test_trust_score_creation(self):
        """Test creating a trust score."""
        score = TrustScore(
            entity_id="test-entity",
            entity_type="agent",
            score=0.85,
            level=TrustLevel.HIGH,
            last_updated=datetime.now(),
        )
        assert score.score == 0.85
        assert score.level == TrustLevel.HIGH
        assert score.entity_id == "test-entity"

    def test_trust_levels(self):
        """Test trust level enum values."""
        assert TrustLevel.LOW is not None
        assert TrustLevel.MEDIUM is not None
        assert TrustLevel.HIGH is not None
        assert TrustLevel.FULL is not None
        assert TrustLevel.UNTRUSTED is not None

    def test_trust_interface_initialization(self):
        """Test that TrustInterface can be initialized."""
        interface = TrustInterface()
        assert interface is not None


class TestContextLoader:
    """Test Context Loader functionality."""

    def test_context_loader_initialization(self):
        """Test that ContextLoader can be initialized."""
        from integration import ContextLoader

        # Set API key for MemoryClient initialization
        os.environ['MCP_API_KEY'] = 'test-api-key'  # pragma: allowlist secret
        loader = ContextLoader()
        assert loader is not None

    def test_load_empty_context(self):
        """Test loading empty folder context."""
        from integration import ContextLoader

        # Set API key for MemoryClient initialization
        os.environ['MCP_API_KEY'] = 'test-api-key'  # pragma: allowlist secret
        loader = ContextLoader()
        # Should handle empty folder context gracefully
        # Test loading context from empty folder (won't actually hit server in unit test)
        # Just verify the method exists and can be called
        assert hasattr(loader, 'load_folder_context')
        assert hasattr(loader, 'search_context')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
