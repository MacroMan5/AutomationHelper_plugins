# {CONNECTOR_NAME} - Actions

<!--
INSTRUCTIONS FOR CLAUDE CODE:
1. Replace {PLACEHOLDERS} with actual values
2. Group actions by logical categories (CRUD, search, etc.)
3. Assign unique IDs: action-001, action-002, etc.
4. Rate complexity: low, medium, high
5. Include concrete examples for each action
6. Link related actions by ID
7. Remove this comment block when done
-->

---
type: connector-actions
connector_name: {CONNECTOR_NAME}
action_count: {X}
version: 1.0
last_updated: {YYYY-MM-DD}
keywords: [{connector}, {category1}, {category2}, {operation-type}]
categories: [create, read, update, delete, search, utility]
---

<action_summary>
**Total Actions**: {X}

**By Category**:
- Create Operations: {X} actions
- Read Operations: {Y} actions
- Update Operations: {Z} actions
- Delete Operations: {A} actions
- Search/Query Operations: {B} actions
- Utility Operations: {C} actions

**Complexity Distribution**:
- Low complexity: {X} actions
- Medium complexity: {Y} actions
- High complexity: {Z} actions
</action_summary>

<action_categories>
## Categories Overview

### Create Operations
{Brief description of create actions available}

### Read Operations
{Brief description of read actions available}

### Update Operations
{Brief description of update actions available}

### Delete Operations
{Brief description of delete actions available}

### Search/Query Operations
{Brief description of search actions available}

### Utility Operations
{Brief description of utility actions available}
</action_categories>

---

## Create Operations

### {Action Name}

<action id="action-{unique-id}" category="create" complexity="low|medium|high" throttle_impact="low|medium|high">

<action_header>
**Operation Type**: Create
**Complexity**: {low|medium|high}
**Throttling Impact**: {low|medium|high}
**Premium**: {yes|no}
</action_header>

<description>
{1-2 clear sentences describing what this action does and when to use it}
</description>

<parameters>
#### Required Parameters

**{parameter_name}** (`{type}`)
- **Description**: {What this parameter does}
- **Format**: {Expected format, e.g., "ISO 8601 date", "JSON object"}
- **Validation**: {Constraints, e.g., "Max 255 characters", "Must be positive integer"}
- **Example**: `{concrete_example_value}`

**{parameter_name}** (`{type}`)
- **Description**: {Description}
- **Format**: {Format}
- **Example**: `{example}`

#### Optional Parameters

**{parameter_name}** (`{type}`)
- **Description**: {What this parameter does}
- **Default**: `{default_value}`
- **Valid Values**: {Range, enum values, or pattern}
- **Impact**: {How this affects behavior}
- **Example**: `{example}`

**{parameter_name}** (`{type}`)
- **Description**: {Description}
- **Default**: `{default}`
- **Example**: `{example}`
</parameters>

<returns>
**Return Type**: `{type}` (e.g., Object, Array, String, Boolean)

**Structure**:
```json
{
  "id": "unique-identifier-123",
  "name": "example-name",
  "created": "2024-10-31T12:00:00Z",
  "status": "success",
  "metadata": {
    "property1": "value1",
    "property2": 123
  }
}
```

**Key Fields**:
- **`id`** (`string`): {Description and when to use}
- **`name`** (`string`): {Description}
- **`created`** (`datetime`): {Description}
- **`status`** (`string`): {Description} - Values: {list valid values}
- **`metadata`** (`object`): {Description}

**Dynamic Content**:
- Use `{output_name}` to reference {field} in subsequent actions
- Access nested properties: `{output_name}/metadata/property1`
</returns>

<limitations>
### Operation-Specific Limits
- **{Limitation 1}**: {Description and impact}
  - **Workaround**: {If available}
- **{Limitation 2}**: {Description and impact}

### Behavioral Notes
- **{Note 1}**: {Important behavior to be aware of}
- **{Note 2}**: {Another consideration}

