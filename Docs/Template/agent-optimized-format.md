# Agent-Optimized Documentation Format

## Purpose

Format standardisé pour maximiser la recherche et l'extraction d'information par les agents Claude Code.

## Principes Clés

1. **Machine-Readable Metadata**: YAML frontmatter pour métadonnées structurées
2. **XML Tags**: Sections critiques balisées pour extraction précise
3. **Hierarchie Stricte**: Structure prévisible et uniforme
4. **Keywords**: Tags sémantiques pour recherche contextuelle
5. **Liens Internes**: Références croisées entre documents

## Format Standard - Overview Documents

```markdown
---
type: connector-overview
connector_name: SharePoint
connector_type: standard|premium|custom
version: 1.0
last_updated: 2024-10-31
keywords: [sharepoint, lists, documents, collaboration]
related_connectors: [OneDrive, Office 365]
api_limits:
  calls_per_minute: 10
  calls_per_hour: 600
  max_file_size_mb: 90
---

# {Connector Name} Connector Overview

<official_docs>
https://learn.microsoft.com/en-us/connectors/{connector-id}/
</official_docs>

<description>
{2-3 sentence summary of connector purpose and capabilities}
</description>

<capabilities>
## Core Capabilities
- Capability 1
- Capability 2
- Capability 3

## Supported Operations
- Operation type 1
- Operation type 2
</capabilities>

<api_limits>
## Rate Limits
- **{X} calls per {Y} seconds** per connection
- Throttling behavior: {description}

## Size Limits
- Max file size: **{X}MB**
- Max batch size: **{Y} items**
- Max request size: **{Z}KB**

## Timeout Limits
- Default timeout: {X} seconds
- Max timeout: {Y} seconds
</api_limits>

<critical_limitations>
## {Category 1}
<limitation id="lim-001" severity="high">
**{Limitation title}**: {Description and impact}
- Affected operations: {list}
- Workaround: {solution or "none"}
</limitation>

<limitation id="lim-002" severity="medium">
**{Another limitation}**: {Description}
</limitation>
</critical_limitations>

<authentication>
## Auth Methods
- OAuth 2.0 (recommended)
- Service Principal
- Legacy auth (if applicable)

## Required Permissions
- {Permission 1}: {Why needed}
- {Permission 2}: {Why needed}
</authentication>

<common_use_cases>
1. **{Use Case 1}**: {Description}
   - Triggers: {list}
   - Actions: {list}

2. **{Use Case 2}**: {Description}
   - Pattern: {workflow pattern}
</common_use_cases>

<best_practices>
## Performance
- {Practice 1}
- {Practice 2}

## Reliability
- {Practice 1}
- {Practice 2}

## Security
- {Practice 1}
- {Practice 2}
</best_practices>

<troubleshooting>
## Common Errors

### Error Code: {code}
<error id="err-001">
- **Symptom**: {what user sees}
- **Cause**: {why it happens}
- **Solution**: {how to fix}
- **Prevention**: {how to avoid}
</error>
</troubleshooting>

<related_docs>
- Actions: [actions.md](./actions.md)
- Triggers: [triggers.md](./triggers.md)
- Related Connectors: {list with links}
</related_docs>
```

## Format Standard - Actions Documents

