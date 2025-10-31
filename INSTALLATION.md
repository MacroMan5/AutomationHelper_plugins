# Installation Guide

Complete instructions for installing and configuring the Workflow Automation Suite plugin for Claude Code.

## Prerequisites

Before installing this plugin, ensure you have:

1. **Claude Code** installed and configured
   - Terminal: Claude Code CLI
   - VS Code: Claude Code extension
   - Minimum version: 2.0.13 or later (plugin support)

2. **Git** (for GitHub installation method)
   - Required to clone repositories
   - Verify: `git --version`

3. **Active Claude Code Session**
   - Must be in a project directory
   - Claude Code must be running

## Installation Methods

### Method 1: GitHub Marketplace (Recommended)

This is the easiest and recommended method for most users.

#### Step 1: Add the Marketplace

In Claude Code (terminal or VS Code), run:

```bash
/plugin marketplace add therouxe/workflow-automation-suite
```

**Expected output:**
```
✓ Marketplace 'workflow-automation-marketplace' added successfully
✓ Found 1 plugin available
```

#### Step 2: Browse Available Plugins

```bash
/plugin
```

You'll see the plugin in the list:
- **workflow-automation-suite** - Complete workflow automation toolkit

#### Step 3: Install the Plugin

```bash
/plugin install workflow-automation-suite
```

**Expected output:**
```
✓ Installing plugin 'workflow-automation-suite'...
✓ Loaded 6 skills
✓ Registered 4 agents
✓ Plugin installed successfully
```

#### Step 4: Verify Installation

```bash
/plugin list
```

You should see:
```
Installed plugins:
  - workflow-automation-suite (v1.0.0)
```

### Method 2: Direct GitHub URL

If you prefer to specify the full URL:

```bash
/plugin marketplace add https://github.com/therouxe/workflow-automation-suite.git
/plugin install workflow-automation-suite
```

### Method 3: Local Development Installation

For testing or development:

#### Step 1: Clone the Repository

```bash
git clone https://github.com/therouxe/workflow-automation-suite.git
cd workflow-automation-suite
```

#### Step 2: Create Local Marketplace

Create a development marketplace directory:

```bash
mkdir -p ~/dev-marketplace
cd ~/dev-marketplace
```

Create `~/dev-marketplace/.claude-plugin/marketplace.json`:

```json
{
  "name": "dev-marketplace",
  "owner": {
    "name": "Development",
    "email": "[email protected]"
  },
  "plugins": [
    {
      "name": "workflow-automation-suite",
      "source": "/full/path/to/workflow-automation-suite",
      "description": "Local development version"
    }
  ]
}
```

#### Step 3: Install from Local Marketplace

```bash
/plugin marketplace add ~/dev-marketplace
/plugin install workflow-automation-suite@dev-marketplace
```

## Team Installation

### For Team Administrators

To deploy this plugin across your entire team:

#### Step 1: Add to Repository Settings

In your team's project repository, create or edit `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "workflow-automation": {
      "source": {
        "source": "github",
        "repo": "therouxe/workflow-automation-suite"
      }
    }
  }
}
```

#### Step 2: Commit and Push

```bash
git add .claude/settings.json
git commit -m "Add Workflow Automation Suite plugin to team configuration"
git push
```

#### Step 3: Team Members Setup

When team members pull the repository and trust the folder:

1. **Pull latest changes**: `git pull`
2. **Trust the repository** in Claude Code
3. **Plugin auto-installs** - Claude Code automatically installs configured marketplaces

### For Team Members

If your team administrator has configured the plugin:

1. **Clone/pull** the team repository
2. **Open in Claude Code**
3. **Trust the repository** when prompted
4. **Verify installation**: `/plugin list`

The plugin will be automatically installed and ready to use.

## Verification & Testing

### 1. Check Plugin Status

```bash
/plugin list
```

Expected output:
```
Installed plugins:
  - workflow-automation-suite (v1.0.0)
    Skills: 6
    Agents: 4
    Status: Active
```

### 2. List Available Skills

The skills don't appear in a command list but activate automatically based on your language. To verify they're available, check the plugin details:

```bash
/plugin info workflow-automation-suite
```

### 3. Test a Skill

Try triggering a skill:

```
"I want to design a workflow to automate email notifications from SharePoint"
```

Expected: The **automation-brainstorm** skill should activate and start asking clarifying questions.

### 4. Check Agents

Agents are automatically available to Claude Code. They're invoked by skills as needed, so no manual verification is required.

### 5. Verify Documentation Access

The plugin includes extensive documentation in the `Docs/` directory. Claude Code can access this automatically when skills are active.

## Configuration

### Plugin Settings

The plugin works out-of-the-box with default settings. No additional configuration is required.

### Custom Skill Configuration

If you want to customize skill behavior, you can edit the skill files:

```
.claude/skills/
├── automation-brainstorm/SKILL.md
├── automation-build-flow/SKILL.md
├── automation-debugger/SKILL.md
├── automation-quick-fix/SKILL.md
├── automation-refactor/SKILL.md
└── automation-validator/SKILL.md
```

**Note**: Editing these files requires local development installation (Method 3).

### Documentation Updates

Documentation is in the `Docs/` directory:

```
Docs/
├── PowerAutomateDocs/
│   ├── Forms/
│   ├── Excel/
│   ├── Outlook/
│   ├── Teams/
│   ├── SharePoint/
│   ├── OneDrive/
│   └── BuiltIn/
└── N8NDocs/
    ├── Core/
    ├── AI/
    ├── Apps/
    └── Database/
