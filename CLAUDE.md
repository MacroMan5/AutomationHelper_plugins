# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

⚠️ **Alpha Version** - This plugin is in active development. Power Automate and n8n focus. Make/Zapier not yet supported.

## Repository Purpose

**Automation Helper**: AI assistant for Power Automate and n8n workflows. Help design, build, debug, and refactor automation workflows.

## ⚠️ CRITICAL - Context Limits & Best Practices

**When users provide large workflows (>300 lines), ALWAYS:**

1. **Ask them to section it**: "This workflow is large. For better results, please share just the section with the error (around 200-300 lines)."

2. **Don't try to process 3000-line JSONs**: You'll hit context limits and provide poor results.

3. **Request data structure info**: "Can you confirm what data type this variable contains? Array of strings or array of objects?"

4. **Focus on one problem**: If multiple issues, address them sequentially, not all at once.

5. **Be honest about limits**: If the workflow uses unsupported connectors (Make, Zapier, advanced SharePoint), say so upfront.

**Example response to large workflow:**
```
"I see this is a large workflow (1500+ lines). For the best results, could you:
1. Share just the section with the error (the loop at lines 200-400)
2. Explain what that section should do
3. Tell me what data type the variable contains

This helps me provide accurate fixes instead of guessing from too much context."
```

**NEVER:** Try to debug 3000 lines of JSON at once. You'll fail.

## What This Repository Provides

### 🎯 6 Specialized Skills (Automation Lifecycle)
- **automation-brainstorm** 💡 - Interactive workflow design advisor
- **automation-build-flow** 🏗️ - Complete workflow JSON generator
- **automation-debugger** 🔧 - Deep error analysis with fix generation
- **automation-quick-fix** ⚡ - Fast fixes for common error patterns
- **automation-refactor** 🔄 - Workflow optimization & best practices application
- **automation-validator** ✓ - Pre-deployment validation & quality checks

### 📚 Comprehensive Platform Documentation
- **Power Automate**: 4 core connectors (Forms, Excel, Outlook, Teams) + 6 built-in categories - 100% complete
- **n8n**: Core nodes, AI integrations, apps, databases - Growing library
- **Agent-optimized format**: XML tags, YAML frontmatter, unique IDs for precise search

### 🤖 Specialized Sub-Agents
- **flow-builder**: Generates copy-paste ready Power Automate JSON
- **powerautomate-docs-researcher**: Searches local Power Automate documentation
- **flow-debugger**: Debugs flows using comprehensive documentation
- **flow-documenter**: Creates natural language documentation from flow JSON

## Architecture Overview

```
/debug_powerAutomate/
├── .claude/
│   ├── skills/                    # 6 automation workflow skills
│   │   ├── automation-brainstorm/     # Interactive planning
│   │   ├── automation-build-flow/     # JSON generation
│   │   ├── automation-debugger/       # Error debugging
│   │   ├── automation-quick-fix/      # Fast common fixes
│   │   ├── automation-refactor/       # Workflow optimization
│   │   └── automation-validator/      # Pre-deployment validation
│   ├── agents/                    # Specialized sub-agents
│   │   ├── flow-builder.md           # Flow JSON generator
│   │   ├── docs-researcher.md        # Documentation searcher
│   │   ├── flow-debugger.md          # Flow debugger
│   │   └── flow-documenter.md        # Flow documenter
│   └── output-style/              # Standardized output formats
│       ├── debug-report.md           # Debug report template
│       ├── research-findings.md      # Research output format
│       └── flow-documentation.md     # Flow docs format
├── Docs/
│   ├── PowerAutomateDocs/         # Power Automate documentation
│   │   ├── Forms/                    # Microsoft Forms (100%)
│   │   ├── Excel/                    # Excel Online (100%)
│   │   ├── Outlook/                  # Office 365 Outlook (100%)
│   │   ├── Teams/                    # Microsoft Teams (100%)
│   │   ├── SharePoint/               # SharePoint (20% - needs update)
│   │   ├── OneDrive/                 # OneDrive (20% - needs update)
│   │   ├── BuiltIn/                  # Built-in connectors
│   │   └── templates/                # Documentation templates
│   └── N8NDocs/                   # n8n documentation
│       ├── Core/                     # Core nodes (HTTP, Webhook, Code, etc.)
│       ├── AI/                       # AI integration nodes
│       ├── Apps/                     # Third-party integrations
│       ├── Database/                 # Database nodes
│       └── templates/                # Documentation templates
├── flow.json                      # Power Automate flow definitions
└── erreur.json                    # Error logs for debugging
```

