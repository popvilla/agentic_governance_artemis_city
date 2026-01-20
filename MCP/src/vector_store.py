"""Vector Store for Artemis City using Supabase pgvector.

This module provides semantic search capabilities for the Artemis memory system
using Supabase's pgvector extension. It enables agents to store and retrieve
information based on semantic similarity rather than just keyword matching.

Integrates with the existing MemoryBus architecture as a pluggable backend.
"""

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from abc import ABC, abstractmethod

# Optional imports - gracefully handle if not installed
try:
    from openai import OpenAI  # type: ignore
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from supabase import create_client, Client  # type: ignore
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False


@dataclass
class VectorDocument:
    """A document with its vector embedding and metadata.

    Attributes:
        id: Unique identifier for the document
        content: The text content of the document
        embedding: Vector embedding of the content
        metadata: Additional metadata (agent, tags, timestamp, etc.)
        similarity: Similarity score (populated during search)
    """
    id: Optional[str] = None
    content: str = ""
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    similarity: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "id": self.id,
            "content": self.content,
            "embedding": self.embedding,
            "metadata": self.metadata,
            "similarity": self.similarity
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VectorDocument':
        """Create from dictionary."""
        return cls(
            id=data.get("id"),
            content=data.get("content", ""),
            embedding=data.get("embedding"),
            metadata=data.get("metadata", {}),
            similarity=data.get("similarity")
        )


class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate embedding for text."""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the embedding dimension."""
        pass


class OpenAIEmbedding(EmbeddingProvider):
    """OpenAI embedding provider using text-embedding-3-small.

    Attributes:
        model: The embedding model to use
        client: OpenAI client instance
    """

    DEFAULT_MODEL = "text-embedding-3-small"
    DIMENSION = 1536

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize OpenAI embedding provider.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Embedding model to use
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package required. Install with: pip install openai")

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY required")

        self.model = model or self.DEFAULT_MODEL
        self.client = OpenAI(api_key=self.api_key)

    def embed(self, text: str) -> List[float]:
        """Generate embedding for single text."""
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        return response.data[0].embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        return [item.embedding for item in response.data]

    @property
    def dimension(self) -> int:
        return self.DIMENSION


class VectorStoreBackend(ABC):
    """Abstract base class for vector storage backends."""

    @abstractmethod
    def upsert(self, documents: List[VectorDocument]) -> List[str]:
        """Insert or update documents."""
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[VectorDocument]:
        """Search for similar documents."""
        pass

    @abstractmethod
    def delete(self, ids: List[str]) -> bool:
        """Delete documents by ID."""
        pass

    @abstractmethod
    def get(self, ids: List[str]) -> List[VectorDocument]:
        """Get documents by ID."""
        pass


