"""Memory integration bridge for Artemis City.

This module provides integration with the Artemis Agentic Memory Layer (MCP Server),
enabling agents to interact with Obsidian vault as a knowledge base.

The Postal Service provides a living city theme where agents send mail through
Pack Rat and store documents in the City Archives.
"""

from .memory_client import MemoryClient, MCPResponse, MCPOperation
from .trust_interface import TrustInterface, TrustScore, TrustLevel, get_trust_interface
from .context_loader import ContextLoader, ContextEntry
from .postal_service import PostOffice, MailPacket, get_post_office

__all__ = [
    # Core memory components
    'MemoryClient',
    'MCPResponse',
    'MCPOperation',
    'TrustInterface',
    'TrustScore',
    'TrustLevel',
    'get_trust_interface',
    'ContextLoader',
    'ContextEntry',
    # Living city theme
    'PostOffice',
    'MailPacket',
    'get_post_office',
]
