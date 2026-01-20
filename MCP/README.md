# Artemis City MCP - Vector Memory Module

Semantic search and vector storage for the Artemis agentic memory system using Supabase pgvector.

## Features

- **Semantic Search**: Find memories by meaning, not just keywords
- **Supabase pgvector**: Production-ready vector database
- **OpenAI Embeddings**: text-embedding-3-small (1536 dimensions)
- **Hebbian Integration**: ATP-compatible retrieval with learned weights
- **MemoryBus Compatible**: Drop-in replacement for file backend

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
export SUPABASE_URL=https://lkyeffgxichvbpxmrgir.supabase.co
export SUPABASE_KEY=sb_publishable_7xivO1svcjiU1vqugJLPLg_wCzqspN
export OPENAI_API_KEY="your-openai-key"
```

### 3. Create Supabase Tables

Run the SQL setup script in your Supabase SQL editor:

```python
from MCP.src.vector_store import get_setup_sql
print(get_setup_sql())
```

Or copy from `src/vector_store.py` (see `SUPABASE_SETUP_SQL`).

## Usage

### Basic Usage

```python
from MCP.src.vector_store import VectorStore

store = VectorStore()

# Store a memory
doc_id = store.store(
    content="Artemis completed governance review of Pack Rat courier service",
    metadata={"agent": "artemis", "action": "review", "target": "packrat"}
)

# Semantic search
results = store.search("governance audit", limit=5)
for doc in results:
    print(f"{doc.similarity:.2f}: {doc.content}")
```

### With MemoryBus

```python
from app.codex.memory_bus import MemoryBus

# Use vector backend for semantic search
memory = MemoryBus(backend_type="vector")

# Write (stores with embedding)
memory.write("Important policy decision", {"agent": "artemis"})

# Read (semantic search)
results = memory.read("governance policies")
```

Alternatively, use VectorMemoryBackend directly:

```python
from app.codex.memory_bus import MemoryBus
from MCP.src.vector_store import VectorMemoryBackend

# Create vector backend and pass to MemoryBus
vector_backend = VectorMemoryBackend()
memory = MemoryBus(backend=vector_backend)

# Same API
memory.write("Important policy decision", {"agent": "artemis"})
results = memory.read("governance policies")
```

### Hebbian-Influenced Retrieval

```python
from MCP.src.vector_store import HebbianVectorStore

store = HebbianVectorStore(
    hebbian_weights={
        "artemis-copilot": 0.8,
        "artemis-packrat": 0.3,
    },
    hebbian_influence=0.3  # 30% Hebbian, 70% semantic
)

# Search as Copilot - Artemis memories weighted higher
results = store.search_with_hebbian(
    query="review process",
    requesting_agent="copilot",
    limit=5
)
```

## Architecture

```
MCP/
├── src/
│   ├── __init__.py
│   └── vector_store.py    # Main module
├── requirements.txt
└── README.md
```

### Integration Points

- **MemoryBus**: `VectorMemoryBackend` adapter
- **MemoryClient**: Complements Obsidian MCP for structured notes
- **ATP Prototype**: `HebbianVectorStore` for learned retrieval

## API Reference

### VectorStore

| Method | Description |
|--------|-------------|
| `store(content, metadata)` | Store with embedding |
| `store_batch(contents, metadatas)` | Batch store |
| `search(query, limit, filter_metadata)` | Semantic search |
| `search_by_agent(query, agent_name)` | Filter by agent |
| `delete(ids)` | Delete by ID |
| `get(ids)` | Get by ID |

### HebbianVectorStore

| Method | Description |
|--------|-------------|
| `search_with_hebbian(query, requesting_agent)` | Hebbian-weighted search |
| `update_hebbian_weight(agent1, agent2, delta)` | Strengthen connection |
| `get_hebbian_weight(agent1, agent2)` | Get connection strength |

## Schema

```sql
CREATE TABLE memory_vectors (
    id UUID PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## License

Part of Artemis City - Systems Architecture by Prinston Palmer