class SupabaseVectorBackend(VectorStoreBackend):
    """Supabase pgvector backend for semantic search.

    Expects a table with the following schema:

    CREATE TABLE memory_vectors (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        content TEXT NOT NULL,
        embedding VECTOR(1536),
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE INDEX ON memory_vectors USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);

    -- Function for similarity search
    CREATE OR REPLACE FUNCTION match_memories(
        query_embedding VECTOR(1536),
        match_threshold FLOAT DEFAULT 0.7,
        match_count INT DEFAULT 10,
        filter_metadata JSONB DEFAULT NULL
    )
    RETURNS TABLE (
        id UUID,
        content TEXT,
        metadata JSONB,
        similarity FLOAT
    )
    LANGUAGE plpgsql
    AS $$
    BEGIN
        RETURN QUERY
        SELECT
            mv.id,
            mv.content,
            mv.metadata,
            1 - (mv.embedding <=> query_embedding) AS similarity
        FROM memory_vectors mv
        WHERE
            (filter_metadata IS NULL OR mv.metadata @> filter_metadata)
            AND 1 - (mv.embedding <=> query_embedding) > match_threshold
        ORDER BY mv.embedding <=> query_embedding
        LIMIT match_count;
    END;
    $$;
    """

    DEFAULT_TABLE = "memory_vectors"
    DEFAULT_MATCH_FUNCTION = "match_memories"

    def __init__(
        self,
        url: Optional[str] = None,
        key: Optional[str] = None,
        table_name: str = DEFAULT_TABLE,
        match_function: str = DEFAULT_MATCH_FUNCTION
    ):
        """Initialize Supabase vector backend.

        Args:
            url: Supabase project URL (defaults to SUPABASE_URL env var)
            key: Supabase anon/service key (defaults to SUPABASE_KEY env var)
            table_name: Name of the vectors table
            match_function: Name of the similarity search function
        """
        if not SUPABASE_AVAILABLE:
            raise ImportError("supabase package required. Install with: pip install supabase")

        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY required")

        self.table_name = table_name
        self.match_function = match_function
        self.client: Client = create_client(self.url, self.key)

    def upsert(self, documents: List[VectorDocument]) -> List[str]:
        """Insert or update documents in Supabase.

        Args:
            documents: List of VectorDocument to upsert

        Returns:
            List of document IDs
        """
        records = []
        for doc in documents:
            record = {
                "content": doc.content,
                "embedding": doc.embedding,
                "metadata": doc.metadata,
                "updated_at": "now()"
            }
            if doc.id:
                record["id"] = doc.id
            records.append(record)

        result = self.client.table(self.table_name).upsert(records).execute()
        return [r["id"] for r in result.data]

    def search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        filter_metadata: Optional[Dict[str, Any]] = None,
        threshold: float = 0.7
    ) -> List[VectorDocument]:
        """Search for similar documents using pgvector.

        Args:
            query_embedding: Query vector embedding
            limit: Maximum results to return
            filter_metadata: Optional metadata filter (JSONB containment)
            threshold: Minimum similarity threshold

        Returns:
            List of matching VectorDocuments with similarity scores
        """
        result = self.client.rpc(
            self.match_function,
            {
                "query_embedding": query_embedding,
                "match_threshold": threshold,
                "match_count": limit,
                "filter_metadata": filter_metadata
            }
        ).execute()

        documents = []
        for row in result.data:
            doc = VectorDocument(
                id=row["id"],
                content=row["content"],
                metadata=row.get("metadata", {}),
                similarity=row.get("similarity")
            )
            documents.append(doc)

        return documents

    def delete(self, ids: List[str]) -> bool:
        """Delete documents by ID.

        Args:
            ids: List of document IDs to delete

        Returns:
            True if successful
        """
        self.client.table(self.table_name).delete().in_("id", ids).execute()
        return True

    def get(self, ids: List[str]) -> List[VectorDocument]:
        """Get documents by ID.

        Args:
            ids: List of document IDs

        Returns:
            List of VectorDocuments
        """
        result = self.client.table(self.table_name).select("*").in_("id", ids).execute()

        return [
            VectorDocument(
                id=row["id"],
                content=row["content"],
                embedding=row.get("embedding"),
                metadata=row.get("metadata", {})
            )
            for row in result.data
        ]


