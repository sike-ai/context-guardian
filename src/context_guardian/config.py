"""Configuration management for Context Guardian."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """Configuration for Context Guardian daemon."""

    threshold: int = 75
    """Compaction threshold (percentage). Default: 75% (compact before hitting 80% limit)."""

    check_interval: int = 300
    """Check interval in seconds. Default: 300 (5 minutes)."""

    history_file: Path = Path("/tmp/context-guardian.json")
    """File to store check history. Default: /tmp/context-guardian.json."""

    state_file: Path = Path("/tmp/context-guardian-state.json")
    """File to store transient state. Default: /tmp/context-guardian-state.json."""

    log_level: str = "INFO"
    """Logging level. Options: DEBUG, INFO, WARNING, ERROR. Default: INFO."""

    dry_run: bool = False
    """If True, don't actually run compaction (for testing). Default: False."""

    openclaw_timeout: int = 10
    """Timeout for openclaw status command (seconds). Default: 10."""

    compaction_timeout: int = 60
    """Timeout for openclaw compact command (seconds). Default: 60."""

    @staticmethod
    def validate_threshold(value: int) -> None:
        """Validate threshold is in valid range.

        Args:
            value: Threshold percentage to validate.

        Raises:
            ValueError: If threshold is not in [50, 95].
        """
        if not (50 <= value <= 95):
            raise ValueError(f"Threshold must be 50-95%, got {value}%")
