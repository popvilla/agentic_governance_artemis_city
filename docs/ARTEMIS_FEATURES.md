# Artemis Persona Features

This document describes the core features implemented for the Artemis agent persona in Artemis City.

## Overview

The Artemis persona implementation brings the agent to life with:

- **ATP (Artemis Transmission Protocol)** for structured communication
- **Multi-scope instruction hierarchy** for contextual behavior
- **Personality system** with multiple response modes
- **Reflection engine** for synthesizing ideas and finding patterns
- **Semantic tagging** for knowledge organization

## Features

### 1. ATP Protocol System (`agents/atp/`)

The Artemis Transmission Protocol provides structured headers for communication.

#### Components

- **`atp_models.py`**: Data models for ATP messages
  - `ATPMessage`: Core message structure
  - `ATPMode`: Intent modes (Build, Review, Organize, Capture, Synthesize, Commit, Reflect)
  - `ATPPriority`: Priority levels (Critical, High, Normal, Low)
  - `ATPActionType`: Action types (Summarize, Scaffold, Execute, Reflect)

- **`atp_parser.py`**: Parser supporting two syntax formats
  - Hash format: `#Mode: Build #Context: description`
  - Bracket format: `[[Mode]]: Build [[Context]]: description`

- **`atp_validator.py`**: Message validation and quality checks
  - Completeness validation
  - Consistency checks between Mode and ActionType
  - Improvement suggestions

#### Usage Example

```python
from agents.atp import ATPParser, ATPValidator

parser = ATPParser()
message = parser.parse("""
#Mode: Build
#Context: Implementing agent communication
#ActionType: Execute
#Priority: High

Create message protocol with context hashing.
""")

print(f"Mode: {message.mode.value}")
print(f"Context: {message.context}")
print(f"Content: {message.content}")

# Validate
validator = ATPValidator()
result = validator.validate(message)
print(f"Valid: {result.is_valid}")
```

### 2. Instruction Hierarchy (`core/instructions/`)

Cascading instruction loading from multiple scopes with priority-based merging.

#### Scope Priority (ascending)

1. **Global** (~/.codex/instructions.md, ~/.artemis/config.md)
2. **Project Root** (codex.md, WARP.md, .artemis/instructions.md)
3. **Current Directory** (codex.md, instructions.md)
4. **Agent-Specific** (agents/<agent_name>/instructions.md)

#### Components

- **`instruction_loader.py`**: Hierarchical instruction loading
  - Auto-detects project root (looks for .git, WARP.md, etc.)
  - Loads and merges instructions by priority
  - Returns `InstructionSet` with all scopes

- **`instruction_cache.py`**: TTL-based caching
  - 5-minute default TTL
  - Per-directory and per-agent caching
  - Global cache instance available

#### Usage Example

```python
from core.instructions import InstructionLoader, get_global_cache

# Direct loading
loader = InstructionLoader()
instruction_set = loader.load(current_dir="/path/to/project", agent_name="artemis")

print(f"Loaded {len(instruction_set.scopes)} scopes:")
for scope in instruction_set.scopes:
    print(f"  - {scope.level}: {scope.path}")

# Using cache
cache = get_global_cache()
instruction_set = cache.get(agent_name="artemis")
```

### 3. Artemis Personality Layer (`agents/artemis/`)

Implements the core personality traits and behaviors for Artemis.

#### Components

**`persona.py`**: Personality and response patterns

- **Traits**: Reflective, Architectural, Insightful, Predictive, Conversational, Verbose, Poetic
- **Response Modes**: Reflective, Architectural, Conversational, Technical, Poetic
- **Context-aware formatting**: Adjusts verbosity and tone based on query

**`reflection.py`**: Idea synthesis and pattern recognition

- Concept extraction from conversations
- Relationship mapping between concepts
- Narrative generation from concept clusters
- Concept graph for visualization

**`semantic_tagging.py`**: Knowledge organization system

- Tag files, concepts, conversations with semantic labels
- Generate citations (file, concept, agent, URL)
- Find related items through shared tags
- Extract tags and citations from text

#### Usage Example

```python
from agents.artemis import ArtemisPersona, ReflectionEngine, SemanticTagger

# Persona
persona = ArtemisPersona()
context = {"query": "Explain the architecture", "atp_mode": "Review"}
formatted = persona.format_response("The system is...", context)
print(formatted)

# Reflection
engine = ReflectionEngine()
engine.add_conversation("We're building an ATP protocol...")
engine.add_conversation("Artemis oversees governance...")
synthesis = engine.synthesize()
print(synthesis)

# Semantic Tagging
tagger = SemanticTagger()
tagger.tag_item("ATP Protocol", ["protocol", "communication"], "concept")
related = tagger.find_related_items("ATP Protocol")
```

### 4. Enhanced CLI (`interface/codex_cli.py`)

Upgraded CLI with full ATP and instruction support.

#### Features

- ATP header parsing from user input
- Automatic instruction loading for context
- Agent routing with keyword matching
- Artemis persona integration
- Interactive and single-command modes

#### Usage

```bash
# Single command mode
python interface/codex_cli.py "ask artemis about the system"

# With ATP headers
python interface/codex_cli.py "#Mode: Build #Context: CLI test #ActionType: Execute ask artemis"

# Interactive mode
python interface/codex_cli.py
artemis> help me understand ATP
artemis> #Mode: Review #Context: System status check status
artemis> exit
```

#### Command-line Options

