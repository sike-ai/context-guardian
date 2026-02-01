"""Context Guardian daemon - proactive context management."""

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

from context_guardian.config import Config
from context_guardian.logger import get_logger
from context_guardian.parser import ContextUsage, parse_openclaw_status


class ContextGuardian:
    """Daemon for monitoring and managing OpenClaw context usage."""

    def __init__(self, config: Optional[Config] = None) -> None:
        """Initialize Context Guardian.

        Args:
            config: Configuration object. If None, uses default config.
        """
        self.config = config or Config()
        self.logger = get_logger(__name__)
        self.history: list[dict] = []
        self._load_history()

    def _load_history(self) -> None:
        """Load check history from file."""
        if not self.config.history_file.exists():
            return

        try:
            with open(self.config.history_file) as f:
                data = json.load(f)
                self.history = data.get("events", [])
        except Exception as e:
            self.logger.warning(f"Failed to load history: {e}")

    def _save_history(self) -> None:
        """Save check history to file."""
        try:
            self.config.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config.history_file, "w") as f:
                json.dump(
                    {
                        "events": self.history,
                        "threshold": self.config.threshold,
                        "updated": datetime.now().isoformat(),
                    },
                    f,
                    indent=2,
                )
        except Exception as e:
            self.logger.error(f"Failed to save history: {e}")

    def get_context_usage(self) -> Optional[ContextUsage]:
        """Get current context usage from OpenClaw.

        Returns:
            ContextUsage if successful, None if unable to parse.
        """
        try:
            result = subprocess.run(
                ["openclaw", "status"],
                capture_output=True,
                text=True,
                timeout=self.config.openclaw_timeout,
                check=False,
            )
            return parse_openclaw_status(result.stdout + result.stderr)
        except subprocess.TimeoutExpired:
            self.logger.error("openclaw status timeout")
            return None
        except Exception as e:
            self.logger.error(f"Failed to get context usage: {e}")
            return None

    def check_and_handle(self) -> bool:
        """Check context usage and compact if necessary.

        Returns:
            True if check succeeded, False if check or compaction failed.
        """
        usage = self.get_context_usage()
        if usage is None:
            return False

        # Record event
        event = {
            "timestamp": datetime.now().isoformat(),
            "used": usage.used_tokens,
            "limit": usage.limit_tokens,
            "percentage": usage.percentage,
            "action": "check",
        }
        self.history.append(event)
        self._save_history()

        self.logger.info(
            f"Context: {usage.percentage}% "
            f"({usage.used_tokens}/{usage.limit_tokens} tokens)"
        )

        # Check if compaction needed
        if usage.percentage >= self.config.threshold:
            self.logger.warning(
                f"Context at {usage.percentage}% (threshold: {self.config.threshold}%) - "
                f"Compacting..."
            )

            if self.config.dry_run:
                self.logger.info("DRY RUN: Skipping actual compaction")
            else:
                if not self._compact():
                    return False

            event["action"] = "compact"
            self.history.append(event)
            self._save_history()

        return True

    def _compact(self) -> bool:
        """Run openclaw compact command.

        Returns:
            True if compaction succeeded, False otherwise.
        """
        try:
            result = subprocess.run(
                ["openclaw", "compact"],
                capture_output=True,
                timeout=self.config.compaction_timeout,
                check=False,
            )
            if result.returncode != 0:
                self.logger.error(f"Compaction failed: {result.stderr.decode()}")
                return False

            self.logger.info("Compaction completed successfully")
            return True
        except subprocess.TimeoutExpired:
            self.logger.error("Compaction timeout")
            return False
        except Exception as e:
            self.logger.error(f"Compaction error: {e}")
            return False

    def get_status(self) -> dict:
        """Get current status.

        Returns:
            Dictionary with status information.
        """
        usage = self.get_context_usage()
        return {
            "threshold": self.config.threshold,
            "usage": {
                "percentage": usage.percentage if usage else None,
                "used": usage.used_tokens if usage else None,
                "limit": usage.limit_tokens if usage else None,
            },
            "history_events": len(self.history),
        }

    def get_history(self, limit: int = 10) -> list[dict]:
        """Get recent check history.

        Args:
            limit: Maximum number of events to return.

        Returns:
            List of recent history events.
        """
        return sorted(
            self.history,
            key=lambda e: e["timestamp"],
            reverse=True,
        )[:limit]