class VectorStore:
    """High-level vector store interface for Artemis City.

    Combines embedding generation with vector storage for seamless
    semantic search operations. Integrates with the Artemis memory
    architecture.

    Example:
        store = VectorStore()

        # Store a memory
        doc_id = store.store(
            content="Artemis completed governance review of Pack Rat",
            metadata={"agent": "artemis", "action": "review"}
        )

        # Semantic search
        results = store.search("governance audit", limit=5)
        for doc in results:
            print(f"{doc.similarity:.2f}: {doc.content}")

    Attributes:
        embedding_provider: Provider for generating embeddings
        backend: Storage backend for vectors
    """

    def __init__(
        self,
        embedding_provider: Optional[EmbeddingProvider] = None,
        backend: Optional[VectorStoreBackend] = None
    ):
        """Initialize VectorStore.

        Args:
            embedding_provider: Embedding provider (defaults to OpenAI)
            backend: Vector storage backend (defaults to Supabase)
        """
        self.embedding_provider = embedding_provider or OpenAIEmbedding()
        self.backend = backend or SupabaseVectorBackend()

    def store(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        doc_id: Optional[str] = None
    ) -> str:
        """Store content with its embedding.

        Args:
            content: Text content to store
            metadata: Optional metadata dictionary
            doc_id: Optional document ID (generates if not provided)

        Returns:
            Document ID
        """
        # Add timestamp to metadata
        metadata = metadata or {}
        metadata["stored_at"] = time.time()

        # Generate embedding
        embedding = self.embedding_provider.embed(content)

        # Create document
        doc = VectorDocument(
            id=doc_id,
            content=content,
            embedding=embedding,
            metadata=metadata
        )

        # Store in backend
        ids = self.backend.upsert([doc])
        return ids[0] if ids else None

    def store_batch(
        self,
        contents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> List[str]:
        """Store multiple contents with embeddings.

        Args:
            contents: List of text contents
            metadatas: Optional list of metadata dicts

        Returns:
            List of document IDs
        """
        metadatas = metadatas or [{} for _ in contents]
        timestamp = time.time()

        # Generate embeddings in batch
        embeddings = self.embedding_provider.embed_batch(contents)

        # Create documents
        documents = []
        for content, embedding, metadata in zip(contents, embeddings, metadatas):
            metadata["stored_at"] = timestamp
            doc = VectorDocument(
                content=content,
                embedding=embedding,
                metadata=metadata
            )
            documents.append(doc)

        return self.backend.upsert(documents)

    def search(
        self,
        query: str,
        limit: int = 10,
        filter_metadata: Optional[Dict[str, Any]] = None,
        threshold: float = 0.7
    ) -> List[VectorDocument]:
        """Search for semantically similar content.

        Args:
            query: Search query text
            limit: Maximum results
            filter_metadata: Optional metadata filter
            threshold: Minimum similarity threshold

        Returns:
            List of matching documents with similarity scores
        """
        # Generate query embedding
        query_embedding = self.embedding_provider.embed(query)

        # Search backend
        return self.backend.search(
            query_embedding=query_embedding,
            limit=limit,
            filter_metadata=filter_metadata,
            threshold=threshold
        )

    def search_by_agent(
        self,
        query: str,
        agent_name: str,
        limit: int = 10
    ) -> List[VectorDocument]:
        """Search for content from a specific agent.

        Args:
            query: Search query text
            agent_name: Agent name to filter by
            limit: Maximum results

        Returns:
            List of matching documents
        """
        return self.search(
            query=query,
            limit=limit,
            filter_metadata={"agent": agent_name}
        )

    def delete(self, ids: List[str]) -> bool:
        """Delete documents by ID.

        Args:
            ids: List of document IDs

        Returns:
            True if successful
        """
        return self.backend.delete(ids)

    def get(self, ids: List[str]) -> List[VectorDocument]:
        """Get documents by ID.

        Args:
            ids: List of document IDs

        Returns:
            List of documents
        """
        return self.backend.get(ids)


# Integration with MemoryBus architecture
class VectorMemoryBackend:
    """MemoryBackend adapter for VectorStore.

    Allows VectorStore to be used as a backend for the existing
    MemoryBus architecture, providing semantic search capabilities
    to agents using the standard memory interface.

    Usage with MemoryBus:
        from memory_bus import MemoryBus
        from vector_store import VectorMemoryBackend

        vector_backend = VectorMemoryBackend()
        memory_bus = MemoryBus(backend=vector_backend)

        # Now uses semantic search
        memory_bus.write("Important governance decision", {"agent": "artemis"})
        results = memory_bus.read("policy decisions")  # Semantic search
    """

    def __init__(self, vector_store: Optional[VectorStore] = None):
        """Initialize vector memory backend.

        Args:
            vector_store: VectorStore instance (creates default if not provided)
        """
        self.vector_store = vector_store or VectorStore()

    def write(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Write content to vector store.

        Args:
            content: Content to store
            metadata: Optional metadata

        Returns:
            Document ID
        """
        return self.vector_store.store(content, metadata)

    def read(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Semantic search for content.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of matching entries (compatible with MemoryBus format)
        """
        results = self.vector_store.search(query, limit=limit)

        # Convert to MemoryBus format
        return [
            {
                "content": doc.content,
                "metadata": doc.metadata,
                "timestamp": doc.metadata.get("stored_at", 0),
                "similarity": doc.similarity
            }
            for doc in results
        ]


# Hebbian-influenced vector retrieval (for ATP integration)
class HebbianVectorStore(VectorStore):
    """Vector store with Hebbian-influenced retrieval.

    Combines semantic similarity with Hebbian connection strengths
    to influence retrieval ranking. Agents that frequently co-activate
    will have their memories weighted higher in search results.

    Integrates with the ATP Hebbian learning system.
    """

    def __init__(
        self,
        hebbian_weights: Optional[Dict[str, float]] = None,
        hebbian_influence: float = 0.3,
        **kwargs
    ):
        """Initialize Hebbian-influenced vector store.

        Args:
            hebbian_weights: Dict mapping agent pairs to weights
            hebbian_influence: Weight of Hebbian score in ranking (0-1)
            **kwargs: Passed to VectorStore
        """
        super().__init__(**kwargs)
        self.hebbian_weights = hebbian_weights or {}
        self.hebbian_influence = hebbian_influence

    def get_hebbian_weight(self, agent1: str, agent2: str) -> float:
        """Get Hebbian weight between two agents.

        Args:
            agent1: First agent name
            agent2: Second agent name

        Returns:
            Connection weight (0-1)
        """
        key = "-".join(sorted([agent1, agent2]))
        return self.hebbian_weights.get(key, 0.0)

    def update_hebbian_weight(
        self,
        agent1: str,
        agent2: str,
        delta: float = 0.1
    ):
        """Strengthen connection between agents.

        Args:
            agent1: First agent
            agent2: Second agent
            delta: Amount to increase weight
        """
        key = "-".join(sorted([agent1, agent2]))
        current = self.hebbian_weights.get(key, 0.0)
        self.hebbian_weights[key] = min(1.0, current + delta)

    def search_with_hebbian(
        self,
        query: str,
        requesting_agent: str,
        limit: int = 10,
        threshold: float = 0.5
    ) -> List[VectorDocument]:
        """Search with Hebbian-influenced ranking.

        Results are ranked by:
        - (1 - hebbian_influence) * semantic_similarity
        - hebbian_influence * hebbian_weight(requesting_agent, source_agent)

        Args:
            query: Search query
            requesting_agent: Agent making the request
            limit: Maximum results
            threshold: Minimum similarity threshold

        Returns:
            List of documents ranked by combined score
        """
        # Get semantic results
        results = self.search(query, limit=limit * 2, threshold=threshold)

        # Apply Hebbian influence
        scored_results = []
        for doc in results:
            source_agent = doc.metadata.get("agent", "unknown")
            hebbian_weight = self.get_hebbian_weight(requesting_agent, source_agent)

            # Combined score
            semantic_score = doc.similarity or 0
            combined_score = (
                (1 - self.hebbian_influence) * semantic_score +
                self.hebbian_influence * hebbian_weight
            )

            doc.metadata["hebbian_weight"] = hebbian_weight
            doc.metadata["combined_score"] = combined_score
            scored_results.append((combined_score, doc))

        # Sort by combined score
        scored_results.sort(key=lambda x: x[0], reverse=True)

        return [doc for _, doc in scored_results[:limit]]


# SQL setup script for Supabase
SUPABASE_SETUP_SQL = """
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create memory vectors table
CREATE TABLE IF NOT EXISTS memory_vectors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for similarity search
CREATE INDEX IF NOT EXISTS memory_vectors_embedding_idx
ON memory_vectors USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create index for metadata filtering
CREATE INDEX IF NOT EXISTS memory_vectors_metadata_idx
ON memory_vectors USING GIN (metadata);

-- Function for similarity search with metadata filtering
CREATE OR REPLACE FUNCTION match_memories(
    query_embedding VECTOR(1536),
    match_threshold FLOAT DEFAULT 0.7,
    match_count INT DEFAULT 10,
    filter_metadata JSONB DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    content TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        mv.id,
        mv.content,
        mv.metadata,
        1 - (mv.embedding <=> query_embedding) AS similarity
    FROM memory_vectors mv
    WHERE
        (filter_metadata IS NULL OR mv.metadata @> filter_metadata)
        AND 1 - (mv.embedding <=> query_embedding) > match_threshold
    ORDER BY mv.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER memory_vectors_updated_at
    BEFORE UPDATE ON memory_vectors
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
"""


def get_setup_sql() -> str:
    """Get SQL script to set up Supabase tables.

    Returns:
        SQL script string
    """
    return SUPABASE_SETUP_SQL
