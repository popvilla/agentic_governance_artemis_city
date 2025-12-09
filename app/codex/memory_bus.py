"""Memory bus system for persistent agent memory operations.

This module provides a pluggable memory backend system for the Artemis
City framework. It implements a file-based storage backend for persisting
agent interactions and enables memory queries across stored content.

The MemoryBus acts as an abstraction layer over different storage backends,
allowing agents to store and retrieve information without coupling to
specific storage implementations.
"""

from abc import ABC, abstractmethod
import os
import json
import time


class MemoryBackend(ABC):
    """Abstract base class for memory storage backends.

    Defines the interface that all memory backends must implement,
    ensuring consistent read/write operations across different
    storage implementations.
    """

    @abstractmethod
    def write(self, content, metadata=None):
        """Write content to the memory backend.

        Args:
            content: The content to store.
            metadata: Optional metadata dictionary to associate with
                the content.

        Returns:
            Implementation-specific identifier or path for the stored
            content, or None if the operation failed.
        """
        pass

    @abstractmethod
    def read(self, query):
        """Read content from the memory backend matching a query.

        Args:
            query: Search query string to match against stored content.

        Returns:
            List of matching content entries.
        """
        pass


class FileMemoryBackend(MemoryBackend):
    """File-based memory storage backend.

    Stores memory entries as individual JSON files in a specified
    directory. Each entry includes content, metadata, and timestamps.
    Supports basic search by matching query strings against content.

    Attributes:
        base_path: Directory path where memory files are stored.
    """

    def __init__(self, base_path="memory_store"):
        """Initialize the file-based memory backend.

        Args:
            base_path: Directory path for storing memory files.
                Created if it doesn't exist.
        """
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    def write(self, content, metadata=None):
        """Write content to a JSON file in the memory store.

        Creates a timestamped JSON file containing the content,
        metadata, and write timestamp.

        Args:
            content: The content to store.
            metadata: Optional dictionary of metadata. If it includes
                a 'source' key, that value is used in the filename.

        Returns:
            str: Path to the created file if successful, None otherwise.
        """
        metadata = metadata or {}
        filename = f"{int(time.time())}_{metadata.get('source', 'unknown')}.json"
        filepath = os.path.join(self.base_path, filename)
        data = {
            "content": content,
            "metadata": metadata,
            "timestamp": time.time()
        }
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return filepath
        except Exception as e:
            print(f"[Memory] Write failed: {e}")
            return None

    def read(self, query):
        """Search stored memories for content matching a query.

        Performs a case-insensitive substring search across all
        stored memory files, returning entries where the content
        contains the query string.

        Args:
            query: Search string to match against stored content.

        Returns:
            list: List of matching memory entries (dictionaries with
                'content', 'metadata', and 'timestamp' keys).
        """
        results = []
        if not os.path.exists(self.base_path):
            return results

        for f in os.listdir(self.base_path):
            if f.endswith(".json"):
                try:
                    with open(os.path.join(self.base_path, f), 'r') as file:
                        data = json.load(file)
                        if query.lower() in str(data.get("content", "")).lower():
                            results.append(data)
                except Exception:
                    continue
        return results


class MemoryBus:
    """High-level memory interface for agent memory operations.

    Provides an abstraction layer over memory backends, allowing
    agents to perform memory operations without coupling to specific
    storage implementations. Currently supports file-based storage.

    Attributes:
        backend: The underlying MemoryBackend implementation.
    """

    def __init__(self, backend_type="file"):
        """Initialize the MemoryBus with the specified backend.

        Args:
            backend_type: Type of backend to use. Currently supported:
                - 'file': File-based storage (default)
        """
        if backend_type == "file":
            self.backend = FileMemoryBackend()
        else:
            print(f"[Memory] Unknown backend {backend_type}, defaulting to file.")
            self.backend = FileMemoryBackend()

    def write(self, content, metadata=None):
        """Write content to the memory backend.

        Args:
            content: The content to store.
            metadata: Optional metadata dictionary.

        Returns:
            Implementation-specific result from the backend write operation.
        """
        return self.backend.write(content, metadata)

    def read(self, query):
        """Query the memory backend for matching content.

        Args:
            query: Search query string.

        Returns:
            List of matching memory entries from the backend.
        """
        return self.backend.read(query)
