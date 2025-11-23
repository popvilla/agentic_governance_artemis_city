"""Reflection and synthesis capabilities for Artemis.

This module implements idea synthesis, pattern recognition, and
narrative building from multiple conversation threads.
"""

from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import re


@dataclass
class ConceptNode:
    """Represents a concept extracted from conversations.
    
    Attributes:
        concept: The concept text
        contexts: List of contexts where concept appeared
        related_concepts: Set of related concept names
        frequency: Number of times concept appeared
        importance_score: Calculated importance (0-1)
    """
    concept: str
    contexts: List[str] = field(default_factory=list)
    related_concepts: Set[str] = field(default_factory=set)
    frequency: int = 0
    importance_score: float = 0.0
    
    def add_context(self, context: str) -> None:
        """Add a context where this concept appeared."""
        self.contexts.append(context)
        self.frequency += 1
    
    def relate_to(self, other_concept: str) -> None:
        """Mark another concept as related."""
        self.related_concepts.add(other_concept)


@dataclass
class ConceptGraph:
    """Graph of concepts and their relationships.
    
    Attributes:
        concepts: Dictionary of concept name to ConceptNode
        concept_pairs: Set of related concept pairs
    """
    concepts: Dict[str, ConceptNode] = field(default_factory=dict)
    concept_pairs: Set[Tuple[str, str]] = field(default_factory=set)
    
    def add_concept(self, concept: str, context: str) -> None:
        """Add or update a concept in the graph.
        
        Args:
            concept: Concept text
            context: Context where concept appeared
        """
        concept_key = concept.lower()
        if concept_key not in self.concepts:
            self.concepts[concept_key] = ConceptNode(concept=concept)
        
        self.concepts[concept_key].add_context(context)
    
    def relate_concepts(self, concept1: str, concept2: str) -> None:
        """Create relationship between two concepts.
        
        Args:
            concept1: First concept
            concept2: Second concept
        """
        key1 = concept1.lower()
        key2 = concept2.lower()
        
        if key1 in self.concepts and key2 in self.concepts:
            self.concepts[key1].relate_to(key2)
            self.concepts[key2].relate_to(key1)
            
            # Store pair (sorted for consistency)
            pair = tuple(sorted([key1, key2]))
            self.concept_pairs.add(pair)
    
    def get_top_concepts(self, n: int = 10) -> List[ConceptNode]:
        """Get top N concepts by importance.
        
        Args:
            n: Number of concepts to return
            
        Returns:
            List of top ConceptNode objects
        """
        sorted_concepts = sorted(
            self.concepts.values(),
            key=lambda c: (c.importance_score, c.frequency),
            reverse=True
        )
        return sorted_concepts[:n]
    
    def find_concept_clusters(self) -> List[Set[str]]:
        """Find clusters of related concepts.
        
        Returns:
            List of concept clusters (sets of concept names)
        """
        visited = set()
        clusters = []
        
        def dfs(concept_key: str, cluster: Set[str]) -> None:
            """Depth-first search to find connected concepts."""
            if concept_key in visited:
                return
            
            visited.add(concept_key)
            cluster.add(concept_key)
            
            if concept_key in self.concepts:
                for related in self.concepts[concept_key].related_concepts:
                    dfs(related, cluster)
        
        for concept_key in self.concepts:
            if concept_key not in visited:
                cluster = set()
                dfs(concept_key, cluster)
                if len(cluster) > 1:  # Only include clusters with multiple concepts
                    clusters.append(cluster)
        
        return clusters


