"""Trust interface for memory operations.

This module provides trust-aware memory access, filtering operations
based on agent trust scores and trust decay model.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List


class TrustLevel(Enum):
    """Trust level categories."""

    FULL = "full"  # Unrestricted access
    HIGH = "high"  # Most operations allowed
    MEDIUM = "medium"  # Limited operations
    LOW = "low"  # Read-only
    UNTRUSTED = "untrusted"  # No access


@dataclass
class TrustScore:
    """Trust score for an entity (agent, memory, protocol).

    Attributes:
        entity_id: Identifier for the entity
        entity_type: Type of entity (agent, memory, protocol)
        score: Current trust score (0.0-1.0)
        level: Trust level category
        last_updated: When score was last updated
        decay_rate: Natural decay rate per day
        reinforcement_events: Count of positive events
        penalty_events: Count of negative events
    """

    entity_id: str
    entity_type: str
    score: float
    level: TrustLevel
    last_updated: datetime
    decay_rate: float = 0.01  # 1% per day default
    reinforcement_events: int = 0
    penalty_events: int = 0

    def apply_decay(self) -> float:
        """Apply natural decay based on time since last update.

        Returns:
            New score after decay
        """
        days_elapsed = (datetime.now() - self.last_updated).days
        decayed_score = self.score * (1 - self.decay_rate) ** days_elapsed

        # Don't decay below certain threshold based on level
        min_score = {
            TrustLevel.FULL: 0.9,
            TrustLevel.HIGH: 0.7,
            TrustLevel.MEDIUM: 0.5,
            TrustLevel.LOW: 0.3,
            TrustLevel.UNTRUSTED: 0.0,
        }.get(self.level, 0.0)

        return max(decayed_score, min_score)

    def reinforce(self, amount: float = 0.05) -> float:
        """Reinforce trust score (successful action).

        Args:
            amount: Amount to increase score

        Returns:
            New score after reinforcement
        """
        self.score = min(1.0, self.score + amount)
        self.reinforcement_events += 1
        self.last_updated = datetime.now()
        self._update_level()
        return self.score

    def penalize(self, amount: float = 0.1) -> float:
        """Penalize trust score (failed action).

        Args:
            amount: Amount to decrease score

        Returns:
            New score after penalty
        """
        self.score = max(0.0, self.score - amount)
        self.penalty_events += 1
        self.last_updated = datetime.now()
        self._update_level()
        return self.score

    def _update_level(self):
        """Update trust level based on current score."""
        if self.score >= 0.9:
            self.level = TrustLevel.FULL
        elif self.score >= 0.7:
            self.level = TrustLevel.HIGH
        elif self.score >= 0.5:
            self.level = TrustLevel.MEDIUM
        elif self.score >= 0.3:
            self.level = TrustLevel.LOW
        else:
            self.level = TrustLevel.UNTRUSTED


class TrustInterface:
    """Interface for trust-aware memory operations.

    Manages trust scores for agents and determines access
    permissions for memory operations based on trust levels.
    """

    # Default trust scores for new entities
    DEFAULT_AGENT_TRUST = 0.8  # High trust for new agents
    DEFAULT_MEMORY_TRUST = 0.7  # Medium-high trust for new memories

    # Operation permission matrix
    OPERATION_PERMISSIONS = {
        TrustLevel.FULL: ['read', 'write', 'delete', 'search', 'tag', 'update'],
        TrustLevel.HIGH: ['read', 'write', 'search', 'tag', 'update'],
        TrustLevel.MEDIUM: ['read', 'write', 'search', 'tag'],
        TrustLevel.LOW: ['read', 'search'],
        TrustLevel.UNTRUSTED: [],
    }

    def __init__(self):
        """Initialize trust interface."""
        self.trust_scores: Dict[str, TrustScore] = {}
        self._initialize_default_agents()

    def _initialize_default_agents(self):
        """Initialize trust scores for known agents."""
        # Core agents start with high trust
        core_agents = {
            'artemis': (0.95, TrustLevel.FULL),
            'pack_rat': (0.85, TrustLevel.HIGH),
            'codex_daemon': (0.85, TrustLevel.HIGH),
            'copilot': (0.80, TrustLevel.HIGH),
        }

        for agent_id, (score, level) in core_agents.items():
            self.trust_scores[agent_id] = TrustScore(
                entity_id=agent_id,
                entity_type='agent',
                score=score,
                level=level,
                last_updated=datetime.now(),
            )

    def get_trust_score(self, entity_id: str, entity_type: str = 'agent') -> TrustScore:
        """Get trust score for an entity.

        Creates new score if entity doesn't exist.

        Args:
            entity_id: Entity identifier
            entity_type: Type of entity

        Returns:
            TrustScore for the entity
        """
        key = f"{entity_type}:{entity_id}"

        if key not in self.trust_scores:
            # Create new trust score
            default_score = (
                self.DEFAULT_AGENT_TRUST if entity_type == 'agent' else self.DEFAULT_MEMORY_TRUST
            )

            self.trust_scores[key] = TrustScore(
                entity_id=entity_id,
                entity_type=entity_type,
                score=default_score,
                level=TrustLevel.HIGH,
                last_updated=datetime.now(),
            )

        # Apply decay
        trust_score = self.trust_scores[key]
        trust_score.score = trust_score.apply_decay()

        return trust_score

    def can_perform_operation(
        self, entity_id: str, operation: str, entity_type: str = 'agent'
    ) -> bool:
        """Check if entity can perform an operation.

        Args:
            entity_id: Entity identifier
            operation: Operation to check (read, write, delete, etc.)
            entity_type: Type of entity

        Returns:
            True if operation is allowed, False otherwise
        """
        trust_score = self.get_trust_score(entity_id, entity_type)
        allowed_operations = self.OPERATION_PERMISSIONS.get(trust_score.level, [])
        return operation in allowed_operations

    def record_success(self, entity_id: str, entity_type: str = 'agent', amount: float = 0.02):
        """Record successful operation (reinforces trust).

        Args:
            entity_id: Entity identifier
            entity_type: Type of entity
            amount: Amount to reinforce
        """
        trust_score = self.get_trust_score(entity_id, entity_type)
        trust_score.reinforce(amount)

    def record_failure(self, entity_id: str, entity_type: str = 'agent', amount: float = 0.05):
        """Record failed operation (penalizes trust).

        Args:
            entity_id: Entity identifier
            entity_type: Type of entity
            amount: Amount to penalize
        """
        trust_score = self.get_trust_score(entity_id, entity_type)
        trust_score.penalize(amount)

    def get_trust_report(self) -> Dict:
        """Generate trust report for all entities.

        Returns:
            Dictionary with trust statistics
        """
        by_level = {}
        for trust_score in self.trust_scores.values():
            level = trust_score.level.value
            if level not in by_level:
                by_level[level] = []
            by_level[level].append(
                {
                    'id': trust_score.entity_id,
                    'type': trust_score.entity_type,
                    'score': round(trust_score.score, 3),
                    'reinforcements': trust_score.reinforcement_events,
                    'penalties': trust_score.penalty_events,
                }
            )

        return {
            'total_entities': len(self.trust_scores),
            'by_level': by_level,
            'timestamp': datetime.now().isoformat(),
        }

    def filter_by_trust(
        self, items: List[Dict], min_trust_level: TrustLevel = TrustLevel.MEDIUM
    ) -> List[Dict]:
        """Filter items by minimum trust level.

        Assumes items have 'entity_id' and 'entity_type' fields.

        Args:
            items: List of items to filter
            min_trust_level: Minimum trust level required

        Returns:
            Filtered list of items
        """
        min_score = {
            TrustLevel.FULL: 0.9,
            TrustLevel.HIGH: 0.7,
            TrustLevel.MEDIUM: 0.5,
            TrustLevel.LOW: 0.3,
            TrustLevel.UNTRUSTED: 0.0,
        }[min_trust_level]

        filtered = []
        for item in items:
            entity_id = item.get('entity_id')
            entity_type = item.get('entity_type', 'agent')

            if entity_id:
                trust_score = self.get_trust_score(entity_id, entity_type)
                if trust_score.score >= min_score:
                    filtered.append(item)

        return filtered


# Global trust interface instance
_global_trust_interface = None


def get_trust_interface() -> TrustInterface:
    """Get or create global trust interface instance.

    Returns:
        Global TrustInterface instance
    """
    global _global_trust_interface
    if _global_trust_interface is None:
        _global_trust_interface = TrustInterface()
    return _global_trust_interface
