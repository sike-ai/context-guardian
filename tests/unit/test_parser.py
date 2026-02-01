"""Tests for context usage parser."""

import pytest

from context_guardian.parser import ContextLevel, ContextUsage, parse_openclaw_status, parse_token_count


class TestTokenParsing:
    """Tests for parse_token_count function."""

    def test_parse_k_unit(self) -> None:
        """Test parsing with 'k' unit."""
        assert parse_token_count("84", "k") == 84000
        assert parse_token_count("84.5", "k") == 84500

    def test_parse_m_unit(self) -> None:
        """Test parsing with 'm' unit."""
        assert parse_token_count("1", "m") == 1_000_000
        assert parse_token_count("1.5", "m") == 1_500_000

    def test_parse_no_unit(self) -> None:
        """Test parsing with no unit."""
        assert parse_token_count("1000", "") == 1000

    def test_parse_case_insensitive(self) -> None:
        """Test case insensitivity."""
        assert parse_token_count("84", "K") == 84000
        assert parse_token_count("1", "M") == 1_000_000


class TestContextUsage:
    """Tests for ContextUsage dataclass."""

    def test_context_usage_creation(self) -> None:
        """Test creating ContextUsage."""
        usage = ContextUsage(used_tokens=84000, limit_tokens=200000, percentage=42)
        assert usage.used_tokens == 84000
        assert usage.limit_tokens == 200000
        assert usage.percentage == 42

    def test_context_level_healthy(self) -> None:
        """Test healthy context level (< 60%)."""
        usage = ContextUsage(used_tokens=100000, limit_tokens=200000, percentage=50)
        assert usage.level == ContextLevel.HEALTHY

    def test_context_level_elevated(self) -> None:
        """Test elevated context level (60-79%)."""
        usage = ContextUsage(used_tokens=140000, limit_tokens=200000, percentage=70)
        assert usage.level == ContextLevel.ELEVATED

    def test_context_level_warning(self) -> None:
        """Test warning context level (80-89%)."""
        usage = ContextUsage(used_tokens=160000, limit_tokens=200000, percentage=80)
        assert usage.level == ContextLevel.WARNING

    def test_context_level_critical(self) -> None:
        """Test critical context level (>= 90%)."""
        usage = ContextUsage(used_tokens=190000, limit_tokens=200000, percentage=95)
        assert usage.level == ContextLevel.CRITICAL


class TestParsing:
    """Tests for parse_openclaw_status function."""

    def test_parse_normal_usage(self, openclaw_status_output: str) -> None:
        """Test parsing normal context usage."""
        result = parse_openclaw_status(openclaw_status_output)
        assert result is not None
        assert result.used_tokens == 84000
        assert result.limit_tokens == 200000
        assert result.percentage == 42

    def test_parse_high_usage(self, openclaw_status_high: str) -> None:
        """Test parsing high context usage."""
        result = parse_openclaw_status(openclaw_status_high)
        assert result is not None
        assert result.percentage == 80

    def test_parse_critical_usage(self, openclaw_status_critical: str) -> None:
        """Test parsing critical context usage."""
        result = parse_openclaw_status(openclaw_status_critical)
        assert result is not None
        assert result.percentage == 95

    def test_parse_empty_output(self) -> None:
        """Test parsing empty output."""
        result = parse_openclaw_status("")
        assert result is None

    def test_parse_invalid_output(self) -> None:
        """Test parsing invalid output."""
        result = parse_openclaw_status("Some random output without tokens")
        assert result is None

    @pytest.mark.parametrize(
        "output,expected_used,expected_limit",
        [
            ("100k/200k (50%)", 100000, 200000),
            ("1.5m/2m (75%)", 1500000, 2000000),
            ("0.5k/100k (0%)", 500, 100000),
        ],
    )
    def test_parse_various_formats(
        self, output: str, expected_used: int, expected_limit: int
    ) -> None:
        """Test parsing various token formats."""
        result = parse_openclaw_status(output)
        assert result is not None
        assert result.used_tokens == expected_used
        assert result.limit_tokens == expected_limit