class ReflectionEngine:
    """Engine for synthesizing ideas and finding patterns.
    
    Capabilities:
    - Extract key concepts from conversations
    - Identify relationships between concepts
    - Generate unified narratives
    - Find patterns across discussions
    """
    
    def __init__(self):
        """Initialize reflection engine."""
        self.concept_graph = ConceptGraph()
        self.conversation_history: List[str] = []
    
    def add_conversation(self, text: str) -> None:
        """Add a conversation to the reflection corpus.
        
        Args:
            text: Conversation text to analyze
        """
        self.conversation_history.append(text)
        
        # Extract concepts
        concepts = self._extract_concepts(text)
        
        # Add concepts to graph
        for concept in concepts:
            self.concept_graph.add_concept(concept, text)
        
        # Find relationships between concepts in this text
        self._identify_relationships(concepts, text)
    
    def synthesize(self, focus: Optional[str] = None) -> str:
        """Synthesize insights from conversation history.
        
        Args:
            focus: Optional focus area for synthesis
            
        Returns:
            Synthesized narrative
        """
        if not self.conversation_history:
            return "No conversations to synthesize yet."
        
        # Get top concepts
        top_concepts = self.concept_graph.get_top_concepts(10)
        
        # Find concept clusters
        clusters = self.concept_graph.find_concept_clusters()
        
        # Build synthesis
        parts = ["## Synthesis of Recent Conversations\n"]
        
        # Key themes
        if top_concepts:
            parts.append("### Key Themes")
            for i, concept in enumerate(top_concepts[:5], 1):
                parts.append(
                    f"{i}. **{concept.concept}** "
                    f"(appeared {concept.frequency} times)"
                )
            parts.append("")
        
        # Concept clusters
        if clusters:
            parts.append("### Connected Ideas")
            for i, cluster in enumerate(clusters[:3], 1):
                concept_names = [
                    self.concept_graph.concepts[c].concept 
                    for c in cluster
                ]
                parts.append(f"{i}. {' ↔ '.join(concept_names[:5])}")
            parts.append("")
        
        # Narrative
        parts.append("### Emerging Narrative")
        narrative = self._build_narrative(top_concepts, clusters)
        parts.append(narrative)
        
        return "\n".join(parts)
    
    def find_connections(self, concept: str) -> List[str]:
        """Find concepts connected to a given concept.
        
        Args:
            concept: Concept to find connections for
            
        Returns:
            List of connected concept names
        """
        concept_key = concept.lower()
        if concept_key in self.concept_graph.concepts:
            node = self.concept_graph.concepts[concept_key]
            return [
                self.concept_graph.concepts[c].concept 
                for c in node.related_concepts
            ]
        return []
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text.
        
        Args:
            text: Text to extract from
            
        Returns:
            List of concept strings
        """
        # Simple concept extraction using noun phrases and key terms
        # This is a basic implementation - could be enhanced with NLP
        
        concepts = []
        
        # Extract capitalized phrases (likely proper nouns/concepts)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        concepts.extend(capitalized)
        
        # Extract quoted terms (explicit concepts)
        quoted = re.findall(r'"([^"]+)"', text)
        concepts.extend(quoted)
        
        # Extract technical terms (CamelCase, snake_case)
        technical = re.findall(r'\b[A-Z][a-z]+[A-Z]\w+\b', text)
        concepts.extend(technical)
        
        technical_snake = re.findall(r'\b\w+_\w+\b', text)
        concepts.extend(technical_snake)
        
        # Deduplicate while preserving order
        seen = set()
        unique_concepts = []
        for concept in concepts:
            if concept.lower() not in seen and len(concept) > 2:
                seen.add(concept.lower())
                unique_concepts.append(concept)
        
        return unique_concepts
    
    def _identify_relationships(
        self, 
        concepts: List[str], 
        context: str
    ) -> None:
        """Identify relationships between concepts in context.
        
        Args:
            concepts: List of concepts to relate
            context: Context text containing the concepts
        """
        # Simple co-occurrence based relationship
        # Concepts appearing in same context are related
        for i, concept1 in enumerate(concepts):
            for concept2 in concepts[i+1:]:
                self.concept_graph.relate_concepts(concept1, concept2)
    
    def _build_narrative(
        self, 
        top_concepts: List[ConceptNode],
        clusters: List[Set[str]]
    ) -> str:
        """Build a narrative from top concepts and clusters.
        
        Args:
            top_concepts: Top concept nodes
            clusters: Concept clusters
            
        Returns:
            Narrative text
        """
        if not top_concepts:
            return "Building understanding of your project landscape..."
        
        narrative_parts = []
        
        # Opening based on most frequent concept
        main_concept = top_concepts[0].concept
        narrative_parts.append(
            f"Your work centers around **{main_concept}**, "
            f"which has emerged as a central theme."
        )
        
        # Connections
        if len(top_concepts) > 1:
            related = [c.concept for c in top_concepts[1:3]]
            narrative_parts.append(
                f"This connects to {', '.join(related)}, "
                f"forming a cohesive system of ideas."
            )
        
        # Clusters indicate architectural patterns
        if clusters:
            narrative_parts.append(
                f"I'm seeing {len(clusters)} distinct conceptual clusters, "
                f"suggesting a multi-layered architecture."
            )
        
        return " ".join(narrative_parts)
    
    def get_stats(self) -> Dict:
        """Get reflection engine statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            "conversations_analyzed": len(self.conversation_history),
            "unique_concepts": len(self.concept_graph.concepts),
            "concept_relationships": len(self.concept_graph.concept_pairs),
            "concept_clusters": len(self.concept_graph.find_concept_clusters())
        }