## Quick Start: When to Use What

### 🎨 Creating New Workflows

**Scenario 1: You have an idea, need planning**
```
Use: automation-brainstorm skill
→ Asks clarifying questions
→ Researches best practices
→ Generates implementation plan
→ Ready for automation-build-flow
```

**Scenario 2: You have clear requirements**
```
Use: automation-build-flow skill
→ Provide detailed requirements
→ Generates complete workflow JSON
→ Copy-paste ready for platform
```

**Example**: "Create a Power Automate flow that monitors SharePoint for new files and sends email notifications"

### 🔧 Fixing Broken Workflows

**Scenario 1: Common error (401, 403, 429)**
```
Use: automation-quick-fix skill
→ Immediate pattern-matched solution
→ Platform-specific fix snippet
→ Fast resolution
```

**Scenario 2: Complex or unknown error**
```
Use: automation-debugger skill
→ Analyzes error in depth
→ Searches documentation for root cause
→ Generates complete fix_bloc.json
→ Structured debug report
```

**Example**: "My Excel flow is getting 429 throttling errors" or "Debug this error file"

### 🔄 Refactoring & Optimizing Workflows

**Scenario: Improve existing working workflow**
```
Use: automation-refactor skill
→ Analyzes current workflow
→ Applies best practices from documentation
→ Optimizes performance (API calls, execution time)
→ Enhances reliability (error handling, retry logic)
→ Improves maintainability (naming, structure)
→ Outputs refactored JSON + detailed report
→ Suggests additional optimizations
```

**Example**: "Optimize this flow to reduce API calls" or "Refactor this workflow to follow best practices" or "Improve error handling in this automation"

### ✓ Validating Workflows

**Before deployment or after changes**
```
Use: automation-validator skill
→ Syntax validation
→ Best practices check
→ Security scanning
→ Performance analysis
→ Comprehensive report
```

**Example**: "Validate this flow.json before I deploy it"

## Using the Skills System

### Triggering Skills

Skills auto-activate based on your language:

| Your Request | Skill Activated |
|--------------|----------------|
| "create workflow", "design automation", "need ideas" | automation-brainstorm |
| "build this flow", "generate JSON" | automation-build-flow |
| "debug this error", provides error JSON | automation-debugger |
| "401 error", "429 throttling", "quick fix" | automation-quick-fix |
| "optimize", "refactor", "improve", "enhance" | automation-refactor |
| "validate workflow", "check before deploy" | automation-validator |

### Complete Workflow Examples

**Example 1: New Automation from Scratch**
```
You: "I want to automate sending weekly reports from Excel to Teams"

→ automation-brainstorm activates
  - Asks: Which Excel file? Which Teams channel? What data?
  - Researches: Excel connector best practices, Teams integration
  - Outputs: Complete implementation plan

You: "Build this workflow"

→ automation-build-flow activates
  - Generates: Complete Power Automate JSON
  - Outputs: Copy-paste ready flow.json

You: "Validate this before I deploy"

→ automation-validator activates
  - Checks: Syntax, best practices, security
  - Outputs: Validation report with recommendations
```

**Example 2: Debug and Fix Existing Flow**
```
You: "My SharePoint flow is failing with this error: [paste error]"

→ automation-debugger activates (if complex)
   OR
→ automation-quick-fix activates (if common pattern)
  - Analyzes: Error message and flow context
  - Searches: PowerAutomateDocs/SharePoint/ for solutions
  - Outputs: fixed JSON with complete solution

You: "Validate the fix"

→ automation-validator activates
  - Verifies: Fix correctness and completeness
  - Outputs: Validation report
```

