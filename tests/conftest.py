"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path
from typing import Any, Dict, Generator

import pytest

from context_guardian.config import Config


@pytest.fixture
def temp_files() -> Generator[Dict[str, Any], None, None]:
    """Create temporary files for testing."""
    with tempfile.TemporaryDirectory(prefix="context-guardian-test-") as tmpdir:
        tmppath = Path(tmpdir)
        yield {
            "history": tmppath / "history.json",
            "state": tmppath / "state.json",
        }


@pytest.fixture
def config(temp_files: Dict[str, Any]) -> Config:
    """Create test configuration."""
    return Config(
        threshold=75,
        history_file=temp_files["history"],
        state_file=temp_files["state"],
        log_level="WARNING",
        dry_run=False,
    )


@pytest.fixture
def openclaw_status_output() -> str:
    """Mock openclaw status output."""
    return """OpenClaw status

Sessions
│ Key                                    │ Tokens         │
├────────────────────────────────────────┼────────────────┤
│ agent:main:main                        │ 84k/200k (42%) │
"""


@pytest.fixture
def openclaw_status_high() -> str:
    """Mock openclaw status with high usage."""
    return """OpenClaw status
│ agent:main:main                        │ 160k/200k (80%) │
"""


@pytest.fixture
def openclaw_status_critical() -> str:
    """Mock openclaw status with critical usage."""
    return """OpenClaw status
│ agent:main:main                        │ 190k/200k (95%) │
"""
