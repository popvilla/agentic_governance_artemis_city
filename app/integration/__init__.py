"""Memory integration bridge for Artemis City.

This module provides integration with the Artemis Agentic Memory Layer (MCP Server),
enabling agents to interact with Obsidian vault as a knowledge base.

The Postal Service provides a living city theme where agents send mail through
Pack Rat and store documents in the City Archives.
"""

from .context_loader import ContextEntry, ContextLoader
from .memory_client import MCPOperation, MCPResponse, MemoryClient
from .postal_service import MailPacket, PostOffice, get_post_office
from .trust_interface import TrustInterface, TrustLevel, TrustScore, get_trust_interface

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