**Example 3: Refactor and Optimize Working Flow**
```
You: "Optimize this Power Automate flow to reduce API calls and improve reliability"
[Provides workflow JSON]

→ automation-refactor activates
  - Analyzes: Current workflow structure and patterns
  - Researches: Best practices from PowerAutomateDocs/
  - Identifies: N+1 query problem, missing error handling, poor naming
  - Generates: Refactored JSON with:
    * 95% fewer API calls (using $expand)
    * Comprehensive error handling
    * Clear action names
    * Retry logic
  - Outputs: Refactored JSON + detailed report
  - Suggests: Additional optimizations (caching, batching, monitoring)

You: "Validate the refactored flow"

→ automation-validator activates
  - Checks: All improvements applied correctly
  - Verifies: No new issues introduced
  - Confirms: Production-ready
  - Outputs: Validation report
```

## Documentation Search: Finding Information Fast

### Documentation Structure

**Power Automate** (Docs/PowerAutomateDocs/):
```
✅ Forms/         - Microsoft Forms (100% complete)
✅ Excel/         - Excel Online (100% complete)
✅ Outlook/       - Office 365 Outlook (100% complete)
✅ Teams/         - Microsoft Teams (100% complete)
✅ BuiltIn/       - Control, Data Operation, HTTP, Schedule, Variable
🔄 SharePoint/   - SharePoint connector (20% - needs update)
🔄 OneDrive/     - OneDrive connector (20% - needs update)
```

**n8n** (Docs/N8NDocs/):
```
✅ Core/         - HTTP Request, Webhook, Code, Schedule, Set
✅ AI/           - OpenAI, Anthropic, LangChain
✅ Apps/         - Google Sheets, Slack, Gmail, Notion, GitHub
✅ Database/     - PostgreSQL, MySQL, MongoDB
```

### Quick Search Commands

#### Find API Rate Limits
```bash
# All Power Automate connectors
grep -r "calls_per_minute:" Docs/PowerAutomateDocs/*/overview.md

# Specific connector
grep "calls_per_minute:" Docs/PowerAutomateDocs/Excel/overview.md
```

#### Find Critical Limitations
```bash
# All critical issues
grep -r '<limitation.*severity="critical"' Docs/PowerAutomateDocs/

# Specific connector
grep '<limitation.*severity="critical"' Docs/PowerAutomateDocs/Teams/overview.md
```

#### Find Specific Error Codes
```bash
# 429 throttling errors
grep -r '<error id="err-429"' Docs/PowerAutomateDocs/

# 403 permission errors
grep -r '<error id="err-403"' Docs/PowerAutomateDocs/
```

#### Find Actions by Category
```bash
# All "create" actions
grep -r 'category="create"' Docs/PowerAutomateDocs/*/actions.md

# Low complexity actions
grep -r 'complexity="low"' Docs/PowerAutomateDocs/*/actions.md
```

#### Search by Keywords
```bash
# Find connectors with "approval" capability
grep -r "keywords:.*approval" Docs/PowerAutomateDocs/*/overview.md

# Find database-related connectors
grep -r "keywords:.*database" Docs/PowerAutomateDocs/*/overview.md
```

### Search Patterns by Use Case

#### Debugging a Throttling Error (429)
1. Find connector's API limits:
```bash
grep -A 10 "<api_limits>" Docs/PowerAutomateDocs/Excel/overview.md
```

2. Find throttling error details:
```bash
grep -A 10 '<error id="err-429"' Docs/PowerAutomateDocs/Excel/overview.md
```

3. Find throttling best practices:
```bash
grep -A 5 "Throttling Management" Docs/PowerAutomateDocs/Excel/overview.md
```

#### Understanding a Limitation
1. Find all limitations:
```bash
grep -A 20 "<critical_limitations>" Docs/PowerAutomateDocs/Excel/overview.md
```

2. Find specific limitation by ID:
```bash
grep -A 10 'id="lim-001"' Docs/PowerAutomateDocs/Excel/overview.md
```

