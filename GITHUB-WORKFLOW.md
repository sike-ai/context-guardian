# Context Guardian - GitHub Workflow

This document defines how we use GitHub as the command center for Context Guardian development.

## Issues

### Categories

**Bugs** (label: `bug`)
- Daemon crashes
- Parsing errors
- Missing dependencies
- CI/CD failures

Example issue title: "Daemon crashes on invalid context output"

**Features** (label: `feature`)
- New CLI commands
- Additional logging
- Configuration options
- New monitoring metrics

Example issue title: "Add alert threshold configuration"

**Community Requests** (label: `community-requested`)
- Feature requests from users
- Enhancement ideas
- Workflow improvements

**Documentation** (label: `documentation`)
- README updates
- Deployment guide improvements
- API documentation
- Troubleshooting guides

### Workflow

1. **Create issue** with clear title + description
2. **Add labels** (bug, feature, documentation, community-requested)
3. **Link to milestone** (v1.0, v1.1, etc.)
4. **Assign to developer** if starting work
5. **Move to "In Progress"** on project board
6. **Create PR** linked to issue (closes #123)
7. **Merge after review**
8. **Issue auto-closes**

## Project Board

**Status Columns:**
- **Backlog** - Ideas, not prioritized
- **Ready** - Prioritized, ready to start
- **In Progress** - Active work
- **In Review** - PR waiting for approval
- **Done** - Merged and shipped

**Usage:**
- Move cards as work progresses
- Drag to reorder within column (priority)
- Everyone sees current state

## Discussions

**Categories:**

1. **Ideas** - New feature proposals, brainstorming
2. **Questions** - How to use, debugging help
3. **Announcements** - Releases, major updates
4. **Show & Tell** - Success stories, extensions

**Process:**
- Community members can start discussions
- Core team responds/discusses
- Good ideas → convert to issues
- Consensus builds naturally

## Pull Requests

**For all code changes:**
1. Create feature branch (`feature/add-webhook-support`)
2. Make changes, commit regularly
3. Open PR with clear title + description
4. Link to issues: "Fixes #123, relates to #456"
5. Require code review approval
6. CI/CD must pass (tests, lint, type-check)
7. Merge to main
8. Delete feature branch

**PR Template:**
```markdown
## Description
What does this PR do?

## Issues Fixed
Fixes #123

## Testing
How was this tested?

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Performance improvement
```

## Milestones

- **v1.0** - Initial release (current)
- **v1.1** - Stability improvements + monitoring
- **v2.0** - Multi-session tracking + cloud support

## Labels

Quick reference for organizing work:

| Label | Purpose |
|-------|---------|
| `bug` | Something broken |
| `feature` | New functionality |
| `enhancement` | Improvement to existing feature |
| `documentation` | Docs only |
| `community-requested` | User-requested feature |
| `good-first-issue` | For new contributors |
| `help-wanted` | Need community input |
| `priority-high` | Do ASAP |
| `priority-low` | Nice to have |
| `blocked` | Waiting on something else |
| `wontfix` | Decision to not implement |

## Developer Workflow (Subagents)

When spawning a developer subagent:

1. **Create GitHub issue** first (or reference existing)
2. **Assign to subagent** (add comment @subagent-name)
3. **Subagent creates feature branch** off main
4. **Subagent makes changes** + tests
5. **Subagent opens PR** linked to issue
6. **Orchestrator reviews** (code review)
7. **Merge after approval**
8. **Subagent deletes branch**

Example:
```
Issue: "Add webhook support"
PR: "feat: add webhook support (#45)"
Branch: feature/webhook-support
Status: In Review
```

## Community Contribution

### For External Contributors

1. Fork repo
2. Create feature branch
3. Make changes
4. Open PR
5. Sign CLA if needed
6. Code review + merge
7. Credit in CHANGELOG

### Encouraging Contributions

- Label beginner-friendly issues as `good-first-issue`
- Write clear contribution guidelines in CONTRIBUTING.md
- Respond quickly to PRs
- Celebrate contributions on Discussions

## Monitoring & Health

**Weekly review:**
- Check open issues count
- Review PR backlog
- Respond to discussions
- Update project board status
- Identify blockers

**Monthly review:**
- Assess milestone progress
- Plan next milestone
- Celebrate wins
- Adjust priorities

## Integration with Moltbook

Link GitHub discussions + issues on moltbook:
- "Check out the discussion about..."
- "Vote on this feature proposal..."
- "Report a bug here..."

Create feedback loop: moltbook → GitHub discussions → issues → PRs

---

**TL;DR:**
- All work visible on GitHub
- Issues for planning
- PRs for code review
- Discussions for community
- Project board for status
- Everyone knows what's happening, why, and when
