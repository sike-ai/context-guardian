"""Context Guardian - Proactive context management for OpenClaw agents.

This module provides tools to monitor OpenClaw session context usage and
automatically compact context before rate limits are hit.
"""

__version__ = "1.0.0"
__author__ = "Sike-AI"
__all__ = ["ContextGuardian", "ContextLevel", "ContextUsage"]

from context_guardian.daemon import ContextGuardian
from context_guardian.parser import ContextLevel, ContextUsage
