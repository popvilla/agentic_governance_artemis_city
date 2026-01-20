"""Artemis City MCP (Model Context Protocol) Module.

This module provides vector storage and semantic search capabilities
for the Artemis agentic memory system using Supabase pgvector.

Components:
- VectorStore: High-level semantic storage interface
- VectorDocument: Document with embedding and metadata
- HebbianVectorStore: ATP-integrated retrieval with Hebbian weights
- VectorMemoryBackend: MemoryBus adapter for semantic search

Example:
    from MCP.src.vector_store import VectorStore

    store = VectorStore()
    doc_id = store.store("Agent memory content", {"agent": "artemis"})
    results = store.search("governance policy")
"""

from .vector_store import (
    VectorStore,
    VectorDocument,
    HebbianVectorStore,
    VectorMemoryBackend,
    OpenAIEmbedding,
    SupabaseVectorBackend,
    get_setup_sql,
)

__all__ = [
    "VectorStore",
    "VectorDocument",
    "HebbianVectorStore",
    "VectorMemoryBackend",
    "OpenAIEmbedding",
    "SupabaseVectorBackend",
    "get_setup_sql",
]

__version__ = "0.1.0"