```

Skills automatically reference this documentation to provide accurate, hallucination-free recommendations.

## Updating the Plugin

### Manual Update

To update to the latest version:

```bash
/plugin uninstall workflow-automation-suite
/plugin install workflow-automation-suite
```

### Auto-Update (Team Configuration)

If installed via team configuration (`.claude/settings.json`), updates happen automatically when:
1. The GitHub repository is updated
2. Team members pull latest changes
3. Claude Code refreshes the marketplace

## Troubleshooting

### Plugin Not Found

**Problem**: `/plugin install workflow-automation-suite` fails with "Plugin not found"

**Solution**:
1. Verify marketplace is added: `/plugin marketplace list`
2. If not listed, add it: `/plugin marketplace add therouxe/workflow-automation-suite`
3. Refresh marketplace: `/plugin marketplace refresh`
4. Try installation again

### Skills Not Activating

**Problem**: Skills don't seem to be working when you mention keywords

**Solution**:
1. Verify plugin is active: `/plugin list`
2. If not active, enable it: `/plugin enable workflow-automation-suite`
3. Try using explicit trigger phrases like "I want to optimize this workflow"
4. Check Claude Code debug mode: `claude --debug`

### Agent Errors

**Problem**: "Agent not found" or agent errors

**Solution**:
1. Verify agents are loaded: `/plugin info workflow-automation-suite`
2. Check for file path errors in plugin.json
3. Ensure `.claude/agents/` directory exists with .md files
4. Reinstall plugin: `/plugin uninstall workflow-automation-suite && /plugin install workflow-automation-suite`

### Documentation Not Found

**Problem**: Skills report they can't find documentation

**Solution**:
1. Ensure `Docs/` directory exists at plugin root
2. Verify directory structure matches expectations
3. Check file permissions (must be readable)
4. Try local development installation for debugging

### Permission Issues

**Problem**: "Permission denied" or access errors

**Solution**:
1. Check Git repository access (if using GitHub installation)
2. Verify Claude Code has read access to plugin directory
3. For team installations, ensure repository is trusted
4. Check file permissions: `ls -la .claude-plugin/`

### Version Conflicts

**Problem**: Multiple versions or conflicting plugins

**Solution**:
1. Uninstall all versions: `/plugin uninstall workflow-automation-suite`
2. Clear marketplace cache: `/plugin marketplace refresh`
3. Reinstall specific version: `/plugin install workflow-automation-suite@1.0.0`

## Uninstallation

### Complete Removal

To completely remove the plugin:

```bash
# Uninstall plugin
/plugin uninstall workflow-automation-suite

# Remove marketplace
/plugin marketplace remove workflow-automation-marketplace

# Verify removal
/plugin list
/plugin marketplace list
```

### Team Configuration Removal

If installed via team configuration, remove from `.claude/settings.json`:

```bash
# Edit .claude/settings.json and remove the extraKnownMarketplaces entry
# Then commit and push
git add .claude/settings.json
git commit -m "Remove Workflow Automation Suite plugin"
git push
```

Team members will need to:
1. Pull the changes
2. Manually uninstall: `/plugin uninstall workflow-automation-suite`

## Support

### Getting Help

If you encounter issues:

1. **Check logs**: Run Claude Code with `--debug` flag
2. **Review documentation**: [CLAUDE.md](./CLAUDE.md)
3. **Search issues**: [GitHub Issues](https://github.com/therouxe/workflow-automation-suite/issues)
4. **Ask community**: [GitHub Discussions](https://github.com/therouxe/workflow-automation-suite/discussions)
5. **Contact support**: [email protected]

### Reporting Bugs

When reporting issues, include:

- Claude Code version: `claude --version`
- Plugin version: `/plugin info workflow-automation-suite`
- Operating system
- Installation method used
- Error messages or logs
- Steps to reproduce

## Next Steps

After successful installation:

1. **Read the usage guide**: [CLAUDE.md](./CLAUDE.md)
2. **Try the examples**: See each skill's EXAMPLE.md file
3. **Explore documentation**: Browse `Docs/` directory
4. **Join discussions**: Share your workflows and get help

---

**Need help?** Open an issue or discussion on GitHub!
