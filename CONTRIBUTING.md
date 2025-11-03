# Contributing to Automation Helper

Thank you for considering contributing to the Automation Helper! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Contributing Documentation](#contributing-documentation)
- [Contributing Skills](#contributing-skills)
- [Contributing Agents](#contributing-agents)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Harassment, trolling, or insulting comments
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## How Can I Contribute?

### 1. Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When filing a bug report, include:**
- Clear, descriptive title
- Steps to reproduce the behavior
- Expected behavior
- Actual behavior
- Claude Code version (`claude --version`)
- Plugin version (`/plugin info automation-helper`)
- Operating system
- Error messages or logs

**Template:**
```markdown
**Description**
A clear description of the bug.

**Steps to Reproduce**
1. Install plugin
2. Run command '...'
3. Observe error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- Claude Code: 2.0.13
- Plugin: 0.1.0-alpha
- OS: macOS 14.2

**Error Messages**
```
Paste error messages here
```
```

### 2. Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**When suggesting an enhancement, include:**
- Clear, descriptive title
- Detailed description of the suggested enhancement
- Use cases and benefits
- Examples of how it would work
- Any potential drawbacks

### 3. Contributing Code

See the [Development Setup](#development-setup) section below.

### 4. Contributing Documentation

Documentation improvements are always welcome! This includes:
- Adding new platform documentation (Docs/)
- Improving existing documentation
- Adding examples
- Fixing typos or clarifying explanations
- Translating documentation

See [Contributing Documentation](#contributing-documentation) below.

## Development Setup

### Prerequisites

- Claude Code 2.0.13 or later
- Git
- Text editor (VS Code recommended)
- Basic knowledge of Markdown and JSON

### Setting Up Development Environment

#### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/AutomationHelper_plugins.git
cd AutomationHelper_plugins
```

#### 2. Create Development Marketplace

```bash
# Create a development marketplace directory
mkdir -p ~/dev-marketplace/.claude-plugin

# Create marketplace.json
cat > ~/dev-marketplace/.claude-plugin/marketplace.json << 'EOF'
{
  "name": "dev-marketplace",
  "owner": {
    "name": "Development",
    "email": "[email protected]"
  },
  "plugins": [
    {
      "name": "automation-helper",
      "source": "/FULL/PATH/TO/AutomationHelper_plugins",
      "description": "Local development version"
    }
  ]
}
EOF
```

#### 3. Install Development Plugin

```bash
# In Claude Code
/plugin marketplace add ~/dev-marketplace
/plugin install automation-helper@dev-marketplace
```

#### 4. Test Your Changes

After making changes:

```bash
# Uninstall and reinstall to test
/plugin uninstall automation-helper
/plugin install automation-helper@dev-marketplace
```

### Creating a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or changes

## Contributing Documentation

### Documentation Structure

```
Docs/
├── PowerAutomateDocs/
│   ├── ConnectorName/
│   │   ├── overview.md          # Connector overview
│   │   ├── triggers.md          # Trigger documentation
│   │   └── actions.md           # Action documentation
│   └── templates/
│       ├── connector-overview-template.md
│       ├── triggers-template.md
│       └── actions-template.md
└── N8NDocs/
    ├── Category/
    │   └── node-name.md
    └── Templates/
        └── node-template.md
```

### Documentation Format (v2)

All documentation must follow the agent-optimized format v2:

#### Required YAML Frontmatter

```yaml
---
type: connector-overview  # or connector-triggers, connector-actions, node-overview
connector_name: Excel Online
platform: power-automate  # or n8n, make, zapier
version: 1.0.0
keywords: [spreadsheet, table, rows, excel]
api_limits:
  calls_per_minute: 1.67
  calls_per_hour: 100
last_updated: 2025-10-31
---
```

#### Required XML Structure

**Limitations:**
```xml
<limitation id="lim-001" severity="critical">
<description>Maximum 25MB file size</description>
<workaround>Use chunked upload for larger files</workaround>
</limitation>
```

**Actions/Triggers:**
```xml
<action id="action-create-row" category="create" complexity="low">
<name>Add a row into a table</name>
<description>Adds a new row to the specified table</description>
</action>
```

**Errors:**
```xml
<error id="err-429" http_code="429">
<message>TooManyRequests</message>
<cause>Exceeded API rate limit</cause>
<solution>Implement delays or batching</solution>
</error>
```

### Adding New Connector Documentation

1. **Copy template:**
```bash
cp Docs/PowerAutomateDocs/templates/connector-overview-template.md \
   Docs/PowerAutomateDocs/NewConnector/overview.md
```

2. **Fill in all sections:**
   - YAML frontmatter
   - Connector overview
   - API limits
   - Critical limitations
   - Common errors
   - Best practices

3. **Follow XML tagging:**
   - Use unique IDs
   - Include all attributes
   - Maintain consistent formatting

4. **Test with agent:**
   - Verify agents can find information
   - Test search patterns
   - Ensure XML is valid

5. **Update status:**
   - Add entry to `Docs/PowerAutomateDocs/DOCUMENTATION_STATUS.md`

### Documentation Quality Checklist

- [ ] YAML frontmatter complete
- [ ] All limitations documented with IDs
- [ ] All actions/triggers documented with IDs
- [ ] Common errors documented with solutions
- [ ] Best practices section included
- [ ] XML tags properly closed
- [ ] Unique IDs assigned
- [ ] Keywords relevant and complete
- [ ] Examples provided where appropriate
- [ ] References to related connectors

## Contributing Skills

### Skill Structure

```
.claude/skills/
└── skill-name/
    ├── SKILL.md              # Main skill implementation (required)
    ├── EXAMPLE.md            # Usage examples (recommended)
    └── supporting-files.md   # Additional reference files (optional)
```

### SKILL.md Format

#### Required Frontmatter

```markdown
---
name: skill-name
description: Brief description of what the skill does, when it activates, and what it outputs. Should mention supported platforms and key features.
---
```

#### Required Sections

1. **Purpose** - What the skill does
2. **When This Skill Activates** - Trigger conditions
3. **Core Workflow** - Step-by-step process
4. **Output Format** - What the skill returns
5. **Examples** - Usage examples
6. **Best Practices** - Guidelines for use

### Creating a New Skill

1. **Copy template:**
```bash
mkdir .claude/skills/new-skill
cp .claude/skills/automation-debugger/SKILL.md \
   .claude/skills/new-skill/SKILL.md
```

2. **Define skill metadata:**
   - Clear name (kebab-case)
   - Comprehensive description
   - Specific trigger conditions

3. **Document workflow:**
   - Phase-by-phase breakdown
   - Sub-agent coordination
   - Documentation references

4. **Add examples:**
   - Create EXAMPLE.md
   - Show complete scenarios
   - Include before/after comparisons

5. **Update skill index:**
   - Add to `.claude/skills/README.md`
   - Update CLAUDE.md with new skill

### Skill Quality Checklist

- [ ] Clear, descriptive name
- [ ] Comprehensive description in frontmatter
- [ ] Well-defined activation triggers
- [ ] Documented workflow phases
- [ ] Sub-agent usage explained
- [ ] Output format specified
- [ ] Multiple examples provided
- [ ] Best practices documented
- [ ] Documentation references included
- [ ] No hardcoded filenames

## Contributing Agents

### Agent Structure

Agents are specialized sub-agents invoked by skills.

```
.claude/agents/
└── agent-name.md
```

### Agent Format

```markdown
---
name: agent-name
type: research | flow-builder | validator | documenter
description: What the agent does
---

# Agent Name

## Purpose
Brief description of agent purpose

## Input Requirements
What the agent needs to operate

## Expected Output
What the agent returns

## Invocation
How skills should invoke this agent

## Examples
Usage examples
```

### Creating a New Agent

1. **Define purpose:**
   - Specific, focused task
   - Clear input/output contract
   - Invocation pattern

2. **Document thoroughly:**
   - All input parameters
   - Output format
   - Error conditions
   - Usage examples

3. **Test with skills:**
   - Verify integration
   - Check output format
   - Ensure reliability

## Coding Standards

### Markdown

- Use ATX-style headers (#)
- Include blank lines around headers
- Use fenced code blocks with language identifiers
- Maximum line length: 120 characters
- Use reference-style links for repeated URLs

### JSON

- Use 2-space indentation
- No trailing commas
- Double quotes for strings
- Validate before committing

### File Naming

- Use kebab-case: `file-name.md`
- Lowercase only
- Descriptive names
- No spaces or special characters

### Documentation

- Write clear, concise descriptions
- Include examples where appropriate
- Use proper grammar and spelling
- Link to related documentation

## Pull Request Process

### Before Submitting

1. **Test thoroughly:**
   - Install in development environment
   - Test all affected functionality
   - Verify no regressions

2. **Update documentation:**
   - Update relevant .md files
   - Add examples if applicable
   - Update CLAUDE.md if needed

3. **Follow commit conventions:**
   ```
   type(scope): description

   - feat: New feature
   - fix: Bug fix
   - docs: Documentation changes
   - refactor: Code refactoring
   - test: Test additions
   - chore: Maintenance tasks
   ```

   Examples:
   ```
   feat(skills): add automation-optimizer skill
   fix(debugger): correct error parsing for n8n
   docs(excel): update API limits documentation
   ```

### Submitting Pull Request

1. **Create pull request:**
   - Clear, descriptive title
   - Detailed description of changes
   - Link related issues
   - Screenshots if applicable

2. **PR template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (describe)

## Changes Made
- List of specific changes
- What was added/modified/removed

## Testing Performed
- How changes were tested
- Test results

## Related Issues
Closes #issue_number

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated checks:**
   - JSON validation
   - Markdown linting
   - File structure verification

2. **Manual review:**
   - Code quality
   - Documentation completeness
   - Test coverage
   - Best practices adherence

3. **Feedback:**
   - Address reviewer comments
   - Make requested changes
   - Re-request review

4. **Merge:**
   - Squash commits if appropriate
   - Update version if needed
   - Close related issues

## Testing Guidelines

### Manual Testing

1. **Installation test:**
```bash
/plugin marketplace add YOUR-FORK/AutomationHelper_plugins
/plugin install automation-helper
/plugin info automation-helper
```

2. **Skill activation test:**
   - Use trigger phrases
   - Verify correct skill activates
   - Check output format

3. **Documentation test:**
   - Verify agents can find information
   - Test search patterns
   - Ensure XML parsing works

4. **Integration test:**
   - Test complete workflows
   - Verify sub-agent coordination
   - Check error handling

### Test Cases

Create test cases for:
- New skills
- Modified functionality
- Edge cases
- Error conditions

**Template:**
```markdown
### Test Case: Skill Activation

**Input:** "Optimize this Power Automate flow"
**Expected:** automation-refactor skill activates
**Actual:** [Record result]
**Status:** Pass/Fail
```

## Recognition

Contributors will be recognized in:
- README.md (Contributors section)
- Release notes
- GitHub contributors page

Significant contributions may result in:
- Co-authorship acknowledgment
- Maintainer status (for consistent, quality contributions)

## Questions?

- **GitHub Discussions:** [Ask questions](https://github.com/MacroMan5/AutomationHelper_plugins/discussions)
- **GitHub Issues:** [Report bugs](https://github.com/MacroMan5/AutomationHelper_plugins/issues)
- **Email:** [email protected]

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing!** 🎉
