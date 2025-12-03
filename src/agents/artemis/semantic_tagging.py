"""Semantic tagging system for Artemis.

This module provides semantic tagging and citation capabilities for
organizing knowledge and referencing files, concepts, and conversations.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set


@dataclass
class SemanticTag:
    """Represents a semantic tag with metadata.

    Attributes:
        tag: Tag name (e.g., 'architecture', 'memory-system')
        category: Tag category (e.g., 'concept', 'file', 'agent')
        references: Set of items tagged with this tag
        description: Optional description of tag meaning
    """

    tag: str
    category: str
    references: Set[str] = field(default_factory=set)
    description: Optional[str] = None

    def add_reference(self, reference: str) -> None:
        """Add a reference to this tag."""
        self.references.add(reference)

    def __str__(self) -> str:
        return f"#{self.tag} ({self.category}) [{len(self.references)} refs]"


@dataclass
class Citation:
    """Represents a citation to a file or concept.

    Attributes:
        target: What is being cited (file path, concept name, etc.)
        citation_type: Type of citation (file, concept, agent, url)
        context: Context where citation appears
        line_number: Optional line number for file citations
    """

    target: str
    citation_type: str
    context: Optional[str] = None
    line_number: Optional[int] = None

    def format(self) -> str:
        """Format citation for display."""
        if self.citation_type == "file":
            path = Path(self.target)
            if self.line_number:
                return f"[{path.name}:{self.line_number}]({self.target})"
            return f"[{path.name}]({self.target})"
        elif self.citation_type == "concept":
            return f"*{self.target}*"
        elif self.citation_type == "agent":
            return f"@{self.target}"
        return self.target


class SemanticTagger:
    """Semantic tagging and citation system.

    Provides capabilities for:
    - Tagging files, concepts, and conversations
    - Generating citations
    - Organizing knowledge by tags
    - Finding related items through tags
    """

    # Predefined tag categories
    TAG_CATEGORIES = {
        "concept": "Abstract ideas and patterns",
        "file": "File paths and documents",
        "agent": "Agent names and roles",
        "protocol": "Communication protocols",
        "technology": "Technologies and frameworks",
        "status": "Status indicators",
    }

    def __init__(self):
        """Initialize semantic tagger."""
        self.tags: Dict[str, SemanticTag] = {}
        self.citations: List[Citation] = []
        self.item_tags: Dict[str, Set[str]] = {}  # item -> tags

    def tag_item(self, item: str, tags: List[str], category: str = "concept") -> None:
        """Tag an item with semantic tags.

        Args:
            item: Item to tag (file path, concept, etc.)
            tags: List of tag names
            category: Tag category
        """
        # Ensure tags exist
        for tag_name in tags:
            tag_key = self._normalize_tag(tag_name)
            if tag_key not in self.tags:
                self.tags[tag_key] = SemanticTag(tag=tag_name, category=category)

            # Add reference
            self.tags[tag_key].add_reference(item)

        # Track item's tags
        if item not in self.item_tags:
            self.item_tags[item] = set()
        self.item_tags[item].update(self._normalize_tag(t) for t in tags)

    def add_citation(
        self,
        target: str,
        citation_type: str,
        context: Optional[str] = None,
        line_number: Optional[int] = None,
    ) -> Citation:
        """Add a citation.

        Args:
            target: Citation target
            citation_type: Type of citation
            context: Optional context
            line_number: Optional line number

        Returns:
            Created Citation object
        """
        citation = Citation(
            target=target, citation_type=citation_type, context=context, line_number=line_number
        )
        self.citations.append(citation)
        return citation

    def get_items_by_tag(self, tag: str) -> List[str]:
        """Get all items with a specific tag.

        Args:
            tag: Tag name to search for

        Returns:
            List of items with that tag
        """
        tag_key = self._normalize_tag(tag)
        if tag_key in self.tags:
            return list(self.tags[tag_key].references)
        return []

    def get_tags_for_item(self, item: str) -> List[str]:
        """Get all tags for an item.

        Args:
            item: Item to get tags for

        Returns:
            List of tag names
        """
        if item in self.item_tags:
            return [
                self.tags[tag_key].tag for tag_key in self.item_tags[item] if tag_key in self.tags
            ]
        return []

    def find_related_items(self, item: str) -> List[str]:
        """Find items related to given item through shared tags.

        Args:
            item: Item to find related items for

        Returns:
            List of related items
        """
        if item not in self.item_tags:
            return []

        related = set()
        item_tag_keys = self.item_tags[item]

        # Find items sharing any tags
        for tag_key in item_tag_keys:
            if tag_key in self.tags:
                related.update(self.tags[tag_key].references)

        # Remove the item itself
        related.discard(item)

        return list(related)

    def extract_tags_from_text(self, text: str) -> List[str]:
        """Extract hashtags from text.

        Args:
            text: Text to extract tags from

        Returns:
            List of extracted tag names
        """
        # Match #tag or #tag-with-hyphens
        pattern = r'#([\w-]+)'
        matches = re.findall(pattern, text)
        return matches

    def extract_citations_from_text(self, text: str) -> List[Citation]:
        """Extract citations from text.

        Args:
            text: Text to extract citations from

        Returns:
            List of extracted Citation objects
        """
        citations = []

        # File paths (absolute or relative)
        file_pattern = r'(?:^|[\s(])([\/~][\w\/.-]+\.[\w]+)'
        for match in re.finditer(file_pattern, text):
            path = match.group(1)
            citations.append(
                Citation(
                    target=path,
                    citation_type="file",
                    context=text[max(0, match.start() - 20) : match.end() + 20],
                )
            )

        # @agent mentions
        agent_pattern = r'@(\w+)'
        for match in re.finditer(agent_pattern, text):
            agent_name = match.group(1)
            citations.append(
                Citation(
                    target=agent_name,
                    citation_type="agent",
                    context=text[max(0, match.start() - 20) : match.end() + 20],
                )
            )

        return citations

    def generate_tag_summary(self) -> str:
        """Generate summary of all tags and their usage.

        Returns:
            Formatted tag summary
        """
        if not self.tags:
            return "No tags defined yet."

        parts = ["## Semantic Tag Summary\n"]

        # Group by category
        by_category: Dict[str, List[SemanticTag]] = {}
        for tag in self.tags.values():
            if tag.category not in by_category:
                by_category[tag.category] = []
            by_category[tag.category].append(tag)

        # Output by category
        for category, tags_list in sorted(by_category.items()):
            parts.append(f"### {category.title()}")
            for tag in sorted(tags_list, key=lambda t: len(t.references), reverse=True):
                parts.append(f"- #{tag.tag} ({len(tag.references)} references)")
            parts.append("")

        return "\n".join(parts)

    def get_citation_context(self, target: str) -> List[str]:
        """Get all contexts where a target was cited.

        Args:
            target: Citation target to search for

        Returns:
            List of context strings
        """
        contexts = []
        for citation in self.citations:
            if citation.target == target and citation.context:
                contexts.append(citation.context)
        return contexts

    @staticmethod
    def _normalize_tag(tag: str) -> str:
        """Normalize tag name for consistent storage.

        Args:
            tag: Tag name to normalize

        Returns:
            Normalized tag name
        """
        # Remove # prefix if present, lowercase, replace spaces with hyphens
        normalized = tag.lstrip('#').lower().replace(' ', '-')
        return normalized

    def get_stats(self) -> Dict:
        """Get tagging system statistics.

        Returns:
            Statistics dictionary
        """
        return {
            "total_tags": len(self.tags),
            "total_citations": len(self.citations),
            "tagged_items": len(self.item_tags),
            "tags_by_category": {
                cat: sum(1 for t in self.tags.values() if t.category == cat)
                for cat in set(t.category for t in self.tags.values())
            },
        }
