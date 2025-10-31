# Automation Workflow Skills

Complete suite of automation workflow skills for Claude Code supporting Power Automate, n8n, Make, Zapier, and other platforms.

## Supported Platforms

- **Power Automate** (Microsoft)
- **n8n** (Open-source automation)
- **Make** (formerly Integromat)
- **Zapier**
- **Other JSON-based workflow platforms**

---

## The 5 Skills

### Creation Skills 🎨

#### 1. automation-brainstorm 💡
**Interactive workflow planning and design**

**Triggers**: "create workflow", "build flow", "design automation", "need ideas"

**What it does**:
- Asks smart questions about requirements (AskUserQuestion tool)
- Uses research sub-agent to find platform best practices
- Designs complete workflow architecture
- Generates detailed implementation plan
- Output: Complete plan ready for automation-build-flow

**Use for**: Planning new workflows, complex requirements, need guidance

---

#### 2. automation-build-flow 🏗️
**Workflow JSON generation from plans/requirements**

**Triggers**: "build this workflow", "generate JSON", "create the flow"

**What it does**:
- Takes implementation plan or requirements as input
- Uses flow-builder sub-agent to generate complete JSON
- Produces platform-specific workflow JSON
- Validates syntax and completeness
- Output: Ready-to-import workflow JSON

**Use for**: Building workflows from plans, generating JSON, implementing designs

---

### Maintenance Skills 🔧

#### 3. automation-debugger 🔧
**Complete error debugging with fix generation**

**Triggers**: erreur.json files, error messages, "debug workflow error"

**What it does**:
- Analyzes errors and identifies root causes
- Uses research sub-agent (searches `Docs/{Platform}_Documentation/`)
- Uses flow-builder sub-agent to generate fixes
- Returns structured XML debug report
- Output: Complete fix_bloc.json

**Use for**: Complex errors, unknown issues, need complete solution

---

#### 4. automation-quick-fix ⚡
**Fast fixes for common error patterns**

**Triggers**: Common error codes (401, 403, 404, 429), "quick fix"

**What it does**:
- Pattern matches against common errors
- Provides immediate fix snippets
- Platform-aware solutions
- Escalates to automation-debugger if needed
- Output: Immediate fix snippet

**Use for**: Known error patterns, need fast solution

---

#### 5. automation-validator ✓
**Pre-deployment validation and quality checks**

**Triggers**: "validate workflow.json", "check before deployment"

**What it does**:
- Multi-level validation (syntax → structure → best practices → optimization)
- Platform-specific schema validation
- Security scanning
- Performance analysis
- Output: Comprehensive validation report

**Use for**: Before deployment, quality assurance, learning best practices

---

## Complete Workflows

### Workflow 1: Create New Automation

```
User Idea
    ↓
automation-brainstorm 💡
    ├─ Asks questions
    ├─ Research best practices
    └─ Generates plan
    ↓
Implementation Plan
    ↓
automation-build-flow 🏗️
    ├─ Flow-builder sub-agent
    └─ Generates JSON
    ↓
Complete Workflow JSON
    ↓
automation-validator ✓
    ├─ Validates
    └─ Reports issues
    ↓
Deploy to Platform
```

### Workflow 2: Fix Broken Automation

```
Error Occurs
    ↓
├─ Common? → automation-quick-fix ⚡
│   └─ Fast solution
│
└─ Complex? → automation-debugger 🔧
    ├─ Research root cause
    ├─ Flow-builder generates fix
    └─ Returns fix_bloc.json
    ↓
automation-validator ✓
    └─ Verify fix
    ↓
Redeploy
```

---

## Skill Coordination

```
┌─────────────────────────────────────────┐
│  Creation Phase                          │
├─────────────────────────────────────────┤
│  brainstorm → build-flow → validator    │
│     💡            🏗️           ✓        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Maintenance Phase                       │
├─────────────────────────────────────────┤
│  quick-fix or debugger → validator      │
│      ⚡         🔧           ✓           │
└─────────────────────────────────────────┘
```

---

## When to Use Which Skill

### Starting Point

| Your Situation | Use Skill |
|----------------|-----------|
| "I have an idea for automation" | **brainstorm** |
| "I have complete requirements" | **build-flow** |
| "My workflow has an error" | **quick-fix** or **debugger** |
| "Is my workflow good?" | **validator** |

### Decision Tree

```
What do you need?
│
├─ Create NEW workflow
│  ├─ Complex/unclear → brainstorm → build-flow
│  └─ Simple/clear → build-flow
│
├─ Fix BROKEN workflow
│  ├─ Common error (401,429) → quick-fix
│  └─ Complex error → debugger
│
└─ Validate/Check → validator
```

---

## Sub-Agent Usage

### automation-brainstorm
**Uses**:
- **Research agent** (Explore): Finds platform best practices
- **AskUserQuestion tool**: Interactive requirements gathering