3. Find workarounds:
```bash
grep -B 2 -A 2 "Workaround:" Docs/PowerAutomateDocs/Excel/overview.md
```

#### Finding Alternative Connectors
1. List connectors with similar keywords:
```bash
grep -l "keywords:.*email" Docs/PowerAutomateDocs/*/overview.md
```

2. Find related connectors:
```bash
grep "related_connectors:" Docs/PowerAutomateDocs/Forms/overview.md
```

### Documentation Format (Agent-Optimized)

All documentation uses **format v2** with:

**YAML Frontmatter** (top of files):
```yaml
type: connector-overview
connector_name: Excel Online
keywords: [spreadsheet, table, rows, excel]
api_limits:
  calls_per_minute: 1.67
  calls_per_hour: 100
```

**XML Tags** (throughout documents):
```xml
<limitation id="lim-001" severity="critical">
<action id="action-create-row" category="create" complexity="low">
<error id="err-429" http_code="429">
```

**Benefits**:
- Fast agent search via grep/XML extraction
- Direct navigation via unique IDs
- Precise filtering by severity/category/complexity
- Structured for LLM consumption

## Specialized Sub-Agents

### When Claude Uses Sub-Agents

Sub-agents are automatically invoked by skills, but you can understand when they're used:

#### flow-builder
**Used by**: automation-build-flow, automation-debugger
**Purpose**: Generates complete workflow JSON
**Output**: Copy-paste ready JSON for Power Automate/n8n/Make/Zapier

**Key Feature**: Outputs exact format expected by platform's "Paste code" feature
- Valid syntax (no placeholders)
- Proper GUIDs and connection names
- Correct expression syntax
- Complete runAfter dependencies

#### powerautomate-docs-researcher
**Used by**: automation-debugger, automation-brainstorm
**Purpose**: Searches PowerAutomateDocs/ for solutions
**Triggers**: Questions about connectors, errors, limitations, best practices

**Example queries**:
- "What are Excel connector API limits?"
- "Why am I getting 429 errors with Forms?"
- "Which connectors support approval workflows?"

#### flow-debugger
**Used by**: automation-debugger skill
**Purpose**: Analyzes flow.json + erreur.json for root causes
**Output**: Structured debug report with fixes

#### flow-documenter
**Used by**: After flow creation
**Purpose**: Generates natural language documentation from flow JSON
**Output**: Comprehensive flow explanation

## Flow Files

### flow.json
Power Automate flow definitions in JSON format:
```json
{
  "definition": {
    "$schema": "https://schema.management.azure.com/...",
    "triggers": { /* entry points */ },
    "actions": { /* operations */ },
    "outputs": {}
  }
}
```

### erreur.json
Error logs for debugging:
- Error messages and codes
- Failing action information
- Stack traces and context

**Usage**: Provide to automation-debugger skill for analysis

## Platform-Specific Knowledge

### Power Automate

**Flow Structure Components**:
1. **Triggers** - Manual, scheduled, event-based
2. **Actions** - API calls, data operations, control flow
3. **Conditions** - Logic branching
4. **Loops** - Apply to each, Do until
5. **Variables** - State management
6. **Error Handling** - Scopes with configure run after

**Critical Limitations**:

**Excel Online**:
- 100 calls/60 seconds
- 25MB file size limit
- 256 rows default retrieval (use pagination)
- Write access required even for reads
- File lock up to 6 minutes

**Forms**:
- 300 calls/60 seconds
- Organizational accounts only
- Real-time webhook vs 24-hour polling

**Outlook**:
- 300 calls/60 seconds
- 49MB email size limit
- 500MB send batch per 5 minutes
- 70 max concurrent requests

**Teams**:
- 100 calls/60 seconds
- 3-minute trigger polling
- Cannot post to private channels
- 25-user chat creation limit

**SharePoint**:
- 600 calls/60 seconds
- 90MB attachment limit
- No custom templates support
- Generic lists/libraries only

**OneDrive**:
- 100 calls/60 seconds
- 50MB file size for triggers
- No cross-tenant support

### n8n

