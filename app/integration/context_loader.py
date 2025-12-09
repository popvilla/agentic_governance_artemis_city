"""Context loader for Obsidian vault.

This module provides utilities to load and parse context from
the Obsidian vault via the MCP server.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from .memory_client import MemoryClient


@dataclass
class ContextEntry:
    """Represents a single context entry from vault.

    Attributes:
        path: Note path in vault
        content: Note content
        tags: List of tags
        frontmatter: YAML frontmatter dict
        relevance_score: Optional relevance score for search results
    """

    path: str
    content: str
    tags: List[str]
    frontmatter: Dict
    relevance_score: Optional[float] = None

    def get_summary(self, max_length: int = 200) -> str:
        """Get content summary.

        Args:
            max_length: Maximum summary length

        Returns:
            Truncated content summary
        """
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."


class ContextLoader:
    """Loader for context from Obsidian vault.

    Provides high-level methods to load, search, and organize
    context from the vault via MCP server.
    """

    def __init__(self, memory_client: Optional[MemoryClient] = None):
        """Initialize context loader.

        Args:
            memory_client: MemoryClient instance (creates new if None)
        """
        self.client = memory_client or MemoryClient()

    def load_note(self, path: str) -> Optional[ContextEntry]:
        """Load a single note as context entry.

        Args:
            path: Path to note in vault

        Returns:
            ContextEntry or None if failed
        """
        # Get note content
        response = self.client.get_context(path)
        if not response.success:
            return None

        content = response.data.get('content', '')

        # Get tags
        tags_response = self.client.manage_tags(path, 'get')
        tags = []
        if tags_response.success and tags_response.data:
            tags = tags_response.data.get('tags', [])

        # Get frontmatter
        fm_response = self.client.manage_frontmatter(path, 'list')
        frontmatter = {}
        if fm_response.success and fm_response.data:
            frontmatter = fm_response.data.get('frontmatter', {})

        return ContextEntry(path=path, content=content, tags=tags, frontmatter=frontmatter)

    def search_context(
        self, query: str, limit: int = 10, context_length: int = 200
    ) -> List[ContextEntry]:
        """Search vault for relevant context.

        Args:
            query: Search query
            limit: Maximum results to return
            context_length: Context snippet length

        Returns:
            List of matching ContextEntry objects
        """
        response = self.client.search_notes(query, context_length)
        if not response.success:
            return []

        results = response.data.get('results', [])[:limit]
        entries = []

        for result in results:
            entry = ContextEntry(
                path=result.get('path', ''),
                content=result.get('content', ''),
                tags=result.get('tags', []),
                frontmatter=result.get('frontmatter', {}),
                relevance_score=result.get('score'),
            )
            entries.append(entry)

        return entries

    def load_folder_context(self, folder: str) -> List[ContextEntry]:
        """Load all notes in a folder as context.

        Args:
            folder: Folder path in vault

        Returns:
            List of ContextEntry objects
        """
        # List notes in folder
        response = self.client.list_notes(folder)
        if not response.success:
            return []

        note_paths = response.data.get('notes', [])
        entries = []

        for path in note_paths:
            entry = self.load_note(path)
            if entry:
                entries.append(entry)

        return entries

    def load_tagged_context(self, tag: str, limit: int = 20) -> List[ContextEntry]:
        """Load notes with specific tag.

        Args:
            tag: Tag to search for (without #)
            limit: Maximum results to return

        Returns:
            List of ContextEntry objects
        """
        # Search for tag
        query = f"#{tag}"
        return self.search_context(query, limit=limit)

    def load_agent_history(self, agent_name: str, limit: int = 10) -> List[ContextEntry]:
        """Load historical context for an agent.

        Args:
            agent_name: Agent name
            limit: Maximum entries to return

        Returns:
            List of ContextEntry objects
        """
        # Get agent context via memory client
        response = self.client.get_agent_context(agent_name, limit)
        if not response.success:
            return []

        results = response.data.get('results', [])
        entries = []

        for result in results:
            path = result.get('path', '')
            entry = self.load_note(path)
            if entry:
                entries.append(entry)

        return entries

    def get_context_summary(self, entries: List[ContextEntry], max_entries: int = 5) -> str:
        """Generate summary from context entries.

        Args:
            entries: List of context entries
            max_entries: Maximum entries to include

        Returns:
            Formatted summary string
        """
        if not entries:
            return "No context available."

        parts = [f"Context Summary ({len(entries)} entries):\n"]

        for i, entry in enumerate(entries[:max_entries], 1):
            parts.append(f"\n{i}. {entry.path}")
            if entry.tags:
                parts.append(f"   Tags: {', '.join(entry.tags)}")
            parts.append(f"   {entry.get_summary(150)}")

        if len(entries) > max_entries:
            parts.append(f"\n... and {len(entries) - max_entries} more entries")

        return "\n".join(parts)

    def filter_by_date_range(
        self,
        entries: List[ContextEntry],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[ContextEntry]:
        """Filter context entries by date range.

        Looks for 'date' or 'created' in frontmatter.

        Args:
            entries: List of context entries
            start_date: Start date (ISO format)
            end_date: End date (ISO format)

        Returns:
            Filtered list of entries
        """
        filtered = []

        for entry in entries:
            # Try to get date from frontmatter
            date = entry.frontmatter.get('date') or entry.frontmatter.get('created')

            if not date:
                continue

            # Simple string comparison (assumes ISO format)
            if start_date and date < start_date:
                continue
            if end_date and date > end_date:
                continue

            filtered.append(entry)

        return filtered

    def get_related_context(self, path: str, max_related: int = 5) -> List[ContextEntry]:
        """Get context related to a specific note.

        Uses tags and content keywords to find related notes.

        Args:
            path: Path to reference note
            max_related: Maximum related entries to return

        Returns:
            List of related ContextEntry objects
        """
        # Load the reference note
        entry = self.load_note(path)
        if not entry:
            return []

        # Search by tags
        related = []
        for tag in entry.tags:
            tag_entries = self.load_tagged_context(tag, limit=3)
            related.extend([e for e in tag_entries if e.path != path])

        # Remove duplicates and limit
        seen = set()
        unique_related = []
        for e in related:
            if e.path not in seen:
                seen.add(e.path)
                unique_related.append(e)

        return unique_related[:max_related]
