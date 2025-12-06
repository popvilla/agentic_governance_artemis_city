"""ATP (Artemis Transmission Protocol) data models.

This module defines the core data structures for ATP messages, enabling
structured communication between agents and users with clear intent signals.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class ATPMode(Enum):
    """ATP Mode values defining overall intent."""

    BUILD = "Build"
    REVIEW = "Review"
    ORGANIZE = "Organize"
    CAPTURE = "Capture"
    SYNTHESIZE = "Synthesize"
    COMMIT = "Commit"
    REFLECT = "Reflect"
    UNKNOWN = "Unknown"


class ATPPriority(Enum):
    """ATP Priority levels for task urgency."""

    CRITICAL = "Critical"
    HIGH = "High"
    NORMAL = "Normal"
    LOW = "Low"
    UNKNOWN = "Unknown"


class ATPActionType(Enum):
    """ATP Action types defining expected response."""

    SUMMARIZE = "Summarize"
    SCAFFOLD = "Scaffold"
    EXECUTE = "Execute"
    REFLECT = "Reflect"
    UNKNOWN = "Unknown"


@dataclass
class ATPMessage:
    """Structured ATP message with protocol-defined fields.

    Attributes:
        mode: Overall intent of the message
        context: Brief mission goal or purpose
        priority: Urgency level
        action_type: Expected response type
        target_zone: Project/folder area for the work
        special_notes: Unusual instructions or warnings
        content: The actual message content (post-ATP header)
        raw_input: Original unprocessed input
        timestamp: When the message was created
        metadata: Additional contextual data
    """

    mode: ATPMode = ATPMode.UNKNOWN
    context: Optional[str] = None
    priority: ATPPriority = ATPPriority.NORMAL
    action_type: ATPActionType = ATPActionType.UNKNOWN
    target_zone: Optional[str] = None
    special_notes: Optional[str] = None
    content: str = ""
    raw_input: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def has_atp_headers(self) -> bool:
        """Check if message has any ATP headers parsed."""
        return (
            self.mode != ATPMode.UNKNOWN
            or self.context is not None
            or self.action_type != ATPActionType.UNKNOWN
            or self.target_zone is not None
        )

    @property
    def is_complete(self) -> bool:
        """Check if message has minimum required ATP fields."""
        return (
            self.mode != ATPMode.UNKNOWN
            and self.context is not None
            and self.action_type != ATPActionType.UNKNOWN
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert ATP message to dictionary format."""
        return {
            "mode": self.mode.value,
            "context": self.context,
            "priority": self.priority.value,
            "action_type": self.action_type.value,
            "target_zone": self.target_zone,
            "special_notes": self.special_notes,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "has_atp_headers": self.has_atp_headers,
            "is_complete": self.is_complete,
        }

    def __str__(self) -> str:
        """Human-readable string representation."""
        parts = []
        if self.mode != ATPMode.UNKNOWN:
            parts.append(f"Mode: {self.mode.value}")
        if self.context:
            parts.append(f"Context: {self.context}")
        if self.priority != ATPPriority.NORMAL:
            parts.append(f"Priority: {self.priority.value}")
        if self.action_type != ATPActionType.UNKNOWN:
            parts.append(f"Action: {self.action_type.value}")
        if self.target_zone:
            parts.append(f"Target: {self.target_zone}")
        if self.special_notes:
            parts.append(f"Notes: {self.special_notes}")

        header = " | ".join(parts) if parts else "No ATP headers"
        return (
            f"[ATP] {header}\nContent: {self.content[:100]}..."
            if len(self.content) > 100
            else f"[ATP] {header}\nContent: {self.content}"
        )
