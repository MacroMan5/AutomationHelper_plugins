# {NODE_NAME} - Operations

<!--
INSTRUCTIONS FOR CLAUDE CODE:
1. Replace {PLACEHOLDERS} with actual values
2. Group operations by logical categories (CRUD, utility, etc.)
3. Assign unique IDs: op-get, op-create, op-update, etc.
4. Rate complexity: low, medium, high
5. Include concrete examples for each operation
6. Link related operations by ID
7. Remove this comment block when done
-->

---
type: node-operations
node_name: {NODE_NAME}
operation_count: {X}
version: 1.0
last_updated: {YYYY-MM-DD}
keywords: [{node-name}, {category1}, {category2}, {operation-type}]
categories: [create, read, update, delete, search, utility, transform]
---

<operation_summary>
**Total Operations**: {X}

**By Category**:
- Create Operations: {X} operations
- Read Operations: {Y} operations
- Update Operations: {Z} operations
- Delete Operations: {A} operations
- Search/Query Operations: {B} operations
- Transform Operations: {C} operations
- Utility Operations: {D} operations

**Complexity Distribution**:
- Low complexity: {X} operations
- Medium complexity: {Y} operations
- High complexity: {Z} operations
</operation_summary>

<operation_categories>
## Categories Overview

### Create Operations
{Brief description of create operations available}

### Read Operations
{Brief description of read operations available}

### Update Operations
{Brief description of update operations available}

### Delete Operations
{Brief description of delete operations available}

### Search/Query Operations
{Brief description of search operations available}

### Transform Operations
{Brief description of transform operations available}

### Utility Operations
{Brief description of utility operations available}
</operation_categories>

---

## Create Operations

### {Operation Name}

<operation id="op-{unique-id}" category="create" complexity="low|medium|high" throttle_impact="low|medium|high">

<operation_header>
**Operation Type**: Create
**Complexity**: {low|medium|high}
**Throttling Impact**: {low|medium|high}
**Auth Required**: {yes|no}
**API Endpoint**: {endpoint path if applicable}
**HTTP Method**: {POST|PUT|etc if applicable}
</operation_header>

<description>
{1-2 clear sentences describing what this operation does and when to use it}
</description>

<parameters>
#### Required Parameters

**{parameter_name}** (`{type}`)
- **Description**: {What this parameter does}
- **Format**: {Expected format, e.g., "ISO 8601 date", "JSON object"}
- **Validation**: {Constraints, e.g., "Max 255 characters", "Must be positive integer"}
- **N8N Field**: {Field name in N8N UI}
- **Expression Support**: {yes|no}
- **Example**: `{concrete_example_value}`

**{parameter_name}** (`{type}`)
- **Description**: {Description}
- **Format**: {Format}
- **N8N Field**: {Field name}
- **Example**: `{example}`

#### Optional Parameters

**{parameter_name}** (`{type}`)
- **Description**: {What this parameter does}
- **Default**: `{default_value}`
- **Valid Values**: {Range, enum values, or pattern}
- **Impact**: {How this affects behavior}
- **N8N Field**: {Field name in N8N UI}
- **Expression Support**: {yes|no}
- **Example**: `{example}`

**{parameter_name}** (`{type}`)
- **Description**: {Description}
- **Default**: `{default}`
- **N8N Field**: {Field name}
- **Example**: `{example}`

#### Advanced Options (N8N)
- **Batch Size**: {If applicable}
- **Timeout**: {Configurable timeout}
- **Retry Settings**: {Retry configuration}
- **Output Simplification**: {On/Off - affects output structure}
</parameters>

<returns>
**Return Type**: `{type}` (e.g., Object, Array, String, Boolean)

**Structure**:
```json
{
  "id": "unique-identifier-123",
  "name": "example-name",
  "created_at": "2024-10-31T12:00:00Z",
  "status": "success",
  "data": {
    "field1": "value1",
    "field2": 123
  }
}
```

**Key Fields**:
- **`id`** (`string`): {Description and when to use}
- **`name`** (`string`): {Description}
- **`created_at`** (`datetime`): {Description}
- **`status`** (`string`): {Description} - Values: {list valid values}
- **`data`** (`object`): {Description}

**N8N Output**:
- Available in subsequent nodes via expressions
- Access fields: `{{ $json.id }}`, `{{ $json.data.field1 }}`
- Array access: `{{ $json.items[0].field }}`
- Use in parameters: Drag from "Expressions" panel

**Output Modes** (if applicable):
- **Simplified**: Returns only essential fields
- **Full**: Returns complete API response
- **Raw**: Returns unprocessed response
</returns>

