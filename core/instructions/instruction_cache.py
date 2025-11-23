"""Instruction caching system for performance optimization.

Caches loaded instructions per directory and agent combination to avoid
repeated file I/O operations.
"""

import os
import time
from typing import Dict, Optional, Tuple
from .instruction_loader import InstructionSet, InstructionLoader


class InstructionCache:
    """Cache for loaded instruction sets.
    
    Implements TTL (time-to-live) based caching to balance performance
    with freshness of instruction data.
    """
    
    def __init__(self, ttl_seconds: int = 300):
        """Initialize instruction cache.
        
        Args:
            ttl_seconds: Time-to-live for cache entries in seconds (default 5 minutes)
        """
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Tuple[InstructionSet, float]] = {}
        self._loader = InstructionLoader()
    
    def get(
        self, 
        current_dir: Optional[str] = None,
        agent_name: Optional[str] = None,
        force_reload: bool = False
    ) -> InstructionSet:
        """Get instruction set from cache or load fresh.
        
        Args:
            current_dir: Current working directory
            agent_name: Agent name for agent-specific instructions
            force_reload: If True, bypass cache and reload from disk
            
        Returns:
            InstructionSet with loaded instructions
        """
        current_dir = current_dir or os.getcwd()
        cache_key = self._make_cache_key(current_dir, agent_name)
        
        # Check cache if not forcing reload
        if not force_reload and cache_key in self._cache:
            instruction_set, cached_time = self._cache[cache_key]
            
            # Check if cache entry is still valid
            if time.time() - cached_time < self.ttl_seconds:
                return instruction_set
            else:
                # Cache expired, remove entry
                del self._cache[cache_key]
        
        # Load fresh instructions
        instruction_set = self._loader.load(current_dir, agent_name)
        
        # Cache the result
        self._cache[cache_key] = (instruction_set, time.time())
        
        return instruction_set
    
    def invalidate(
        self, 
        current_dir: Optional[str] = None, 
        agent_name: Optional[str] = None
    ) -> None:
        """Invalidate cache entry for specific directory/agent combination.
        
        Args:
            current_dir: Directory to invalidate
            agent_name: Agent name to invalidate
        """
        current_dir = current_dir or os.getcwd()
        cache_key = self._make_cache_key(current_dir, agent_name)
        if cache_key in self._cache:
            del self._cache[cache_key]
    
    def clear(self) -> None:
        """Clear entire cache."""
        self._cache.clear()
    
    def get_stats(self) -> Dict:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        current_time = time.time()
        valid_entries = sum(
            1 for _, cached_time in self._cache.values()
            if current_time - cached_time < self.ttl_seconds
        )
        
        return {
            "total_entries": len(self._cache),
            "valid_entries": valid_entries,
            "expired_entries": len(self._cache) - valid_entries,
            "ttl_seconds": self.ttl_seconds
        }
    
    @staticmethod
    def _make_cache_key(current_dir: str, agent_name: Optional[str]) -> str:
        """Create cache key from directory and agent name.
        
        Args:
            current_dir: Current directory path
            agent_name: Optional agent name
            
        Returns:
            Cache key string
        """
        # Normalize path for consistent keys
        normalized_dir = os.path.normpath(current_dir)
        agent_part = f":{agent_name}" if agent_name else ":_default"
        return f"{normalized_dir}{agent_part}"


# Global cache instance for shared use
_global_cache = None


def get_global_cache(ttl_seconds: int = 300) -> InstructionCache:
    """Get or create global instruction cache instance.
    
    Args:
        ttl_seconds: TTL for cache entries if creating new cache
        
    Returns:
        Global InstructionCache instance
    """
    global _global_cache
    if _global_cache is None:
        _global_cache = InstructionCache(ttl_seconds)
    return _global_cache


def reset_global_cache() -> None:
    """Reset global cache instance."""
    global _global_cache
    if _global_cache is not None:
        _global_cache.clear()
    _global_cache = None
