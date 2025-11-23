# Artemis City Test Plan

> **Purpose:** Comprehensive test strategy for the Artemis City codebase, aligned with Python testing best practices using pytest.

---

## Table of Contents

1. [Test Strategy Overview](#test-strategy-overview)
2. [Test Directory Structure](#test-directory-structure)
3. [Unit Tests](#unit-tests)
4. [Integration Tests](#integration-tests)
5. [End-to-End Tests](#end-to-end-tests)
6. [Test Fixtures & Utilities](#test-fixtures--utilities)
7. [Running Tests](#running-tests)
8. [Coverage Requirements](#coverage-requirements)

---

## Test Strategy Overview

### Testing Pyramid

```
         ╱╲
        ╱  ╲        E2E Tests (10%)
       ╱────╲       - Full workflow validation
      ╱      ╲      - CLI interaction tests
     ╱────────╲
    ╱          ╲    Integration Tests (30%)
   ╱────────────╲   - Module interaction
  ╱              ╲  - ATP pipeline, Memory system
 ╱────────────────╲
╱                  ╲ Unit Tests (60%)
╲──────────────────╱ - Individual functions/classes
```

### Testing Framework

- **Framework:** pytest
- **Mocking:** pytest-mock, unittest.mock
- **Coverage:** pytest-cov
- **Async:** pytest-asyncio (if needed)

### Test Naming Convention

```
test_<module>_<function>_<scenario>
```

Examples:
- `test_atp_parser_parse_hash_format`
- `test_trust_score_apply_decay_after_one_day`
- `test_memory_client_get_context_server_unreachable`

---

## Test Directory Structure

```
Artemis-City/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Shared fixtures
│   │
│   ├── unit/                          # Unit tests
│   │   ├── __init__.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── test_persona.py        # ArtemisPersona tests
│   │   │   ├── test_reflection.py     # ReflectionEngine tests
│   │   │   ├── test_semantic_tagging.py
│   │   │   ├── test_atp_models.py
│   │   │   ├── test_atp_parser.py
│   │   │   └── test_atp_validator.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── test_instruction_loader.py
│   │   │   └── test_instruction_cache.py
│   │   └── memory/
│   │       ├── __init__.py
│   │       ├── test_memory_client.py
│   │       ├── test_context_loader.py
│   │       └── test_trust_interface.py
│   │
│   ├── integration/                   # Integration tests
│   │   ├── __init__.py
│   │   ├── test_atp_pipeline.py
│   │   ├── test_instruction_system.py
│   │   ├── test_artemis_integration.py
│   │   └── test_memory_system.py
│   │
│   └── e2e/                           # End-to-end tests
│       ├── __init__.py
│       ├── test_cli_workflow.py
│       └── test_demo_scripts.py
│
├── pytest.ini                         # pytest configuration
└── requirements-dev.txt               # Test dependencies
```

---

## Unit Tests

### 1. Agents/Artemis Module

#### test_persona.py

```python
"""Unit tests for ArtemisPersona."""

class TestResponseMode:
    """Tests for ResponseMode enum."""

    def test_response_mode_values(self):
        """Verify all response modes are defined."""

    def test_response_mode_default(self):
        """Default mode should be REFLECTIVE."""

class TestArtemisPersona:
    """Tests for ArtemisPersona class."""

    # Initialization
    def test_init_default_mode(self):
        """Persona initializes with REFLECTIVE mode."""

    def test_init_empty_context_history(self):
        """Persona initializes with empty context history."""

    # Mode Management
    def test_set_mode_valid(self):
        """Setting valid mode updates current mode."""

    def test_set_mode_all_modes(self):
        """All response modes can be set."""

    # Phrase Selection
    def test_get_opening_phrase_returns_string(self):
        """Opening phrase returns non-empty string."""

    def test_get_opening_phrase_varies(self):
        """Multiple calls may return different phrases."""

    def test_get_transition_phrase_by_mode(self):
        """Transition phrases match current mode."""

    def test_get_closing_phrase_by_mode(self):
        """Closing phrases match current mode."""

    # Verbose Detection
    def test_should_be_verbose_with_explain_keyword(self):
        """Verbose when context contains 'explain'."""

    def test_should_be_verbose_with_architecture_keyword(self):
        """Verbose when context contains 'architecture'."""

    def test_should_not_be_verbose_simple_query(self):
        """Not verbose for simple queries."""

    # Mode Inference
    def test_infer_mode_from_atp_build(self):
        """ATP BUILD mode infers TECHNICAL."""

    def test_infer_mode_from_atp_review(self):
        """ATP REVIEW mode infers REFLECTIVE."""

    def test_infer_mode_from_query_how(self):
        """Query starting with 'how' infers TECHNICAL."""

    def test_infer_mode_from_query_why(self):
        """Query starting with 'why' infers REFLECTIVE."""

    # Context History
    def test_add_context_memory_stores_context(self):
        """Context is stored in history."""

    def test_add_context_memory_max_limit(self):
        """History limited to 50 items (FIFO)."""

    def test_get_recent_context_returns_latest(self):
        """Recent context returns most recent entries."""

    # Response Formatting
    def test_format_response_with_framing(self):
        """Response includes opening and closing phrases."""

    def test_format_response_without_framing(self):
        """Response excludes framing when disabled."""

    # Edge Cases
    def test_empty_context_dictionary(self):
        """Handles empty context gracefully."""

    def test_none_query_in_context(self):
        """Handles None query in context."""
```

#### test_reflection.py

```python
"""Unit tests for ReflectionEngine."""

class TestConceptNode:
    """Tests for ConceptNode dataclass."""

    def test_init_defaults(self):
        """Node initializes with correct defaults."""

    def test_add_context_increments_frequency(self):
        """Adding context increments frequency."""

    def test_relate_to_adds_relationship(self):
        """Relating concepts creates bidirectional link."""

class TestConceptGraph:
    """Tests for ConceptGraph dataclass."""

    def test_add_concept_new(self):
        """New concept is added to graph."""

    def test_add_concept_existing_increments(self):
        """Existing concept frequency increases."""

    def test_relate_concepts_bidirectional(self):
        """Relationships are bidirectional."""

    def test_get_top_concepts_sorted(self):
        """Top concepts sorted by importance + frequency."""

    def test_find_concept_clusters_single(self):
        """Single isolated concept forms cluster of one."""

    def test_find_concept_clusters_connected(self):
        """Connected concepts form single cluster."""

class TestReflectionEngine:
    """Tests for ReflectionEngine class."""

    # Concept Extraction
    def test_extract_concepts_capitalized(self):
        """Extracts capitalized multi-word phrases."""

    def test_extract_concepts_quoted(self):
        """Extracts quoted terms."""

    def test_extract_concepts_camelcase(self):
        """Extracts CamelCase identifiers."""

    def test_extract_concepts_snake_case(self):
        """Extracts snake_case identifiers."""

    def test_extract_concepts_filters_short(self):
        """Filters concepts shorter than 3 characters."""

    # Synthesis
    def test_synthesize_with_concepts(self):
        """Synthesis generates narrative from concepts."""

    def test_synthesize_empty_graph(self):
        """Synthesis handles empty concept graph."""

    def test_synthesize_with_focus(self):
        """Focus parameter filters synthesis."""

    # Statistics
    def test_get_stats_accurate(self):
        """Stats reflect actual graph state."""

    # Edge Cases
    def test_add_conversation_empty_text(self):
        """Empty text adds nothing to graph."""

    def test_duplicate_concepts_merged(self):
        """Duplicate concepts are merged (case-insensitive)."""
```

#### test_semantic_tagging.py

```python
"""Unit tests for SemanticTagger."""

class TestSemanticTag:
    """Tests for SemanticTag dataclass."""

    def test_add_reference(self):
        """Reference is added to tag."""

    def test_str_format(self):
        """String format shows tag, category, ref count."""

class TestCitation:
    """Tests for Citation dataclass."""

    def test_format_file_citation(self):
        """File citation formatted correctly."""

    def test_format_agent_citation(self):
        """Agent citation formatted correctly."""

    def test_format_url_citation(self):
        """URL citation formatted correctly."""

class TestSemanticTagger:
    """Tests for SemanticTagger class."""

    # Tag Management
    def test_tag_item_creates_tag(self):
        """Tagging item creates tag if not exists."""

    def test_tag_item_adds_reference(self):
        """Tagging adds item to tag references."""

    def test_normalize_tag_lowercase(self):
        """Tags normalized to lowercase."""

    def test_normalize_tag_removes_hash(self):
        """Hash prefix removed from tags."""

    def test_normalize_tag_spaces_to_hyphens(self):
        """Spaces converted to hyphens."""

    # Citation Management
    def test_add_citation_creates_entry(self):
        """Adding citation creates entry."""

    def test_add_citation_with_line_number(self):
        """Citation stores line number."""

    # Lookups
    def test_get_items_by_tag(self):
        """Returns items with specific tag."""

    def test_get_tags_for_item(self):
        """Returns tags for specific item."""

    def test_find_related_items(self):
        """Finds items sharing tags."""

    # Text Extraction
    def test_extract_tags_from_text(self):
        """Extracts #hashtags from text."""

    def test_extract_tags_with_hyphens(self):
        """Extracts tags with hyphens."""

    def test_extract_citations_file_paths(self):
        """Extracts file path citations."""

    def test_extract_citations_agent_mentions(self):
        """Extracts @agent mentions."""

    # Summary & Stats
    def test_generate_tag_summary(self):
        """Generates formatted summary by category."""

    def test_get_stats_accurate(self):
        """Stats reflect actual state."""
```

### 2. Agents/ATP Module

#### test_atp_models.py

```python
"""Unit tests for ATP models."""

class TestATPEnums:
    """Tests for ATP enum types."""

    def test_atp_mode_values(self):
        """All ATPMode values defined."""

    def test_atp_priority_values(self):
        """All ATPPriority values defined."""

    def test_atp_action_type_values(self):
        """All ATPActionType values defined."""

class TestATPMessage:
    """Tests for ATPMessage dataclass."""

    def test_init_defaults(self):
        """Message initializes with defaults."""

    def test_has_atp_headers_true(self):
        """has_atp_headers True when headers present."""

    def test_has_atp_headers_false(self):
        """has_atp_headers False when no headers."""

    def test_is_complete_true(self):
        """is_complete True when mode+context+action."""

    def test_is_complete_false(self):
        """is_complete False when missing fields."""

    def test_to_dict(self):
        """to_dict returns all fields."""

    def test_str_format(self):
        """String format is human-readable."""
```

#### test_atp_parser.py

```python
"""Unit tests for ATPParser."""

class TestATPParser:
    """Tests for ATPParser class."""

    # Hash Format Parsing
    def test_parse_hash_format_mode(self):
        """Parses #Mode: header."""

    def test_parse_hash_format_context(self):
        """Parses #Context: header."""

    def test_parse_hash_format_priority(self):
        """Parses #Priority: header."""

    def test_parse_hash_format_action_type(self):
        """Parses #ActionType: header."""

    def test_parse_hash_format_target_zone(self):
        """Parses #TargetZone: header."""

    def test_parse_hash_format_special_notes(self):
        """Parses #SpecialNotes: header."""

    def test_parse_hash_format_all_headers(self):
        """Parses complete ATP message."""

    # Bracket Format Parsing
    def test_parse_bracket_format_mode(self):
        """Parses [[Mode]]: header."""

    def test_parse_bracket_format_all_headers(self):
        """Parses complete bracket format."""

    # Enum Parsing
    def test_parse_enum_valid_value(self):
        """Valid enum string converts to enum."""

    def test_parse_enum_case_insensitive(self):
        """Enum parsing is case-insensitive."""

    def test_parse_enum_unknown_defaults(self):
        """Unknown value defaults to UNKNOWN."""

    # Format Detection
    def test_detect_format_hash(self):
        """Detects hash format."""

    def test_detect_format_bracket(self):
        """Detects bracket format."""

    def test_detect_format_none(self):
        """Returns None for no format."""

    def test_is_atp_formatted_true(self):
        """Correctly identifies ATP formatted text."""

    def test_is_atp_formatted_false(self):
        """Correctly identifies non-ATP text."""

    # Content Handling
    def test_parse_extracts_content(self):
        """Content extracted after headers."""

    def test_parse_removes_separator_lines(self):
        """Separator lines removed from content."""

    def test_parse_preserves_raw_input(self):
        """Raw input preserved in message."""

    # Edge Cases
    def test_parse_empty_input(self):
        """Empty input returns message with empty content."""

    def test_parse_no_headers(self):
        """No headers puts all text in content."""

    def test_parse_duplicate_headers(self):
        """Last header value wins."""

    def test_parse_malformed_headers(self):
        """Malformed headers ignored."""

    def test_parse_whitespace_handling(self):
        """Whitespace trimmed from values."""
```

#### test_atp_validator.py

```python
"""Unit tests for ATPValidator."""

class TestValidationResult:
    """Tests for ValidationResult class."""

    def test_init_valid(self):
        """Starts as valid."""

    def test_add_warning_keeps_valid(self):
        """Warning doesn't invalidate."""

    def test_add_error_invalidates(self):
        """Error invalidates result."""

    def test_has_issues_with_warnings(self):
        """has_issues True with warnings."""

    def test_str_format(self):
        """String includes all issues."""

class TestATPValidator:
    """Tests for ATPValidator class."""

    # Content Validation
    def test_validate_empty_content_error(self):
        """Empty content is error."""

    def test_validate_short_content_warning(self):
        """Content < 10 chars is warning."""

    def test_validate_long_content_suggestion(self):
        """Content > 2000 chars gets suggestion."""

    # Header Validation
    def test_validate_no_headers_warning(self):
        """Missing headers is warning (non-strict)."""

    def test_validate_no_headers_error_strict(self):
        """Missing headers is error (strict mode)."""

    def test_validate_missing_mode_warning(self):
        """Missing Mode header is warning."""

    def test_validate_missing_context_warning(self):
        """Missing Context header is warning."""

    def test_validate_missing_action_type_warning(self):
        """Missing ActionType header is warning."""

    # Mode/Action Consistency
    def test_validate_build_execute_valid(self):
        """BUILD + EXECUTE is valid combination."""

    def test_validate_build_scaffold_valid(self):
        """BUILD + SCAFFOLD is valid combination."""

    def test_validate_build_summarize_suggestion(self):
        """BUILD + SUMMARIZE gets suggestion."""

    def test_validate_review_reflect_valid(self):
        """REVIEW + REFLECT is valid combination."""

    def test_validate_review_execute_suggestion(self):
        """REVIEW + EXECUTE gets suggestion."""

    # Target Zone Validation
    def test_validate_target_zone_valid_path(self):
        """Valid path format passes."""

    def test_validate_target_zone_invalid_suggestion(self):
        """Invalid format gets suggestion."""

    # Suggestions
    def test_suggest_improvements_returns_list(self):
        """suggest_improvements returns list."""

    def test_suggest_improvements_includes_missing(self):
        """Suggestions include missing headers."""
```

### 3. Core/Instructions Module

#### test_instruction_loader.py

```python
"""Unit tests for InstructionLoader."""

class TestInstructionScope:
    """Tests for InstructionScope dataclass."""

    def test_init_all_fields(self):
        """Scope initializes with all fields."""

class TestInstructionSet:
    """Tests for InstructionSet dataclass."""

    def test_add_scope_stores(self):
        """Added scope is stored."""

    def test_add_scope_sorts_by_priority(self):
        """Scopes sorted by priority ascending."""

    def test_get_merged_combines_content(self):
        """Merged content combines all scopes."""

    def test_get_merged_with_markers(self):
        """Markers included when requested."""

    def test_get_merged_without_markers(self):
        """Markers excluded when not requested."""

class TestInstructionLoader:
    """Tests for InstructionLoader class."""

    # Project Root Detection
    def test_find_project_root_git(self):
        """Finds root with .git marker."""

    def test_find_project_root_pyproject(self):
        """Finds root with pyproject.toml."""

    def test_find_project_root_none(self):
        """Returns None when no markers found."""

    # Scope Loading
    def test_load_global_instructions(self, tmp_path, monkeypatch):
        """Loads from home directory."""

    def test_load_project_instructions(self, tmp_path):
        """Loads from project root."""

    def test_load_local_instructions(self, tmp_path):
        """Loads from current directory."""

    def test_load_agent_instructions(self, tmp_path):
        """Loads agent-specific instructions."""

    # Priority
    def test_scope_priority_order(self):
        """Global < Project < Local < Agent priority."""

    # File Reading
    def test_read_file_existing(self, tmp_path):
        """Reads existing file content."""

    def test_read_file_missing(self):
        """Returns None for missing file."""

    def test_read_file_io_error(self, tmp_path):
        """Handles IO errors gracefully."""

    # Edge Cases
    def test_load_no_files_found(self, tmp_path):
        """Empty set when no instruction files."""

    def test_load_current_dir_same_as_root(self, tmp_path):
        """Skips local scope when same as project root."""
```

#### test_instruction_cache.py

```python
"""Unit tests for InstructionCache."""

class TestInstructionCache:
    """Tests for InstructionCache class."""

    # Cache Operations
    def test_get_cache_miss_loads(self, tmp_path):
        """Cache miss triggers load."""

    def test_get_cache_hit_returns_cached(self, tmp_path):
        """Cache hit returns cached value."""

    def test_get_force_reload_bypasses_cache(self, tmp_path):
        """Force reload ignores cache."""

    # TTL
    def test_ttl_not_expired(self, tmp_path):
        """Valid cache entry within TTL."""

    def test_ttl_expired_reloads(self, tmp_path, monkeypatch):
        """Expired entry triggers reload."""

    # Cache Key
    def test_make_cache_key_with_agent(self):
        """Key includes agent name."""

    def test_make_cache_key_without_agent(self):
        """Key uses _default for no agent."""

    def test_make_cache_key_normalizes_path(self):
        """Path normalized in key."""

    # Invalidation
    def test_invalidate_removes_entry(self, tmp_path):
        """Invalidate removes specific entry."""

    def test_clear_removes_all(self, tmp_path):
        """Clear removes all entries."""

    # Statistics
    def test_get_stats_accurate(self, tmp_path):
        """Stats reflect cache state."""

class TestGlobalCache:
    """Tests for global cache functions."""

    def test_get_global_cache_singleton(self):
        """Returns same instance."""

    def test_reset_global_cache(self):
        """Reset creates new instance."""
```

### 4. Memory/Integration Module

#### test_memory_client.py

```python
"""Unit tests for MemoryClient."""

class TestMCPResponse:
    """Tests for MCPResponse dataclass."""

    def test_from_json_success(self):
        """Creates response from successful JSON."""

    def test_from_json_error(self):
        """Creates response from error JSON."""

class TestMemoryClient:
    """Tests for MemoryClient class."""

    # Initialization
    def test_init_with_params(self):
        """Initializes with explicit params."""

    def test_init_from_env(self, monkeypatch):
        """Falls back to environment variables."""

    def test_init_missing_api_key_raises(self):
        """Raises ValueError without API key."""

    # Request Building (mocked)
    def test_make_request_builds_url(self, mocker):
        """Correct URL constructed."""

    def test_make_request_sets_headers(self, mocker):
        """Authorization header set."""

    def test_make_request_sends_json(self, mocker):
        """Request body is JSON."""

    # Operations (mocked)
    def test_get_context(self, mocker):
        """get_context calls correct operation."""

    def test_append_context(self, mocker):
        """append_context calls correct operation."""

    def test_update_note(self, mocker):
        """update_note calls correct operation."""

    def test_search_notes(self, mocker):
        """search_notes calls correct operation."""

    def test_list_notes(self, mocker):
        """list_notes calls correct operation."""

    def test_delete_note(self, mocker):
        """delete_note calls correct operation."""

    def test_manage_frontmatter(self, mocker):
        """manage_frontmatter calls correct operation."""

    def test_manage_tags(self, mocker):
        """manage_tags calls correct operation."""

    def test_search_replace(self, mocker):
        """search_replace calls correct operation."""

    # Error Handling
    def test_http_error_handling(self, mocker):
        """HTTP errors return error response."""

    def test_url_error_handling(self, mocker):
        """Network errors return error response."""

    def test_json_decode_error(self, mocker):
        """JSON errors return error response."""

    # Convenience Methods
    def test_health_check_success(self, mocker):
        """Health check returns True when accessible."""

    def test_health_check_failure(self, mocker):
        """Health check returns False when inaccessible."""

    def test_get_agent_context(self, mocker):
        """Gets agent's tagged notes."""

    def test_store_agent_context(self, mocker):
        """Stores timestamped context."""
```

#### test_context_loader.py

```python
"""Unit tests for ContextLoader."""

class TestContextEntry:
    """Tests for ContextEntry dataclass."""

    def test_get_summary_short_content(self):
        """Short content returned as-is."""

    def test_get_summary_truncates(self):
        """Long content truncated with ellipsis."""

class TestContextLoader:
    """Tests for ContextLoader class."""

    # Note Loading
    def test_load_note_success(self, mocker):
        """Loads note as ContextEntry."""

    def test_load_note_not_found(self, mocker):
        """Returns None for missing note."""

    # Search
    def test_search_context_returns_entries(self, mocker):
        """Search returns list of entries."""

    def test_search_context_no_results(self, mocker):
        """Empty list when no results."""

    # Folder Loading
    def test_load_folder_context(self, mocker):
        """Loads all notes in folder."""

    def test_load_folder_context_empty(self, mocker):
        """Empty list for empty folder."""

    # Tagged Loading
    def test_load_tagged_context(self, mocker):
        """Loads notes with specific tag."""

    # Agent History
    def test_load_agent_history(self, mocker):
        """Loads agent's context entries."""

    # Summary Generation
    def test_get_context_summary(self):
        """Generates formatted summary."""

    def test_get_context_summary_limits_entries(self):
        """Respects max_entries limit."""

    # Date Filtering
    def test_filter_by_date_range_start(self):
        """Filters entries after start date."""

    def test_filter_by_date_range_end(self):
        """Filters entries before end date."""

    def test_filter_by_date_range_both(self):
        """Filters entries within range."""

    # Related Context
    def test_get_related_context(self, mocker):
        """Finds related notes by tags."""
```

#### test_trust_interface.py

```python
"""Unit tests for TrustInterface."""

class TestTrustLevel:
    """Tests for TrustLevel enum."""

    def test_trust_level_thresholds(self):
        """Verify threshold values for each level."""

class TestTrustScore:
    """Tests for TrustScore dataclass."""

    # Decay
    def test_apply_decay_one_day(self):
        """Decay after one day."""

    def test_apply_decay_multiple_days(self):
        """Decay after multiple days."""

    def test_apply_decay_respects_floor(self):
        """Decay doesn't go below floor for level."""

    # Reinforcement
    def test_reinforce_increases_score(self):
        """Reinforcement increases score."""

    def test_reinforce_max_one(self):
        """Score capped at 1.0."""

    def test_reinforce_increments_count(self):
        """Reinforcement count incremented."""

    # Penalty
    def test_penalize_decreases_score(self):
        """Penalty decreases score."""

    def test_penalize_min_zero(self):
        """Score floored at 0.0."""

    def test_penalize_increments_count(self):
        """Penalty count incremented."""

    # Level Updates
    def test_update_level_full(self):
        """Score >= 0.9 is FULL."""

    def test_update_level_high(self):
        """Score 0.7-0.89 is HIGH."""

    def test_update_level_medium(self):
        """Score 0.5-0.69 is MEDIUM."""

    def test_update_level_low(self):
        """Score 0.3-0.49 is LOW."""

    def test_update_level_untrusted(self):
        """Score < 0.3 is UNTRUSTED."""

class TestTrustInterface:
    """Tests for TrustInterface class."""

    # Default Agents
    def test_init_default_agents(self):
        """Default agents initialized with correct scores."""

    # Score Management
    def test_get_trust_score_existing(self):
        """Returns existing score."""

    def test_get_trust_score_new_agent(self):
        """Creates score for new agent."""

    def test_get_trust_score_new_memory(self):
        """Creates score for new memory."""

    # Permission Checking
    def test_can_perform_operation_full_all(self):
        """FULL trust allows all operations."""

    def test_can_perform_operation_high_no_delete(self):
        """HIGH trust denies delete."""

    def test_can_perform_operation_medium_limited(self):
        """MEDIUM trust has limited operations."""

    def test_can_perform_operation_low_readonly(self):
        """LOW trust is read-only + search."""

    def test_can_perform_operation_untrusted_none(self):
        """UNTRUSTED denies all operations."""

    # Recording Events
    def test_record_success_reinforces(self):
        """Success reinforces score."""

    def test_record_failure_penalizes(self):
        """Failure penalizes score."""

    # Reporting
    def test_get_trust_report(self):
        """Report includes all scores."""

    # Filtering
    def test_filter_by_trust_includes_above(self):
        """Includes items above threshold."""

    def test_filter_by_trust_excludes_below(self):
        """Excludes items below threshold."""
```

---

## Integration Tests

### test_atp_pipeline.py

```python
"""Integration tests for ATP pipeline."""

class TestATPPipeline:
    """Tests for Parser → Validator → Message flow."""

    def test_parse_and_validate_complete_message(self):
        """Complete message parses and validates."""

    def test_parse_and_validate_incomplete_message(self):
        """Incomplete message gets warnings."""

    def test_parse_and_validate_invalid_content(self):
        """Invalid content gets errors."""

    def test_mode_action_consistency_through_pipeline(self):
        """Mode/action checked after parsing."""
```

### test_instruction_system.py

```python
"""Integration tests for instruction system."""

class TestInstructionSystem:
    """Tests for Loader → Cache → merged output."""

    def test_load_and_cache_instructions(self, tmp_path):
        """Instructions loaded and cached."""

    def test_cache_respects_ttl(self, tmp_path, monkeypatch):
        """Cache expires after TTL."""

    def test_merged_content_priority_order(self, tmp_path):
        """Higher priority scopes appear last."""
```

### test_artemis_integration.py

```python
"""Integration tests for Artemis agent components."""

class TestArtemisIntegration:
    """Tests for Persona + Reflection + Tagging."""

    def test_persona_with_reflection(self):
        """Persona uses reflection for synthesis."""

    def test_persona_with_tagging(self):
        """Persona uses tagging for citations."""

    def test_full_artemis_workflow(self):
        """Complete Artemis processing workflow."""
```

### test_memory_system.py

```python
"""Integration tests for memory system."""

class TestMemorySystem:
    """Tests for Client → ContextLoader → Trust."""

    def test_load_context_with_trust_check(self, mocker):
        """Context loading respects trust levels."""

    def test_store_context_updates_trust(self, mocker):
        """Storing context updates trust on success/failure."""

    def test_search_with_trust_filtering(self, mocker):
        """Search results filtered by trust."""
```

---

## End-to-End Tests

### test_cli_workflow.py

```python
"""End-to-end tests for CLI."""

class TestCLIWorkflow:
    """Tests for complete CLI interactions."""

    def test_cli_atp_command(self, tmp_path):
        """CLI processes ATP-formatted command."""

    def test_cli_instruction_display(self, tmp_path):
        """CLI displays loaded instructions."""

    def test_cli_agent_routing(self, tmp_path):
        """CLI routes to correct agent."""

    def test_cli_exit_commands(self, tmp_path):
        """CLI handles exit/quit."""
```

### test_demo_scripts.py

```python
"""End-to-end tests for demo scripts."""

class TestDemoScripts:
    """Tests verifying demo scripts run without error."""

    def test_demo_artemis_runs(self):
        """demo_artemis.py completes without error."""

    def test_demo_memory_integration_runs(self, mocker):
        """demo_memory_integration.py completes (mocked server)."""
```

---

## Test Fixtures & Utilities

### conftest.py

```python
"""Shared pytest fixtures."""

import pytest
from pathlib import Path

# Sample ATP Messages
@pytest.fixture
def sample_atp_hash():
    """Sample ATP message in hash format."""
    return """#Mode: Build
#Context: Implementing new feature
#Priority: High
#ActionType: Execute
#TargetZone: /agents/

Build the new agent component."""

@pytest.fixture
def sample_atp_bracket():
    """Sample ATP message in bracket format."""
    return """[[Mode]]: Review
[[Context]]: Code review
[[ActionType]]: Reflect

Review the implementation."""

# Temporary Project Structure
@pytest.fixture
def project_structure(tmp_path):
    """Create temporary project structure."""
    # Create directories
    (tmp_path / "agents").mkdir()
    (tmp_path / "codex").mkdir()
    (tmp_path / ".git").mkdir()

    # Create files
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'")
    (tmp_path / "codex.md").write_text("# Project Instructions")

    return tmp_path

# Mock Memory Client
@pytest.fixture
def mock_memory_client(mocker):
    """Mock MemoryClient for tests without server."""
    mock = mocker.MagicMock()
    mock.health_check.return_value = True
    mock.get_context.return_value = mocker.MagicMock(
        success=True,
        data={"content": "test content"}
    )
    return mock

# Sample Trust Scores
@pytest.fixture
def sample_trust_scores():
    """Sample trust score data."""
    return {
        "artemis": 0.95,
        "pack_rat": 0.85,
        "new_agent": 0.50,
        "untrusted": 0.20
    }

# Context Entries
@pytest.fixture
def sample_context_entries():
    """Sample context entries for testing."""
    from memory.integration import ContextEntry
    return [
        ContextEntry(
            path="test/note1.md",
            content="First note content",
            tags=["test", "sample"],
            frontmatter={"date": "2025-11-01"},
            relevance_score=0.9
        ),
        ContextEntry(
            path="test/note2.md",
            content="Second note content",
            tags=["test"],
            frontmatter={"date": "2025-11-15"},
            relevance_score=0.7
        )
    ]
```

---

## Running Tests

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
filterwarnings =
    ignore::DeprecationWarning
```

### requirements-dev.txt

```
# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
pytest-asyncio>=0.21.0

# Code Quality
ruff>=0.1.0
mypy>=1.5.0

# Development
black>=23.0.0
isort>=5.12.0
```

### Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test types
pytest -m unit
pytest -m integration
pytest -m e2e

# Run specific module tests
pytest tests/unit/agents/test_atp_parser.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/unit/agents/test_persona.py::TestArtemisPersona::test_set_mode_valid
```

---

## Coverage Requirements

### Minimum Coverage Targets

| Module | Target |
|--------|--------|
| agents/artemis/ | 90% |
| agents/atp/ | 95% |
| core/instructions/ | 85% |
| memory/integration/ | 85% |
| interface/ | 75% |
| **Overall** | **85%** |

### Coverage Configuration

```ini
# pyproject.toml or .coveragerc
[tool.coverage.run]
source = ["agents", "core", "memory", "interface"]
omit = ["*/tests/*", "*/__pycache__/*", "*/demo_*.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if __name__ == .__main__.:"
]
```

---

## Implementation Priority

### Phase 1: Core Unit Tests
1. ATP Parser & Validator
2. Trust Interface
3. Instruction Loader & Cache

### Phase 2: Agent Unit Tests
4. ArtemisPersona
5. ReflectionEngine
6. SemanticTagger

### Phase 3: Memory Unit Tests
7. MemoryClient (mocked)
8. ContextLoader

### Phase 4: Integration Tests
9. ATP Pipeline
10. Memory System
11. Artemis Integration

### Phase 5: E2E Tests
12. CLI Workflow
13. Demo Scripts

---

**Last Updated:** 2025-11-23
**Document Version:** 1.0.0