```markdown
---
type: connector-actions
connector_name: {Name}
action_count: {number}
version: 1.0
last_updated: 2024-10-31
keywords: [action-specific, keywords]
categories: [create, read, update, delete, search]
---

# {Connector Name} - Actions

<action_summary>
Total Actions: {X}
Categories: {list}
</action_summary>

<action_categories>
- **Create Operations**: {count} actions
- **Read Operations**: {count} actions
- **Update Operations**: {count} actions
- **Delete Operations**: {count} actions
- **Special Operations**: {count} actions
</action_categories>

---

## {Category Name}

### {Action Name}

<action id="action-{unique-id}" category="{category}" complexity="low|medium|high">

<action_header>
**Type**: {create|read|update|delete|custom}
**Complexity**: {low|medium|high}
**Throttling Impact**: {low|medium|high}
</action_header>

<description>
{1-2 sentence clear description of what this action does}
</description>

<parameters>
#### Required Parameters
- **{param_name}** (`{type}`): {description}
  - Format: {format if applicable}
  - Example: `{example_value}`

#### Optional Parameters
- **{param_name}** (`{type}`): {description}
  - Default: `{default_value}`
  - Valid values: {range or options}
</parameters>

<returns>
**Return Type**: {type}
**Structure**:
```json
{
  "property1": "value",
  "property2": 123
}
```

**Key Fields**:
- `{field}`: {description}
- `{field}`: {description}
</returns>

<limitations>
- **{Limitation 1}**: {Impact and details}
- **{Limitation 2}**: {Impact and details}
</limitations>

<use_cases>
1. **{Use Case 1}**: {When to use}
2. **{Use Case 2}**: {When to use}
</use_cases>

<best_practices>
1. **{Practice}**: {Why and how}
2. **{Practice}**: {Why and how}
</best_practices>

<example>
```json
{
  "action": "{action_name}",
  "parameters": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

**Use Case**: {What this example demonstrates}
**Expected Result**: {What should happen}
</example>

<common_errors>
- **Error**: {error message or code}
  - **Cause**: {why}
  - **Fix**: {how to resolve}
</common_errors>

<related_actions>
- Often used with: [{action1}](#action-id), [{action2}](#action-id)
- Alternative to: [{action3}](#action-id)
</related_actions>

</action>

---

{Repeat for each action}
```

## Format Standard - Triggers Documents

```markdown
---
type: connector-triggers
connector_name: {Name}
trigger_count: {number}
version: 1.0
last_updated: 2024-10-31
keywords: [trigger-specific, keywords]
trigger_types: [polling, webhook, scheduled]
---

# {Connector Name} - Triggers

<trigger_summary>
Total Triggers: {X}
Types:
- Polling: {count}
- Webhook: {count}
- Scheduled: {count}
</trigger_summary>

---

## {Trigger Name}

<trigger id="trigger-{unique-id}" type="polling|webhook|scheduled" frequency="high|medium|low">

<trigger_header>
**Type**: {polling|webhook|scheduled}
**Frequency**: {How often it checks}
**Latency**: {Expected delay}
</trigger_header>

<description>
{1-2 sentence description of when this trigger fires}
</description>

<parameters>
#### Required Parameters
- **{param_name}** (`{type}`): {description}

#### Optional Parameters
- **{param_name}** (`{type}`): {description}
  - Impact: {performance/behavior impact}
</parameters>

<behavior>
**Polling Interval**: {if applicable}
**Batch Size**: {how many items per trigger}
**Deduplication**: {how duplicates are handled}
**Ordering**: {order of items}
</behavior>

<outputs>
**Trigger Output Structure**:
```json
{
  "property1": "value",
  "property2": 123
}
```

**Dynamic Content Available**:
- `{field}`: {description and usage}
</outputs>

<limitations>
- **{Limitation 1}**: {Impact}
- **{Limitation 2}**: {Impact}
</limitations>

<filtering>
**Filtering Options**:
- Server-side: {what can be filtered}
- Client-side: {what needs condition action}

**Recommendation**: {best filtering approach}
</filtering>

<use_cases>
1. **{Use Case}**: {Scenario description}
2. **{Use Case}**: {Scenario description}
</use_cases>

<best_practices>
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}
</best_practices>

<example>
**Scenario**: {What you're trying to achieve}

**Configuration**:
```json
{
  "trigger": "{trigger_name}",
  "parameters": {
    "param1": "value1"
  }
}
```

**Expected Behavior**: {What happens when trigger fires}
</example>

<performance_impact>
- **Throttling**: {impact on API limits}
- **Resource Usage**: {memory/processing impact}
- **Scaling**: {behavior with high volume}
</performance_impact>

<related_triggers>
- Alternative: [{trigger}](#trigger-id)
- Often paired with actions: {list}
</related_triggers>

</trigger>

---

{Repeat for each trigger}
```

## Benefits for Agent Search

### 1. YAML Frontmatter
```yaml
keywords: [specific, searchable, terms]
categories: [organized, taxonomies]
```
Agents can quickly filter by metadata without parsing entire document.

### 2. XML Tags
```xml
<limitation id="lim-001" severity="high">
```
Precise extraction of critical information sections.

### 3. Unique IDs
```markdown
<action id="action-create-file">
```
Direct linking and reference between documents.

### 4. Structured Hierarchy
Predictable document structure means agents know exactly where to find information.

### 5. Semantic Keywords
Tags like `severity`, `complexity`, `type` provide context for search relevance.

## Search Optimization Examples

### Finding Critical Limitations
Agent can grep for: `<limitation.*severity="high"`

### Finding Actions by Category
Agent can search frontmatter: `categories: [create]`

### Finding Related Operations
Agent can follow: `<related_actions>` tags

### Error Troubleshooting
Agent can search: `<error id="err-{code}">` for exact error

### Performance Issues
Agent can search: `<performance_impact>` sections

## Migration Path

To migrate existing docs to this format:

1. **Add YAML Frontmatter**
   - Extract keywords from content
   - Add metadata (type, version, dates)

2. **Wrap Sections in XML Tags**
   - Identify critical sections
   - Add structured tags with attributes

3. **Add Unique IDs**
   - Create consistent ID scheme
   - Link related content

4. **Enhance Structure**
   - Ensure consistent hierarchy
   - Add missing standard sections

5. **Add Semantic Attributes**
   - Severity levels
   - Complexity ratings
   - Type classifications

## Validation Checklist

- [ ] YAML frontmatter present and complete
- [ ] All critical sections have XML tags
- [ ] Unique IDs for all actions/triggers/limitations
- [ ] Keywords relevant and comprehensive
- [ ] Cross-references use proper links
- [ ] Consistent hierarchy depth
- [ ] All required sections present
- [ ] Examples are concrete and testable
- [ ] Related content linked

## Template Files

See these templates for reference:
- `template-overview-v2.md` - Enhanced overview template
- `template-actions-v2.md` - Enhanced actions template
- `template-triggers-v2.md` - Enhanced triggers template