<limitations>
### Operation-Specific Limits
- **{Limitation 1}**: {Description and impact}
  - **Workaround**: {If available}
  - **N8N Handling**: {How N8N handles this}
- **{Limitation 2}**: {Description and impact}

### Behavioral Notes
- **{Note 1}**: {Important behavior to be aware of}
- **{Note 2}**: {Another consideration}
- **N8N Specifics**: {Any N8N-specific behavior}

### Dependencies
- **Requires**: {Other operations/setup needed first}
- **Conflicts with**: {What can't be done simultaneously}
- **Prerequisites**: {Required credentials/configuration}
</limitations>

<use_cases>
1. **{Use Case 1 Title}**
   - **Scenario**: {When you would use this}
   - **Why This Operation**: {Why it's the right choice}
   - **Typical Workflow**: {Trigger} → {Node} → This operation → {Next node}
   - **N8N Example**: {Brief workflow description}

2. **{Use Case 2 Title}**
   - **Scenario**: {When you would use this}
   - **Combined With**: [{related operation}](#op-related-id)
   - **N8N Pattern**: {Common N8N workflow pattern}

3. **{Use Case 3 Title}**
   - **Scenario**: {When you would use this}
   - **Alternative**: Consider [{other operation}](#op-alt-id) if {condition}
</use_cases>

<best_practices>
### Performance
1. **{Practice}**: {Explanation}
   - **Impact**: {Performance benefit}
   - **N8N Implementation**: {How to configure in N8N}
   - **Example**: {Concrete example}

2. **{Practice}**: {Explanation}

### Reliability
1. **{Practice}**: {Explanation}
   - **Why**: {Reason}
   - **N8N Feature**: {Which N8N feature supports this}
   - **Configuration**: {How to set up}

2. **{Practice}**: {Explanation}

### Data Handling
1. **Validate Input**: Use N8N "IF" node before this operation
   - **Why**: Prevent errors from invalid data
   - **How**: Add condition to check required fields

2. **Transform Data**: Use "Set" node to prepare data
   - **Why**: Ensure correct format
   - **How**: Map fields to expected structure

### Error Handling
1. **Enable Retry**: Configure in node settings
   - **Recommended**: 3 retries with exponential backoff
   - **Retry On**: [429, 500, 502, 503, 504]

2. **Add Error Workflow**: Handle failures gracefully
   - **Why**: Prevent workflow stoppage
   - **How**: Create error workflow in N8N settings
</best_practices>

<example>
### Example 1: {Scenario Name}

**Objective**: {What you're trying to accomplish}

**N8N Workflow**:
```
1. [Webhook] Receive data
2. [Set] Transform data
3. [THIS NODE - {Operation}] Execute operation
4. [IF] Check result
5. [Send Email] Notify on success
```

**Node Configuration**:
```json
{
  "operation": "{operation_id}",
  "parameters": {
    "param1": "concrete-value-1",
    "param2": "{{ $json.field_from_previous_node }}",
    "param3": {
      "nested": "value"
    }
  },
  "options": {
    "timeout": 30000,
    "retry": {
      "enabled": true,
      "maxRetries": 3
    }
  }
}
```

**N8N Expression Examples**:
```javascript
// Access previous node data
{{ $json.user_id }}

// Format date
{{ $now.toISO() }}

// Conditional value
{{ $json.status === 'active' ? 'yes' : 'no' }}

// Array mapping
{{ $json.items.map(item => item.name) }}
```

**Expected Result**:
```json
{
  "id": "generated-id-123",
  "status": "success",
  "message": "Operation completed"
}
```

**What Happens**: {Step-by-step description}

---

### Example 2: {Another Scenario}

**Objective**: {What you're trying to accomplish}

**N8N Workflow**:
```
1. [Schedule Trigger] Run daily at 9 AM
2. [THIS NODE - {Operation}] Get data
3. [Split In Batches] Process in chunks
4. [Loop Over Items] Process each item
5. [Google Sheets] Write to spreadsheet
```

**Node Configuration**:
```json
{
  "operation": "{operation_id}",
  "parameters": {
    "param1": "{{ $('Schedule Trigger').item.json.date }}",
    "param2": "batch-process"
  }
}
```

**Use Case**: {When this pattern is useful}

**N8N Tips**:
- {Tip 1}
- {Tip 2}

</example>

<common_errors>
### Error: {Error Message or Code}

<error ref="err-op-001">
- **Full Message**: "{Complete error message text}"
- **Cause**: {Why this error occurs}
- **N8N Context**: {When this happens in N8N workflows}
- **Fix**:
  1. {Step 1 to resolve}
  2. {Step 2 to resolve}
  3. {Step 3 to resolve}
- **Prevention**: {How to avoid in future}
- **N8N Debugging**:
  - Check execution log
  - Verify input data format
  - Test with sample data
- **Related**: See [limitation lim-XXX](./overview.md#lim-XXX)
</error>

### Error: {Another Error}

<error ref="err-op-002">
{Same structure as above}
</error>

### Validation Errors
- **"{Error}"**: {Cause and fix}
  - **N8N Tip**: {How to prevent in N8N}
- **"{Error}"**: {Cause and fix}
  - **N8N Tip**: {How to prevent in N8N}
</common_errors>

<related_operations>
### Commonly Used Together
- **[{Operation Name}](#op-id)**: {Why often used together}
  - **N8N Pattern**: {How typically combined in workflows}
- **[{Operation Name}](#op-id)**: {Why often used together}

### Alternatives
- **[{Operation Name}](#op-id)**: {When to use instead}
  - Use when: {Condition}
  - Difference: {Key distinction}
  - **N8N Consideration**: {Which to choose in N8N}

### Sequential Operations
Typical N8N workflow sequence:
1. [{Prerequisite Operation}](#op-id) - {Purpose}
2. **This Operation** - {Purpose}
3. [{Follow-up Operation}](#op-id) - {Purpose}

### N8N Helper Nodes
Common nodes used before/after this operation:
- **Set**: Transform data to correct format
- **IF**: Validate before execution
- **Split In Batches**: Handle large datasets
- **Error Trigger**: Catch and handle errors

### See Also
- Overview: [Limitations](./overview.md#critical_limitations)
- Related Nodes: [{Node Name}](../Category/node.md)
</related_operations>

<troubleshooting>
### Performance Issues
**Problem**: Operation takes too long
- **Check**:
  - Input data size
  - Network latency
  - Service response time
- **Solution**:
  - Enable caching
  - Use pagination
  - Increase timeout
- **N8N Tools**:
  - Check execution time in logs
  - Use "Stop on Error" for debugging

### Unexpected Results
**Problem**: Output doesn't match expected
- **Check**:
  - Input data format
  - Parameter values
  - Expression syntax
- **Solution**:
  - Validate input with IF node
  - Use Set node to transform
  - Check N8N expression builder
- **N8N Debugging**:
  - Use "Execute Node" to test
  - Inspect input/output data
  - Check expression evaluation

### Intermittent Failures
**Problem**: Operation sometimes fails
- **Check**:
  - Rate limiting
  - Service availability
  - Network issues
- **Solution**:
  - Enable retry
  - Add error handling
  - Implement queue
- **N8N Features**:
  - Automatic retry
  - Error workflow
  - Execution recovery
</troubleshooting>

</operation>

---

{Repeat the above <operation> template for each operation}

---

## Read Operations

{Repeat operation sections with appropriate modifications for Read operations}

---

## Update Operations

{Repeat operation sections with appropriate modifications for Update operations}

---

## Delete Operations

{Repeat operation sections with appropriate modifications for Delete operations}

---

## Search/Query Operations

{Repeat operation sections with appropriate modifications for Search operations}

---

## Transform Operations

{Repeat operation sections with appropriate modifications for Transform operations}

---

## Utility Operations

{Repeat operation sections with appropriate modifications for Utility operations}

---

<operation_index>
## Quick Reference Index

### Alphabetical
- [{Operation A}](#op-id-a)
- [{Operation B}](#op-id-b)
- [{Operation C}](#op-id-c)

### By Complexity
**Low Complexity**:
- [{Operation}](#op-id) - {Brief description}
- [{Operation}](#op-id) - {Brief description}

**Medium Complexity**:
- [{Operation}](#op-id) - {Brief description}

**High Complexity**:
- [{Operation}](#op-id) - {Brief description}

### By Use Case
**{Use Case Category}**:
- [{Operation}](#op-id) - {When to use}
- [{Operation}](#op-id) - {When to use}

**{Another Use Case}**:
- [{Operation}](#op-id) - {When to use}

### N8N Workflow Patterns
**Data Fetching**:
- [{Operation}](#op-id) → Set → IF

**Data Creation**:
- Webhook → Set → [{Operation}](#op-id)

**Batch Processing**:
- Schedule → [{Operation}](#op-id) → Split In Batches → Loop
</operation_index>

<related_docs>
- **Overview**: [overview.md](./overview.md) - Node limitations and capabilities
- **N8N Documentation**: {Official N8N docs URL}
- **Service API Docs**: {Service API documentation URL}
</related_docs>
