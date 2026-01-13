"""ATP (Artemis Transmission Protocol) validator.

This module validates ATP messages for completeness, consistency, and quality.
"""

from typing import List

from .atp_models import ATPActionType, ATPMessage, ATPMode


class ValidationResult:
    """Result of ATP message validation."""

    def __init__(self):
        """Initialize validation result."""
        self.is_valid = True
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.suggestions: List[str] = []

    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)

    def add_error(self, message: str) -> None:
        """Add an error message and mark as invalid."""
        self.errors.append(message)
        self.is_valid = False

    def add_suggestion(self, message: str) -> None:
        """Add a suggestion for improvement."""
        self.suggestions.append(message)

    @property
    def has_issues(self) -> bool:
        """Check if there are any warnings or errors."""
        return len(self.warnings) > 0 or len(self.errors) > 0

    def __str__(self) -> str:
        """Human-readable validation result."""
        parts = []
        if self.errors:
            parts.append(f"Errors ({len(self.errors)}):")
            for error in self.errors:
                parts.append(f"  - {error}")
        if self.warnings:
            parts.append(f"Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                parts.append(f"  - {warning}")
        if self.suggestions:
            parts.append(f"Suggestions ({len(self.suggestions)}):")
            for suggestion in self.suggestions:
                parts.append(f"  - {suggestion}")

        if not parts:
            return "Validation passed with no issues"

        return "\n".join(parts)


class ATPValidator:
    """Validator for ATP messages.

    Checks message completeness, consistency, and provides suggestions
    for improving message quality.
    """

    # Minimum recommended content length
    MIN_CONTENT_LENGTH = 10

    # Maximum recommended content length (for single messages)
    MAX_CONTENT_LENGTH = 2000

    def __init__(self, strict: bool = False):
        """Initialize ATP validator.

        Args:
            strict: If True, enforce stricter validation rules
        """
        self.strict = strict

    def validate(self, message: ATPMessage) -> ValidationResult:
        """Validate an ATP message.

        Args:
            message: ATPMessage to validate

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult()

        # Check for ATP headers presence
        if not message.has_atp_headers:
            if self.strict:
                result.add_error("No ATP headers found in message")
            else:
                result.add_suggestion("Consider using ATP headers for structured communication")

        # Check for completeness (Mode, Context, ActionType)
        if message.has_atp_headers and not message.is_complete:
            missing = []
            if message.mode == ATPMode.UNKNOWN:
                missing.append("Mode")
            if message.context is None:
                missing.append("Context")
            if message.action_type == ATPActionType.UNKNOWN:
                missing.append("ActionType")

            if self.strict:
                result.add_error(f"Incomplete ATP headers: missing {', '.join(missing)}")
            else:
                result.add_warning(f"Recommended ATP headers missing: {', '.join(missing)}")

        # Validate content presence
        if not message.content or len(message.content.strip()) == 0:
            result.add_error("Message content is empty")
        elif len(message.content) < self.MIN_CONTENT_LENGTH:
            result.add_warning(f"Message content is very short ({len(message.content)} chars)")
        elif len(message.content) > self.MAX_CONTENT_LENGTH:
            result.add_suggestion("Consider breaking long message into multiple ATP messages")

        # Check Mode/ActionType consistency
        if message.has_atp_headers:
            self._validate_mode_action_consistency(message, result)

        # Check TargetZone format
        if message.target_zone:
            self._validate_target_zone(message.target_zone, result)

        return result

    def _validate_mode_action_consistency(
        self, message: ATPMessage, result: ValidationResult
    ) -> None:
        """Check if Mode and ActionType are logically consistent.

        Args:
            message: ATPMessage to check
            result: ValidationResult to add warnings to
        """
        mode = message.mode
        action = message.action_type

        # Define expected action types for each mode
        expected_actions = {
            ATPMode.BUILD: [ATPActionType.SCAFFOLD, ATPActionType.EXECUTE],
            ATPMode.REVIEW: [ATPActionType.SUMMARIZE, ATPActionType.REFLECT],
            ATPMode.ORGANIZE: [ATPActionType.SCAFFOLD, ATPActionType.EXECUTE],
            ATPMode.CAPTURE: [ATPActionType.SUMMARIZE],
            ATPMode.SYNTHESIZE: [ATPActionType.SUMMARIZE, ATPActionType.REFLECT],
            ATPMode.COMMIT: [ATPActionType.EXECUTE],
            ATPMode.REFLECT: [ATPActionType.REFLECT, ATPActionType.SUMMARIZE],
        }

        if (
            mode in expected_actions
            and action not in expected_actions[mode]
            and action != ATPActionType.UNKNOWN
        ):
            result.add_suggestion(
                f"Mode '{mode.value}' typically uses "
                f"{', '.join(a.value for a in expected_actions[mode])} actions, "
                f"but '{action.value}' was specified"
            )

    def _validate_target_zone(self, target_zone: str, result: ValidationResult) -> None:
        """Validate TargetZone format.

        Args:
            target_zone: Target zone string to validate
            result: ValidationResult to add warnings to
        """
        # Check if it looks like a path
        if not ('/' in target_zone or '\\' in target_zone):
            result.add_suggestion("TargetZone should typically be a file path or project location")

        # Check for relative vs absolute paths
        if not target_zone.startswith('/') and not target_zone.startswith('~'):
            result.add_suggestion(
                "Consider using absolute paths or home-relative paths (~/) in TargetZone"
            )

    def suggest_improvements(self, message: ATPMessage) -> List[str]:
        """Suggest improvements for an ATP message.

        Args:
            message: ATPMessage to analyze

        Returns:
            List of improvement suggestions
        """
        suggestions = []

        # Suggest adding ATP headers if none present
        if not message.has_atp_headers:
            suggestions.append(
                "Add ATP headers (Mode, Context, ActionType) for structured communication"
            )

        # Suggest filling optional fields
        if message.has_atp_headers:
            if not message.target_zone:
                suggestions.append("Consider adding TargetZone to specify project location")
            if not message.special_notes:
                suggestions.append(
                    "Use SpecialNotes for warnings, dependencies, or special instructions"
                )

        # Suggest context improvements
        if message.context and len(message.context) < 10:
            suggestions.append("Context should be more descriptive (aim for 1-2 sentences)")

        return suggestions