**Key Node Categories**:
- **Core**: HTTP Request, Webhook, Code, Schedule
- **AI**: OpenAI, Anthropic, LangChain
- **Apps**: Google Sheets, Slack, Gmail, Notion
- **Database**: PostgreSQL, MySQL, MongoDB

**Best Practices**:
- Use error handling nodes (Error Trigger)
- Implement pagination for large datasets
- Add logging for debugging
- Test with sample data first

## Common Debugging Workflow

### Step 1: Identify the Error
- Review error messages in erreur.json
- Locate failing action in flow.json
- Note error code (401, 403, 429, 404, etc.)

### Step 2: Use Appropriate Skill
**Common error?** → automation-quick-fix
**Complex error?** → automation-debugger

### Step 3: Consult Documentation
- Navigate to Docs/PowerAutomateDocs/{ConnectorType}/
- Check overview.md for limitations
- Review actions.md or triggers.md for specifics
- Look for error ID in XML tags

### Step 4: Apply Fix
- Update flow.json with suggested changes
- Validate with automation-validator
- Test with sample data
- Monitor for errors

### Step 5: Document Resolution
- Note root cause
- Save fix pattern for future reference
- Update documentation if needed

## Best Practices

### Workflow Design
1. Always include error handling (Scope + Configure run after)
2. Initialize variables at flow start
3. Implement retry logic for transient failures
4. Use appropriate trigger types
5. Filter data at source to minimize API calls
6. Add descriptive names to all actions

### Performance
1. Enable concurrency for independent operations
2. Use batch operations when available
3. Implement caching for frequently accessed data
4. Monitor and optimize for API throttling
5. Use properties-only triggers when content not needed

### Reliability
1. Handle all expected error codes
2. Implement idempotency for critical operations
3. Add retry logic with exponential backoff
4. Log critical operations for debugging
5. Set appropriate timeouts on loops

### Security
1. Store credentials securely (never hardcode)
2. Use managed identity when possible
3. Implement least privilege access
4. Validate all input data
5. Sanitize data for injection vulnerabilities

## Error Patterns Reference

### Throttling Errors (429)
**Symptoms**: Too many API calls
**Solution**:
- Check API limits in connector overview
- Implement delays between calls
- Use batch operations
- Reference: `Docs/PowerAutomateDocs/{connector}/overview.md`

### Authentication Errors (401/403)
**Symptoms**: Access denied
**Solution**:
- Verify connection credentials
- Check permission requirements
- Review conditional access policies
- Reference: `Docs/PowerAutomateDocs/{connector}/actions.md`

### Data Format Errors
**Symptoms**: Parse failures, type mismatches
**Solution**:
- Validate JSON schema (Parse JSON action)
- Check required parameters
- Verify data types
- Reference: `Docs/PowerAutomateDocs/BuiltIn/data-operation.md`

### Timeout Errors
**Symptoms**: Operations taking too long
**Solution**:
- Check file sizes (OneDrive 50MB limit)
- Review Do until timeout settings
- Optimize query filters
- Reference: `Docs/PowerAutomateDocs/BuiltIn/control.md`

### Not Found Errors (404)
**Symptoms**: Resource doesn't exist
**Solution**:
- Verify resource paths/IDs
- Check permissions
- Confirm resource existence
- Reference: Connector-specific actions.md

## Official Resources

### Power Automate
- **Documentation**: https://learn.microsoft.com/en-us/power-automate/
- **Connectors**: https://learn.microsoft.com/en-us/connectors/
- **Community**: https://powerusers.microsoft.com/

### n8n
- **Documentation**: https://docs.n8n.io/
- **Node Reference**: https://docs.n8n.io/integrations/builtin/
- **Community**: https://community.n8n.io/
- **GitHub**: https://github.com/n8n-io/n8n

## Advanced Features

### Multi-Platform Support
Skills work with any JSON-based automation platform:
- Power Automate
- n8n
- Make (Integromat)
- Zapier
- Custom platforms

**How it works**: Skills auto-detect platform from context and generate platform-specific JSON.

### Documentation-First Approach
- No hallucinations - always references real docs
- Cites specific files and sections
- Validates against official sources
- Updates regularly from Microsoft Learn / n8n docs