### Dependencies
- Requires: {Other actions/setup needed first}
- Conflicts with: {What can't be done simultaneously}
</limitations>

<use_cases>
1. **{Use Case 1 Title}**
   - **Scenario**: {When you would use this}
   - **Why This Action**: {Why it's the right choice}
   - **Typical Flow**: {Trigger} → This action → {Next action}

2. **{Use Case 2 Title}**
   - **Scenario**: {When you would use this}
   - **Combined With**: [{related action}](#action-related-id)

3. **{Use Case 3 Title}**
   - **Scenario**: {When you would use this}
   - **Alternative**: Consider [{other action}](#action-alt-id) if {condition}
</use_cases>

<best_practices>
### Performance
1. **{Practice}**: {Explanation}
   - **Impact**: {Performance benefit}
   - **Implementation**: {How to do it}

2. **{Practice}**: {Explanation}

### Reliability
1. **{Practice}**: {Explanation}
   - **Why**: {Reason}
   - **How**: {Implementation}

2. **{Practice}**: {Explanation}

### Data Integrity
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

### Error Handling
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}
</best_practices>

<example>
### Example 1: {Scenario Name}

**Objective**: {What you're trying to accomplish}

**Configuration**:
```json
{
  "action": "{action_technical_name}",
  "parameters": {
    "param1": "concrete-value-1",
    "param2": "concrete-value-2",
    "param3": {
      "nested": "value"
    }
  }
}
```

**Power Automate Expression** (if applicable):
```
@{triggerOutputs()?['body/field1']}
```

**Expected Result**:
```json
{
  "id": "generated-id-123",
  "status": "success"
}
```

**What Happens**: {Step-by-step description of the operation}

---

### Example 2: {Another Scenario}

**Objective**: {What you're trying to accomplish}

**Configuration**:
```json
{
  "action": "{action_technical_name}",
  "parameters": {
    "param1": "@{variables('dynamicValue')}",
    "param2": "@{triggerBody()?['data']}"
  }
}
```

**Use Case**: {When this pattern is useful}

</example>

<common_errors>
### Error: {Error Message or Code}

<error ref="err-action-001">
- **Full Message**: "{Complete error message text}"
- **Cause**: {Why this error occurs}
- **Fix**:
  1. {Step 1 to resolve}
  2. {Step 2 to resolve}
  3. {Step 3 to resolve}
- **Prevention**: {How to avoid in future}
- **Related**: See [limitation lim-XXX](./overview.md#lim-XXX)
</error>

### Error: {Another Error}

<error ref="err-action-002">
{Same structure as above}
</error>

### Validation Errors
- **"{Error}"**: {Cause and fix}
- **"{Error}"**: {Cause and fix}
</common_errors>

<related_actions>
### Commonly Used Together
- **[{Action Name}](#action-id)**: {Why often used together}
- **[{Action Name}](#action-id)**: {Why often used together}

### Alternatives
- **[{Action Name}](#action-id)**: {When to use instead}
  - Use when: {Condition}
  - Difference: {Key distinction}

### Sequential Operations
Typical sequence:
1. [{Prerequisite Action}](#action-id) - {Purpose}
2. **This Action** - {Purpose}
3. [{Follow-up Action}](#action-id) - {Purpose}

### See Also
- Overview: [Limitations](./overview.md#critical_limitations)
- Related Trigger: [{Trigger Name}](./triggers.md#trigger-id)
</related_actions>

<troubleshooting>
### Performance Issues
**Problem**: Action takes too long
- **Check**: {What to verify}
- **Solution**: {How to optimize}

### Unexpected Results
**Problem**: Output doesn't match expected
- **Check**: {What to verify}
- **Solution**: {How to fix}

### Intermittent Failures
**Problem**: Action sometimes fails
- **Check**: {What to verify}
- **Solution**: {How to handle}
</troubleshooting>

</action>

---

{Repeat the above <action> template for each action in the category}

---

## Read Operations

{Repeat action sections with appropriate modifications for Read operations}

---

## Update Operations

{Repeat action sections with appropriate modifications for Update operations}

---

## Delete Operations

{Repeat action sections with appropriate modifications for Delete operations}

---

## Search/Query Operations

{Repeat action sections with appropriate modifications for Search operations}

---

## Utility Operations

{Repeat action sections with appropriate modifications for Utility operations}

---

<action_index>
## Quick Reference Index

### Alphabetical
- [{Action A}](#action-id-a)
- [{Action B}](#action-id-b)
- [{Action C}](#action-id-c)

### By Complexity
**Low Complexity**:
- [{Action}](#action-id), [{Action}](#action-id)

**Medium Complexity**:
- [{Action}](#action-id), [{Action}](#action-id)

**High Complexity**:
- [{Action}](#action-id), [{Action}](#action-id)

### By Use Case
**{Use Case Category}**:
- [{Action}](#action-id) - {Brief note}
- [{Action}](#action-id) - {Brief note}

**{Another Use Case}**:
- [{Action}](#action-id) - {Brief note}
</action_index>

<related_docs>
- **Overview**: [overview.md](./overview.md) - Connector limitations and capabilities
- **Triggers**: [triggers.md](./triggers.md) - Available triggers for this connector
- **Official Docs**: {Microsoft Learn URL}
</related_docs>
