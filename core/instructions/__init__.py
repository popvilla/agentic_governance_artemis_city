"""Instruction hierarchy system for multi-scope configuration.

This module provides cascading instruction loading from global, project,
local, and agent-specific scopes.
"""

from .instruction_loader import (
    InstructionLoader,
    InstructionSet,
    InstructionScope
)
from .instruction_cache import (
    InstructionCache,
    get_global_cache,
    reset_global_cache
)

__all__ = [
    'InstructionLoader',
    'InstructionSet',
    'InstructionScope',
    'InstructionCache',
    'get_global_cache',
    'reset_global_cache',
]
