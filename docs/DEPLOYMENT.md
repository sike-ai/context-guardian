# Deployment Guide - Context Guardian

This guide covers installing and deploying Context Guardian as a background daemon.

## Prerequisites

- Python 3.8 or higher
- OpenClaw installed and configured
- Linux with systemd (for background daemon)
- Basic command-line familiarity

## Installation Steps

### 1. Install Context Guardian

```bash
cd /path/to/context-guardian
pip install -e .
```

Verify installation:
```bash
context-guardian --help
```

### 2. Create Systemd Service Files

Create `~/.config/systemd/user/context-guardian.service`:

```ini
[Unit]
Description=Context Guardian - Proactive Context Management
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/context-guardian check
StandardOutput=journal
StandardError=journal
SyslogIdentifier=context-guardian
Environment="PATH=/usr/local/bin:/usr/bin:/bin"

[Install]
WantedBy=multi-user.target
```

Create `~/.config/systemd/user/context-guardian.timer`:

```ini
[Unit]
Description=Context Guardian - Check every 5 minutes
Requires=context-guardian.service

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min
Persistent=true
AccuracySec=10s

[Install]
WantedBy=timers.target
```

Or copy from the repository:
```bash
mkdir -p ~/.config/systemd/user
cp configs/systemd/* ~/.config/systemd/user/
```

### 3. Enable and Start

```bash
# Reload systemd
systemctl --user daemon-reload

# Enable timer to start on boot
systemctl --user enable context-guardian.timer

# Start the timer
systemctl --user start context-guardian.timer
```

### 4. Verify Installation

```bash
# Check timer status
systemctl --user status context-guardian.timer

# View next scheduled run
systemctl --user list-timers context-guardian.timer

# Manual check (should work immediately)
context-guardian check
```

## Configuration

### Threshold

Adjust the compaction threshold (default: 75%):

```bash
context-guardian set-threshold 80
```

Range: 50-95% (recommended: 70-80%)

### Environment Variables

Set environment variables to customize behavior:

```bash
export CONTEXT_GUARDIAN_THRESHOLD=75          # Compaction threshold
export CONTEXT_GUARDIAN_CHECK_INTERVAL=300    # Check interval (seconds)
export CONTEXT_GUARDIAN_LOG_LEVEL=INFO        # DEBUG, INFO, WARNING, ERROR
export CONTEXT_GUARDIAN_DRY_RUN=false         # Don't actually compact (for testing)
```

### Config File (Optional)

Create `~/.config/context-guardian/config.yaml` (optional):

```yaml
threshold: 75
check_interval: 300
log_level: INFO
```

## Troubleshooting

### Service Not Starting

```bash
# Check for errors
systemctl --user status context-guardian.service

# View detailed logs
journalctl --user -u context-guardian --all

# Try running manually
/usr/local/bin/context-guardian check
```

### Timer Not Triggering

```bash
# Verify timer is enabled
systemctl --user is-enabled context-guardian.timer

# Check next trigger time
systemctl --user list-timers context-guardian.timer

# Force immediate run (for testing)
systemctl --user start context-guardian.service
```

### OpenClaw Command Not Found

```bash
# Verify openclaw is in PATH
which openclaw
echo $PATH

# If needed, update PATH in systemd service:
# Environment="PATH=/usr/local/bin:/usr/bin:/bin"
```

## Monitoring

### Real-time Logs

```bash
journalctl --user -u context-guardian -f
```

### Check Last 10 Events

```bash
journalctl --user -u context-guardian -n 10
```

### View All Logs (Current Session)

```bash
journalctl --user -u context-guardian --all
```

## Uninstall

If you need to remove Context Guardian:

```bash
# Stop the timer
systemctl --user stop context-guardian.timer

# Disable auto-start
systemctl --user disable context-guardian.timer

# Remove service files
rm ~/.config/systemd/user/context-guardian.*
systemctl --user daemon-reload

# Uninstall package
pip uninstall context-guardian
```

## Performance Tuning

### Increase Check Frequency

Edit `~/.config/systemd/user/context-guardian.timer`:

```ini
[Timer]
OnBootSec=30s
OnUnitActiveSec=1min     # Check every 1 minute instead of 5
AccuracySec=5s
```

Then reload:
```bash
systemctl --user daemon-reload
systemctl --user restart context-guardian.timer
```

### Decrease Compaction Threshold

For more aggressive compaction (compact at 60% instead of 75%):

```bash
context-guardian set-threshold 60
```

### Adjust Logging Level

For debug output:

```bash
export CONTEXT_GUARDIAN_LOG_LEVEL=DEBUG
systemctl --user restart context-guardian.service
```

## Health Checks

Verify the daemon is healthy:

```bash
# 1. Check timer is active
systemctl --user is-active context-guardian.timer

# 2. Check last run time
systemctl --user status context-guardian.service

# 3. Verify no recent errors in logs
journalctl --user -u context-guardian --since "10 minutes ago" | grep ERROR

# 4. Manual run should succeed
context-guardian check && echo "✓ OK" || echo "✗ FAILED"
```

## Stability Verification (24-48 Hour Test)

Run for 1-2 days to verify stability:

### Success Criteria

- ✓ Timer runs every 5 minutes without missing checks
- ✓ All checks complete successfully (no parsing errors)
- ✓ No crashed processes or hung operations
- ✓ Compaction triggers correctly when threshold reached
- ✓ Logs show clean operation (no ERROR messages)
- ✓ Memory usage remains stable (no leaks)

### Verification Commands

```bash
# Check run count (should increase every 5 minutes)
journalctl --user -u context-guardian | grep "Context:" | wc -l

# Check for errors
journalctl --user -u context-guardian | grep ERROR | wc -l

# Check last 5 runs
context-guardian history 5

# View context usage trend
journalctl --user -u context-guardian | grep "Context:" | tail -10
```

### After Stability Verified

Once confirmed stable for 24-48 hours:
- Update documentation
- Consider publishing to PyPI
- Share success metrics on moltbook
- Monitor in production long-term

## Next Steps

- Read [MONITORING.md](MONITORING.md) for ongoing monitoring
- See [README.md](../README.md) for usage examples
- Check [DEVELOPMENT.md](DEVELOPMENT.md) to contribute improvements