### automation-build-flow
**Uses**:
- **Flow-builder agent** (general-purpose/Plan): Generates JSON
- **AskUserQuestion tool**: Clarifies missing requirements

### automation-debugger
**Uses**:
- **Research agent** (Explore): Finds root causes
- **Flow-builder agent**: Generates fixes

### automation-quick-fix
**Uses**:
- Pattern matching (no sub-agents for speed)
- Escalates to debugger if pattern doesn't match

### automation-validator
**Uses**:
- Read-only validation (no sub-agents)
- Fast quality checks

---

## Documentation Structure

Skills reference platform-specific documentation:

```
Docs/
├── PowerAutomateDocs/           # Power Automate
├── n8n_Documentation/           # n8n
└── [Platform]_Documentation/    # Other platforms
    ├── overview.md
    ├── connectors/ or nodes/
    ├── common-errors.md
    └── best-practices.md
```

---

## Key Features

### 1. Multi-Platform Support
- Works with any JSON-based automation platform
- Auto-detects platform from context
- Platform-specific outputs

### 2. Documentation-First
- Always references real documentation
- No hallucinations
- Cites specific files and sections

### 3. Sub-Agent Orchestration
- Research agents find documentation
- Flow-builder agents generate JSON
- Coordinated workflow between skills

### 4. Production-Ready Output
- Complete JSON (no placeholders)
- Valid syntax
- Platform-specific format
- Ready to import

### 5. Comprehensive Coverage
- Error patterns
- Best practices
- Security scanning
- Performance optimization

---

## Quick Start Examples

### Create Workflow
```
"I want to create a workflow in n8n that syncs data from Salesforce to PostgreSQL every hour"

→ automation-brainstorm asks questions
→ Generates implementation plan
→ automation-build-flow generates n8n JSON
→ automation-validator checks quality
→ Import into n8n
```

### Fix Error
```
"My Power Automate flow is failing with 429 errors"

→ automation-quick-fix provides throttling solution
   OR
→ automation-debugger analyzes and generates fix
→ automation-validator verifies fix
→ Redeploy
```

### Validate Quality
```
"Check my Make scenario for issues before I deploy"

→ automation-validator runs checks
→ Reports findings
→ Recommends improvements
```

---

## Best Practices

### 1. Specify Platform Early
```
✅ "Create a workflow in n8n that..."
✅ "Debug this Power Automate error..."
❌ "Create a workflow..." (platform unclear)
```

### 2. Use Brainstorm for Complex
```
✅ Use brainstorm when:
- Requirements unclear
- Multiple options
- Complex multi-step
- New to platform

✅ Go direct to build-flow when:
- Simple workflow
- Clear requirements
- Following pattern
```

### 3. Always Validate
```
✅ After building: automation-validator
✅ After fixing: automation-validator
✅ Before deploy: automation-validator

Benefits:
- Catch issues early
- Learn best practices
- Security scanning
```

### 4. Quick-Fix First for Common Errors
```
✅ Try quick-fix for: 401, 403, 429, timeout
⏱️ Saves time
❌ Doesn't work? → automation-debugger
```

---

## Adding New Platforms

To add support for a new platform:

1. **Add Documentation**:
   ```
   Docs/[NewPlatform]_Documentation/
   ├── overview.md
   ├── connectors/ or nodes/
   ├── common-errors.md
   └── best-practices.md
   ```

2. **Skills Auto-Adapt**:
   - brainstorm researches new docs
   - build-flow generates platform-specific JSON
   - debugger finds fixes in new docs
   - validator checks platform schema

3. **No Code Changes Needed**:
   - Skills are platform-agnostic
   - Documentation-driven

---

## Learn More

### Documentation

- **Complete Guide**: `../../../COMPLETE_WORKFLOW_GUIDE.md`
- **Quick Start**: `../../../AUTOMATION_SKILLS.md`
- **Skill Details**: Individual SKILL.md files
- **Error Patterns**: `automation-debugger/ERROR-PATTERNS.md`
- **Example**: `automation-debugger/EXAMPLE.md`

### Platform Docs

- **Power Automate**: `../../../Docs/PowerAutomateDocs/`
- **n8n**: `../../../Docs/n8n_Documentation/`
- **Add yours**: `../../../Docs/[Platform]_Documentation/`

---

## Summary

🎯 **5 Skills, Complete Automation Lifecycle**

**Creation**:
- 💡 brainstorm → Interactive planning
- 🏗️ build-flow → JSON generation

**Maintenance**:
- 🔧 debugger → Complete error fixes
- ⚡ quick-fix → Fast common fixes
- ✓ validator → Quality assurance

**Platforms**: Power Automate, n8n, Make, Zapier + extensible

**Workflow**: Idea → Plan → Build → Validate → Deploy

---

**Version**: 2.0 (Complete Suite)
**Skills**: 5 total (2 creation + 3 maintenance)
**Last Updated**: 2025-10-31
