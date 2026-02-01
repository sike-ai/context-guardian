"""Command-line interface for Context Guardian."""

import argparse
import sys
from typing import Optional

from context_guardian.config import Config
from context_guardian.daemon import ContextGuardian
from context_guardian.logger import setup_logger


def cli(args: Optional[list[str]] = None) -> int:
    """Command-line interface entry point.

    Args:
        args: Command-line arguments. If None, uses sys.argv[1:].

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    parser = argparse.ArgumentParser(
        description="Context Guardian - Proactive context management for OpenClaw agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status              Show current context usage
  %(prog)s check               Check and compact if needed
  %(prog)s history             Show recent check history
  %(prog)s set-threshold 80    Set compaction threshold to 80%
  %(prog)s --help              Show this help message
        """,
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # status command
    subparsers.add_parser("status", help="Show current context usage")

    # check command
    subparsers.add_parser("check", help="Check and compact if needed")

    # history command
    history_parser = subparsers.add_parser("history", help="Show recent check history")
    history_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of events to show (default: 10)",
    )

    # set-threshold command
    threshold_parser = subparsers.add_parser("set-threshold", help="Set compaction threshold")
    threshold_parser.add_argument(
        "percentage",
        type=int,
        help="Threshold percentage (50-95%)",
    )

    # Parse arguments
    parsed = parser.parse_args(args)
    setup_logger(__name__, parsed.log_level)

    # Create config
    config = Config(log_level=parsed.log_level)

    # Create guardian
    guardian = ContextGuardian(config)

    # Handle commands
    if parsed.command == "status":
        return cmd_status(guardian)
    elif parsed.command == "check":
        return cmd_check(guardian)
    elif parsed.command == "history":
        return cmd_history(guardian, parsed.limit)
    elif parsed.command == "set-threshold":
        return cmd_set_threshold(guardian, parsed.percentage)
    else:
        parser.print_help()
        return 1


def cmd_status(guardian: ContextGuardian) -> int:
    """Status command implementation."""
    status = guardian.get_status()

    print("\n" + "=" * 50)
    print("Context Guardian Status")
    print("=" * 50)
    print(f"Threshold: {status['threshold']}%")

    if status["usage"]["percentage"] is not None:
        usage = status["usage"]
        print(f"Usage: {usage['percentage']}% ({usage['used']}/{usage['limit']} tokens)")
    else:
        print("Usage: Unable to parse context")

    print(f"History events: {status['history_events']}")
    print("=" * 50 + "\n")
    return 0


def cmd_check(guardian: ContextGuardian) -> int:
    """Check command implementation."""
    success = guardian.check_and_handle()
    return 0 if success else 1


def cmd_history(guardian: ContextGuardian, limit: int) -> int:
    """History command implementation."""
    events = guardian.get_history(limit)

    print("\n" + "=" * 50)
    print(f"Recent Events (Last {limit})")
    print("=" * 50)

    for i, event in enumerate(events, 1):
        ts = event["timestamp"].split("T")[1].split("+")[0]  # Extract time part
        action = event.get("action", "?")
        percent = event.get("percentage", "?")
        print(f"{i}. [{ts}] {action}: {percent}%")

    print("=" * 50 + "\n")
    return 0


def cmd_set_threshold(guardian: ContextGuardian, percentage: int) -> int:
    """Set threshold command implementation."""
    try:
        Config.validate_threshold(percentage)
        guardian.config.threshold = percentage
        guardian._save_history()  # Save updated config
        print(f"✓ Threshold set to {percentage}%")
        return 0
    except ValueError as e:
        print(f"✗ Error: {e}")
        return 1


def main() -> int:
    """Main entry point."""
    try:
        return cli()
    except KeyboardInterrupt:
        print("\nInterrupted")
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
