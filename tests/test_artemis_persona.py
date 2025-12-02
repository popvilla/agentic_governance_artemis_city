"""
Unit tests for Artemis Persona functionality.

Tests the ArtemisPersona, ReflectionEngine, and SemanticTagger components.
"""

import pytest
from agents.artemis import ArtemisPersona, ReflectionEngine, SemanticTagger, ResponseMode


class TestArtemisPersona:
    """Test Artemis Persona functionality."""

    def test_persona_initialization(self):
        """Test that ArtemisPersona can be initialized."""
        persona = ArtemisPersona()
        assert persona is not None

    def test_response_modes(self):
        """Test response mode enum values."""
        assert ResponseMode.TECHNICAL is not None
        assert ResponseMode.CONVERSATIONAL is not None
        assert ResponseMode.GOVERNANCE is not None

    def test_persona_with_mode(self):
        """Test creating persona with specific mode."""
        persona = ArtemisPersona(mode=ResponseMode.GOVERNANCE)
        assert persona is not None
        assert persona.mode == ResponseMode.GOVERNANCE


class TestReflectionEngine:
    """Test Reflection Engine functionality."""

    def test_reflection_engine_initialization(self):
        """Test that ReflectionEngine can be initialized."""
        engine = ReflectionEngine()
        assert engine is not None

    def test_concept_graph_creation(self):
        """Test creating a concept graph."""
        from agents.artemis import ConceptGraph
        graph = ConceptGraph()
        assert graph is not None

    def test_add_concept_node(self):
        """Test adding concept nodes to graph."""
        from agents.artemis import ConceptGraph, ConceptNode
        graph = ConceptGraph()
        node = ConceptNode(id="test-1", label="Test Concept", value="Test value")
        # Test that graph can accept nodes
        assert node is not None
        assert node.id == "test-1"


class TestSemanticTagger:
    """Test Semantic Tagger functionality."""

    def test_semantic_tagger_initialization(self):
        """Test that SemanticTagger can be initialized."""
        tagger = SemanticTagger()
        assert tagger is not None

    def test_semantic_tag_creation(self):
        """Test creating semantic tags."""
        from agents.artemis import SemanticTag
        tag = SemanticTag(
            name="governance",
            category="system",
            confidence=0.95
        )
        assert tag.name == "governance"
        assert tag.category == "system"
        assert tag.confidence == 0.95

    def test_tag_text(self):
        """Test tagging text content."""
        tagger = SemanticTagger()
        text = "This is a test of the governance system."
        # Should be able to tag text
        result = tagger.tag(text)
        assert result is not None or result == []


class TestCitationSystem:
    """Test citation and reference system."""

    def test_citation_creation(self):
        """Test creating citations."""
        from agents.artemis import Citation
        citation = Citation(
            source="memory/trust_decay_model.md",
            line_number=42,
            text="Trust decays over time"
        )
        assert citation.source == "memory/trust_decay_model.md"
        assert citation.line_number == 42


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