### Sub-Agent Orchestration
Skills coordinate multiple sub-agents:
- Research agents find documentation
- Flow-builder agents generate JSON
- Validation agents check quality
- Documentation agents explain flows

### Production-Ready Output
All generated JSON is:
- ✅ Complete (no placeholders)
- ✅ Valid syntax
- ✅ Platform-specific format
- ✅ Ready to import/paste

## Adding New Platform Support

To add a new automation platform:

1. **Add Documentation Structure**:
```
Docs/[NewPlatform]_Documentation/
├── overview.md
├── connectors/ or nodes/
├── common-errors.md
└── best-practices.md
```

2. **Skills Auto-Adapt**:
- automation-brainstorm researches new docs
- automation-build-flow generates platform-specific JSON
- automation-debugger finds fixes in new docs
- automation-validator checks platform schema

3. **No Code Changes Needed**:
Skills are platform-agnostic and documentation-driven.

## Quick Reference Card

### I want to...

| Goal | Use | Example |
|------|-----|---------|
| Plan new workflow | automation-brainstorm | "Design workflow to sync Salesforce to Excel" |
| Build workflow | automation-build-flow | "Generate JSON for file approval flow" |
| Fix common error | automation-quick-fix | "Getting 429 errors in Excel flow" |
| Debug complex error | automation-debugger | "Analyze this error.json file" |
| Refactor/optimize flow | automation-refactor | "Optimize this flow to reduce API calls" |
| Validate before deploy | automation-validator | "Check this workflow.json for issues" |
| Find API limits | Search docs | `grep "calls_per_minute:" Docs/PowerAutomateDocs/Excel/overview.md` |
| Find error solutions | Search docs | `grep -r '<error id="err-429"' Docs/PowerAutomateDocs/` |
| Understand limitation | Search docs | `grep -A 10 'id="lim-001"' Docs/PowerAutomateDocs/Excel/overview.md` |

### Key Commands

```bash
# Search documentation
grep -r "keyword" Docs/PowerAutomateDocs/
grep -r "keyword" Docs/N8NDocs/

# View flow definition
cat flow.json

# View error logs
cat erreur.json

# Check connector documentation status
cat Docs/PowerAutomateDocs/DOCUMENTATION_STATUS.md

# List available connectors
ls Docs/PowerAutomateDocs/
ls Docs/N8NDocs/
```

## Tips for Working with Claude Code in This Repo

1. **Be Platform-Specific**: Always mention "Power Automate", "n8n", "Make", etc.

2. **Provide Context**: Include flow.json and erreur.json when debugging

3. **Use Precise Language**:
   - ✅ "Debug this 429 throttling error in Excel connector"
   - ❌ "Fix my flow"

4. **Leverage Skills**: Let skills guide you through complex tasks

5. **Reference Documentation**: Point to specific connectors for faster results

6. **Validate Always**: Run automation-validator before deployment

7. **Iterate**: Use automation-brainstorm → build-flow → validator workflow

## Repository Maintenance

### Documentation Updates
- **Monthly**: Check Microsoft Learn / n8n docs for updates
- **Quarterly**: Add new connectors based on usage patterns
- **Annually**: Full documentation review and validation

### Next Priorities
1. Update SharePoint connector to 100% (currently 20%)
2. Update OneDrive connector to 100% (currently 20%)
3. Add Dataverse connector documentation
4. Add Approvals connector documentation
5. Expand n8n documentation coverage

### Contributing to Documentation
1. Use templates from `Docs/PowerAutomateDocs/templates/` or `Docs/N8NDocs/Templates/`
2. Follow agent-optimized format v2
3. Include YAML frontmatter with metadata
4. Use XML tags for structured sections
5. Assign unique IDs to elements
6. Update DOCUMENTATION_STATUS.md

---

**Version**: 0.1.0-alpha
**Last Updated**: 2025-10-31
**Skills**: 6 (all in alpha development)
**Platforms**: Power Automate (partial), n8n (core nodes only)
**Status**: Active Development - Contributions Welcome!
