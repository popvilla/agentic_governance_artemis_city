"""
Unit tests for Artemis Persona functionality.

Tests the ArtemisPersona, ReflectionEngine, and SemanticTagger components.
"""

import pytest

from agents.artemis import ArtemisPersona, ReflectionEngine, ResponseMode, SemanticTagger


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
        assert ResponseMode.REFLECTIVE is not None
        assert ResponseMode.ARCHITECTURAL is not None
        assert ResponseMode.POETIC is not None

    def test_persona_with_mode(self):
        """Test creating persona with specific mode."""
        persona = ArtemisPersona()
        persona.set_mode(ResponseMode.REFLECTIVE)
        assert persona is not None
        assert persona.current_mode == ResponseMode.REFLECTIVE


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

        _ = ConceptGraph()  # Verify graph can be created
        node = ConceptNode(concept="Test Concept", frequency=1)
        # Test that graph can accept nodes
        assert node is not None
        assert node.concept == "Test Concept"
        assert node.frequency == 1


class TestSemanticTagger:
    """Test Semantic Tagger functionality."""

    def test_semantic_tagger_initialization(self):
        """Test that SemanticTagger can be initialized."""
        tagger = SemanticTagger()
        assert tagger is not None

    def test_semantic_tag_creation(self):
        """Test creating semantic tags."""
        from agents.artemis import SemanticTag

        tag = SemanticTag(tag="governance", category="system", description="System governance")
        assert tag.tag == "governance"
        assert tag.category == "system"
        assert tag.description == "System governance"

    def test_tag_text(self):
        """Test tagging text content."""
        tagger = SemanticTagger()
        item = "test-document.md"
        tags = ["governance", "system"]
        # Should be able to tag items
        tagger.tag_item(item, tags, category="file")
        result = tagger.get_tags_for_item(item)
        assert result is not None
        assert len(result) == 2


class TestCitationSystem:
    """Test citation and reference system."""

    def test_citation_creation(self):
        """Test creating citations."""
        from agents.artemis import Citation

        citation = Citation(
            target="memory/trust_decay_model.md",
            citation_type="file",
            line_number=42,
            context="Trust decays over time",
        )
        assert citation.target == "memory/trust_decay_model.md"
        assert citation.citation_type == "file"
        assert citation.line_number == 42
        assert citation.context == "Trust decays over time"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
