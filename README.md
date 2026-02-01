# Context Guardian

[![Tests](https://img.shields.io/github/actions/workflow/status/sike-ai/context-guardian/test.yml?label=tests)](https://github.com/sike-ai/context-guardian/actions)
[![Coverage](https://img.shields.io/badge/coverage-90%25-green)](https://github.com/sike-ai/context-guardian)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Proactive context management for OpenClaw agents.** Never hit rate limits unexpectedly again.

## The Problem

When running OpenClaw agents, you accumulate tokens with each operation. Hit the context limit and **everything breaks**—agents fail silently, tasks stop mid-execution, you have to manually compact and start over.

You need something watching for you.

## The Solution

Context Guardian runs in the background, monitoring your context usage **every 5 minutes**. When you're approaching the limit, it automatically compacts—before you hit the wall.

**Result:** Uninterrupted agent execution. No surprises. No manual interventions.

## Features

- 🎯 **Proactive monitoring** - Checks every 5 minutes by default
- 🚨 **Auto-compaction** - Compacts at 75% threshold (prevents hitting the limit)
- 📊 **History tracking** - Logs all checks and compactions
- ⚙️ **Configurable** - Adjust threshold, interval, logging level
- 🧪 **Well tested** - 90%+ code coverage with comprehensive test suite
- 📦 **Zero dependencies** - Pure Python 3.8+, uses only stdlib
- 🏢 **Production ready** - Type hints, CI/CD workflows, professional structure

## Quick Start

### Installation

```bash
# Clone the repo
git clone https://github.com/sike-ai/context-guardian.git
cd context-guardian

# Install in development mode
pip install -e .

# Or with dev dependencies for local development
pip install -e ".[dev]"
```

### Setup (Systemd Background Daemon)

```bash
# Copy systemd service and timer files
mkdir -p ~/.config/systemd/user
cp configs/systemd/* ~/.config/systemd/user/

# Enable and start
systemctl --user daemon-reload
systemctl --user enable context-guardian.timer
systemctl --user start context-guardian.timer

# Verify it's running
systemctl --user list-timers context-guardian.timer
```

### Usage

```bash
# Check current status
context-guardian status

# Manually check and compact if needed
context-guardian check

# View recent checks
context-guardian history

# Set compaction threshold (50-95%)
context-guardian set-threshold 80

# Watch logs in real-time
journalctl --user -u context-guardian -f
```

## How It Works

```
Every 5 minutes (systemd timer):
  ↓
  openclaw status → Extract tokens (e.g., 160k/200k)
  ↓
  Percentage = 160/200 = 80%
  ↓
  If >= 75% threshold:
    → Run openclaw compact
    → Log event
  ↓
  Save to history
```

**Key insight:** Daemon checks BEFORE you hit the limit, so compaction is preventative, not reactive.

## Configuration

Edit `~/.config/systemd/user/context-guardian.service` or use environment variables:

```bash
export CONTEXT_GUARDIAN_THRESHOLD=80      # Compaction threshold (%)
export CONTEXT_GUARDIAN_CHECK_INTERVAL=300  # Check interval (seconds)
export CONTEXT_GUARDIAN_LOG_LEVEL=INFO     # DEBUG, INFO, WARNING, ERROR
```

## Monitoring & Verification

### Real-time Logs
```bash
journalctl --user -u context-guardian -f
```

### Check Last Run
```bash
systemctl --user status context-guardian.service
```

### View History
```bash
context-guardian history 20
```

### Manual Dry-Run
```bash
CONTEXT_GUARDIAN_DRY_RUN=true context-guardian check
```

## Architecture

```
context_guardian/
├── main.py           # CLI entry point
├── daemon.py         # Core guardian logic
├── parser.py         # OpenClaw status parsing
├── config.py         # Configuration management
└── logger.py         # Logging setup
```

All components are **fully typed** and **heavily tested**.

## Development

### Run Tests
```bash
make test          # Run pytest
make coverage      # Generate coverage report
make lint          # Run ruff linter
make type-check    # Type checking with mypy
make all           # Run all checks
```

### Local Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

## Troubleshooting

### Daemon Not Running
```bash
# Check service status
systemctl --user status context-guardian.service

# Check timer status
systemctl --user list-timers context-guardian.timer

# View error logs
journalctl --user -u context-guardian --all
```

### Context Not Being Detected
- Ensure `openclaw` is in your PATH
- Run `openclaw status` manually to verify it works
- Check logs for parsing errors

### Compaction Not Triggering
- Verify threshold with `context-guardian status`
- Check recent history: `context-guardian history`
- Enable debug logging: `export CONTEXT_GUARDIAN_LOG_LEVEL=DEBUG`

## Performance

- **Memory:** < 10MB (minimal history storage)
- **CPU:** < 1% per check (syscalls only)
- **Frequency:** Every 5 minutes (configurable)
- **Reliability:** Systemd restarts on failure

## API Usage

```python
from context_guardian import ContextGuardian
from context_guardian.config import Config

# Create config
config = Config(threshold=80, log_level="INFO")

# Create guardian
guardian = ContextGuardian(config)

# Check and compact if needed
if guardian.check_and_handle():
    print("Check successful")
else:
    print("Check failed")

# Get current status
status = guardian.get_status()
print(f"Context: {status['usage']['percentage']}%")

# Get history
events = guardian.get_history(limit=5)
for event in events:
    print(event)
```

## Testing

Comprehensive test suite with:
- 90%+ code coverage
- Unit tests for parsing, config, daemon logic
- Integration tests for CLI
- Mocked subprocess calls (no side effects)
- Parametrized tests for various input formats

Run tests:
```bash
pytest -v              # Verbose output
pytest --cov           # Show coverage
pytest -k "parser"     # Run specific tests
```

## Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass (`make all`)
5. Submit a PR

## License

MIT License - see [LICENSE](LICENSE) file

## Inspiration

Built for developers who:
- Run OpenClaw agents continuously
- Want reliability without manual monitoring
- Appreciate simple, focused tools
- Value clean code and proper testing

## Support

- **Issues:** [GitHub Issues](https://github.com/sike-ai/context-guardian/issues)
- **Discussions:** [GitHub Discussions](https://github.com/sike-ai/context-guardian/discussions)
- **Documentation:** See [docs/](docs/) folder

---

**Make your agents unstoppable. Let Context Guardian handle the limits.**
