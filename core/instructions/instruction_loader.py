"""Instruction hierarchy loader for multi-scope configuration.

This module implements cascading instruction loading from multiple scopes:
global → project root → current directory → agent-specific
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class InstructionScope:
    """Represents a single instruction scope with metadata.
    
    Attributes:
        level: Scope level (global, project, local, agent)
        path: File path where instructions were loaded from
        content: Raw instruction content
        priority: Priority level (higher = higher precedence)
    """
    level: str
    path: str
    content: str
    priority: int
    
    def __str__(self) -> str:
        return f"[{self.level}] {self.path} (priority: {self.priority})"


@dataclass
class InstructionSet:
    """Collection of instructions from multiple scopes.
    
    Attributes:
        scopes: List of instruction scopes in priority order
        merged_content: Combined instructions with scope markers
        metadata: Additional contextual information
    """
    scopes: List[InstructionScope] = field(default_factory=list)
    merged_content: str = ""
    metadata: Dict = field(default_factory=dict)
    
    def add_scope(self, scope: InstructionScope) -> None:
        """Add an instruction scope and re-sort by priority."""
        self.scopes.append(scope)
        self.scopes.sort(key=lambda s: s.priority)
    
    def get_merged(self, include_markers: bool = True) -> str:
        """Get merged instruction content.
        
        Args:
            include_markers: If True, add scope markers to content
            
        Returns:
            Combined instruction content
        """
        if not self.scopes:
            return ""
        
        if not include_markers:
            return "\n\n".join(s.content for s in self.scopes)
        
        parts = []
        for scope in self.scopes:
            parts.append(f"# --- Instructions from {scope.level} ({scope.path}) ---")
            parts.append(scope.content)
            parts.append("")
        
        return "\n".join(parts)
    
    def __str__(self) -> str:
        scope_list = "\n".join(f"  {s}" for s in self.scopes)
        return f"InstructionSet with {len(self.scopes)} scopes:\n{scope_list}"


class InstructionLoader:
    """Loads and merges instructions from multiple hierarchical scopes.
    
    Scope priority (ascending):
    1. Global (~/.codex/instructions.md, ~/.artemis/config.md)
    2. Project root (codex.md, WARP.md, .artemis/instructions.md)
    3. Current directory (codex.md, instructions.md)
    4. Agent-specific (agents/<agent_name>/instructions.md)
    """
    
    # Default instruction file names by scope
    GLOBAL_FILES = [
        "~/.codex/instructions.md",
        "~/.artemis/config.md",
        "~/.artemis/instructions.md"
    ]
    
    PROJECT_FILES = [
        "codex.md",
        "WARP.md",
        ".codex/instructions.md",
        ".artemis/instructions.md"
    ]
    
    LOCAL_FILES = [
        "codex.md",
        "instructions.md",
        ".instructions.md"
    ]
    
    def __init__(self, project_root: Optional[str] = None):
        """Initialize instruction loader.
        
        Args:
            project_root: Root directory of the project. If None, will be auto-detected.
        """
        self.project_root = self._find_project_root(project_root)
    
    def load(
        self, 
        current_dir: Optional[str] = None, 
        agent_name: Optional[str] = None
    ) -> InstructionSet:
        """Load instructions from all applicable scopes.
        
        Args:
            current_dir: Current working directory. Defaults to os.getcwd()
            agent_name: Specific agent name for agent-level instructions
            
        Returns:
            InstructionSet with all loaded scopes
        """
        current_dir = current_dir or os.getcwd()
        instruction_set = InstructionSet()
        
        # Load global instructions (priority 1)
        global_scope = self._load_global_instructions()
        if global_scope:
            instruction_set.add_scope(global_scope)
        
        # Load project root instructions (priority 2)
        if self.project_root:
            project_scope = self._load_project_instructions()
            if project_scope:
                instruction_set.add_scope(project_scope)
        
        # Load local (current directory) instructions (priority 3)
        local_scope = self._load_local_instructions(current_dir)
        if local_scope:
            instruction_set.add_scope(local_scope)
        
        # Load agent-specific instructions (priority 4)
        if agent_name:
            agent_scope = self._load_agent_instructions(agent_name)
            if agent_scope:
                instruction_set.add_scope(agent_scope)
        
        # Build merged content
        instruction_set.merged_content = instruction_set.get_merged()
        instruction_set.metadata = {
            "project_root": self.project_root,
            "current_dir": current_dir,
            "agent_name": agent_name,
            "scope_count": len(instruction_set.scopes)
        }
        
        return instruction_set
    
    def _load_global_instructions(self) -> Optional[InstructionScope]:
        """Load global-level instructions from home directory."""
        for file_pattern in self.GLOBAL_FILES:
            file_path = os.path.expanduser(file_pattern)
            content = self._read_file(file_path)
            if content:
                return InstructionScope(
                    level="global",
                    path=file_path,
                    content=content,
                    priority=1
                )
        return None
    
    def _load_project_instructions(self) -> Optional[InstructionScope]:
        """Load project root-level instructions."""
        if not self.project_root:
            return None
        
        for filename in self.PROJECT_FILES:
            file_path = os.path.join(self.project_root, filename)
            content = self._read_file(file_path)
            if content:
                return InstructionScope(
                    level="project",
                    path=file_path,
                    content=content,
                    priority=2
                )
        return None
    
    def _load_local_instructions(self, current_dir: str) -> Optional[InstructionScope]:
        """Load current directory-level instructions."""
        # Skip if current_dir is same as project_root
        if self.project_root and os.path.samefile(current_dir, self.project_root):
            return None
        
        for filename in self.LOCAL_FILES:
            file_path = os.path.join(current_dir, filename)
            content = self._read_file(file_path)
            if content:
                return InstructionScope(
                    level="local",
                    path=file_path,
                    content=content,
                    priority=3
                )
        return None
    
    def _load_agent_instructions(self, agent_name: str) -> Optional[InstructionScope]:
        """Load agent-specific instructions."""
        if not self.project_root:
            return None
        
        # Check agents/<agent_name>/instructions.md
        agent_dir = os.path.join(self.project_root, "agents", agent_name)
        for filename in ["instructions.md", f"{agent_name}.md"]:
            file_path = os.path.join(agent_dir, filename)
            content = self._read_file(file_path)
            if content:
                return InstructionScope(
                    level=f"agent:{agent_name}",
                    path=file_path,
                    content=content,
                    priority=4
                )
        return None
    
    @staticmethod
    def _read_file(file_path: str) -> Optional[str]:
        """Read file content, returning None if file doesn't exist.
        
        Args:
            file_path: Path to file to read
            
        Returns:
            File content or None
        """
        try:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except (IOError, OSError):
            pass
        return None
    
    @staticmethod
    def _find_project_root(explicit_root: Optional[str] = None) -> Optional[str]:
        """Find project root by looking for marker files.
        
        Args:
            explicit_root: Explicitly provided root directory
            
        Returns:
            Project root path or None if not found
        """
        if explicit_root:
            return os.path.abspath(explicit_root)
        
        # Start from current directory and walk up
        current = Path.cwd()
        
        # Marker files that indicate project root
        markers = ['.git', '.artemis', 'codex.md', 'WARP.md', 'pyproject.toml', 'package.json']
        
        # Walk up directory tree
        for parent in [current] + list(current.parents):
            for marker in markers:
                if (parent / marker).exists():
                    return str(parent)
        
        return None
    
    def get_active_scopes(self, current_dir: Optional[str] = None) -> List[str]:
        """Get list of active instruction file paths.
        
        Args:
            current_dir: Directory to check for local instructions
            
        Returns:
            List of file paths that would be loaded
        """
        instruction_set = self.load(current_dir)
        return [scope.path for scope in instruction_set.scopes]