- `--no-atp`: Disable ATP parsing
- `--project-root PATH`: Specify project root directory

## Running the Demo

A comprehensive demo script showcases all features:

```bash
# Make executable
chmod +x demo_artemis.py

# Run demo
python demo_artemis.py
```

The demo includes:

1. ATP Protocol Parsing
2. Instruction Hierarchy Loading
3. Artemis Personality & Response Modes
4. Reflection Engine & Concept Synthesis
5. Semantic Tagging & Citations

## Integration Points

### With Memory Layer

The Artemis personality can integrate with the Artemis Agentic Memory Layer:

```python
# Future integration example
from memory.integration import MemoryClient

memory_client = MemoryClient()
artemis_persona = ArtemisPersona()

# Store conversation context
memory_client.store_context(artemis_persona.get_recent_context())

# Load historical context
history = memory_client.load_context(agent="artemis")
for item in history:
    artemis_persona.add_context_memory(item)
```

### With Agent Communication

ATP messages can be used for inter-agent communication:

```python
from agents.atp import ATPParser
from agents.communication import MessageProtocol  # Future implementation

# Agent A sends message
parser = ATPParser()
message = parser.parse("#Mode: Request #Context: Data needed #ActionType: Summarize")

# Agent B receives and processes
protocol = MessageProtocol()
response = protocol.handle_message(message, from_agent="agent_a")
```

## File Structure

```
Artemis-City/
├── agents/
│   ├── atp/                    # ATP protocol system
│   │   ├── __init__.py
│   │   ├── atp_models.py
│   │   ├── atp_parser.py
│   │   └── atp_validator.py
│   └── artemis/                # Artemis personality
│       ├── __init__.py
│       ├── persona.py
│       ├── reflection.py
│       └── semantic_tagging.py
├── core/
│   └── instructions/           # Instruction hierarchy
│       ├── __init__.py
│       ├── instruction_loader.py
│       └── instruction_cache.py
├── interface/
│   └── codex_cli.py           # Enhanced CLI
├── demo_artemis.py            # Feature demonstration
└── ARTEMIS_FEATURES.md        # This document
```

## Configuration

### Global Instructions

Create `~/.artemis/instructions.md` for global Artemis behavior:

```markdown
# Global Artemis Instructions

- Always be reflective and insightful
- Prioritize clarity and architectural thinking
- Use semantic tagging for all file references
- Maintain conversational tone unless technical mode required
```

### Project Instructions

Create `WARP.md` or `codex.md` in project root:

```markdown
# Project: My System

Artemis should:
- Focus on system architecture and design patterns
- Reference the ATP protocol for structured communication
- Track concepts in the reflection engine
- Tag all discussions with #architecture #design
```

### Agent-Specific Instructions

Create `agents/artemis/instructions.md` for agent-level behavior:

```markdown
# Artemis Agent Instructions

Persona Mode: Architectural + Reflective
Verbosity: High for explanations, Normal for responses
Tagging: Always tag with #artemis #governance
```

## Best Practices

### Using ATP Headers

1. Always include Mode, Context, and ActionType for complete messages
2. Use Priority for time-sensitive requests
3. Specify TargetZone for file/directory operations
4. Add SpecialNotes for warnings or dependencies

### Instruction Hierarchy

1. Use global for personal preferences and style
2. Use project for project-specific conventions
3. Use local for component/module-specific rules
4. Use agent for agent behavior customization

### Reflection & Tagging

1. Feed all important conversations to ReflectionEngine
2. Tag concepts immediately as they emerge
3. Use semantic tags consistently across sessions
4. Link related concepts through shared tags

## Testing

Run tests (when implemented):

```bash
# Unit tests for ATP
pytest tests/test_atp.py

# Unit tests for instructions
pytest tests/test_instructions.py

# Integration tests
pytest tests/test_artemis_integration.py
```

## Future Enhancements

1. **Agent Communication Protocol** (`agents/communication/`)
   - Message envelopes with context hashing
   - Symmetric tag acknowledgment (==ref== → ==ref_ack==)
   - Fault awareness for unknown tags

2. **Memory Integration Bridge** (`memory/integration/`)
   - Trust score queries before routing
   - REST client for Memory Layer
   - Context loading from Obsidian vault

3. **Enhanced Reflection**
   - NLP-based concept extraction
   - Temporal pattern recognition
   - Cross-session synthesis

4. **Advanced Tagging**
   - Hierarchical tag taxonomy
   - Tag inference from context
   - Auto-tagging with ML

## Troubleshooting

### ATP Not Parsing

- Ensure tags are formatted correctly: `#Tag: value` or `[[Tag]]: value`
- Check for proper spacing after colons
- Verify tag names match ATP spec (Mode, Context, etc.)

### Instructions Not Loading

- Confirm file exists at expected path
- Check file encoding (must be UTF-8)
- Verify project root is detected correctly
- Clear cache if stale: `reset_global_cache()`

### Persona Not Responding Correctly

- Check context dictionary contains required keys
- Verify query contains mode-triggering keywords
- Ensure persona mode is set appropriately
- Review personality context output

## Contributing

When adding features to Artemis:

1. Follow existing code conventions (Google-style docstrings)
2. Add comprehensive type hints
3. Update this documentation
4. Add examples to demo script
5. Write tests for new functionality

## License

MIT License - See LICENSE file

---

**Version**: 1.0.0  
**Author**: Prinston Palmer  
**Last Updated**: November 23, 2025
