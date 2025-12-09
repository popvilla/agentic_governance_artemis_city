from abc import ABC, abstractmethod
import os
import json
import time

class MemoryBackend(ABC):
    @abstractmethod
    def write(self, content, metadata=None):
        pass
        
    @abstractmethod
    def read(self, query):
        pass

class FileMemoryBackend(MemoryBackend):
    def __init__(self, base_path="memory_store"):
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            
    def write(self, content, metadata=None):
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
        # Simplistic read for now
        results = []
        if not os.path.exists(self.base_path):
            return results
            
        for f in os.listdir(self.base_path):
            if f.endswith(".json"):
                try:
                    with open(os.path.join(self.base_path, f), 'r') as file:
                        data = json.load(file)
                        # Very basic search: string match in content
                        if query.lower() in str(data.get("content", "")).lower():
                            results.append(data)
                except Exception:
                    continue
        return results

class MemoryBus:
    def __init__(self, backend_type="file"):
        if backend_type == "file":
            self.backend = FileMemoryBackend()
        else:
            # Fallback or other backends
            print(f"[Memory] Unknown backend {backend_type}, defaulting to file.")
            self.backend = FileMemoryBackend()
            
    def write(self, content, metadata=None):
        return self.backend.write(content, metadata)
        
    def read(self, query):
        return self.backend.read(query)
