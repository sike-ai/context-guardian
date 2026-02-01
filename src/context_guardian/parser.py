"""Context usage parser for OpenClaw status output."""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ContextLevel(Enum):
    """Context severity level."""

    HEALTHY = (0, "✓")
    ELEVATED = (1, "●")
    WARNING = (2, "⚠")
    CRITICAL = (3, "🚨")


@dataclass
class ContextUsage:
    """Parsed context usage information."""

    used_tokens: int
    """Tokens currently used."""

    limit_tokens: int
    """Token limit."""

    percentage: int
    """Usage percentage (0-100)."""

    @property
    def level(self) -> ContextLevel:
        """Determine context severity level.

        Returns:
            ContextLevel based on usage percentage.
        """
        if self.percentage < 60:
            return ContextLevel.HEALTHY
        elif self.percentage < 80:
            return ContextLevel.ELEVATED
        elif self.percentage < 90:
            return ContextLevel.WARNING
        else:
            return ContextLevel.CRITICAL


def parse_token_count(value: str, unit: str) -> int:
    """Convert token count with unit to integer.

    Args:
        value: Numeric value (e.g., "84.5").
        unit: Unit ('k' for thousands, 'm' for millions).

    Returns:
        Total token count as integer.
    """
    numeric = float(value.strip())
    multiplier = {"k": 1000, "m": 1_000_000}.get(unit.lower(), 1)
    return int(numeric * multiplier)


def parse_openclaw_status(output: str) -> Optional[ContextUsage]:
    """Parse OpenClaw status output to extract context usage.

    Looks for pattern: "84.5k/200k (42%)" or similar in the output.

    Args:
        output: Combined stdout+stderr from openclaw status command.

    Returns:
        ContextUsage if pattern found, None otherwise.
    """
    # Match pattern: "123k/200k (45%)" or "1.5m/2m (75%)"
    pattern = r"([\d.]+)([km])/([\d.]+)([km])\s+\((\d+)%\)"
    match = re.search(pattern, output, re.IGNORECASE)

    if not match:
        return None

    used_str, used_unit, limit_str, limit_unit, percent_str = match.groups()

    used = parse_token_count(used_str, used_unit)
    limit = parse_token_count(limit_str, limit_unit)
    percent = int(percent_str)

    return ContextUsage(
        used_tokens=used,
        limit_tokens=limit,
        percentage=percent,
    )
