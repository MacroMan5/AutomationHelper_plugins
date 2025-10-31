# {CONNECTOR_NAME} - Triggers

<!--
INSTRUCTIONS FOR CLAUDE CODE:
1. Replace {PLACEHOLDERS} with actual values
2. Classify triggers by type: polling, webhook, scheduled
3. Assign unique IDs: trigger-001, trigger-002, etc.
4. Document frequency and latency characteristics
5. Include filtering and performance guidance
6. Remove this comment block when done
-->

---
type: connector-triggers
connector_name: {CONNECTOR_NAME}
trigger_count: {X}
version: 1.0
last_updated: {YYYY-MM-DD}
keywords: [{connector}, {event-type}, {automation}]
trigger_types: [polling, webhook, scheduled, instant]
---

<trigger_summary>
**Total Triggers**: {X}

**By Type**:
- Polling Triggers: {X} triggers
- Webhook Triggers: {Y} triggers
- Scheduled Triggers: {Z} triggers
- Instant Triggers: {A} triggers

**Performance Characteristics**:
- Real-time (< 1 min): {X} triggers
- Near real-time (1-5 min): {Y} triggers
- Delayed (5+ min): {Z} triggers
</trigger_summary>

<trigger_types>
## Trigger Types Overview

### Polling Triggers
{Brief description - these check for changes on a schedule}
- Typical latency: {X} minutes
- Recommended for: {Use cases}

### Webhook Triggers
{Brief description - these respond to events in real-time}
- Typical latency: {X} seconds
- Recommended for: {Use cases}

### Scheduled Triggers
{Brief description - these run on a time-based schedule}
- Typical latency: N/A (user-defined)
- Recommended for: {Use cases}

### Instant Triggers
{Brief description - these run manually or via API}
- Typical latency: Immediate
- Recommended for: {Use cases}
</trigger_types>

---

## Polling Triggers

### {Trigger Name}

<trigger id="trigger-{unique-id}" type="polling" frequency="high|medium|low" latency_minutes="{X}">

<trigger_header>
**Type**: Polling
**Polling Interval**: {X} minutes (default)
**Latency**: {Y} minutes typical
**API Impact**: {low|medium|high} ({X} calls per hour)
**Premium**: {yes|no}
</trigger_header>

<description>
{1-2 sentences describing when this trigger fires and what events it detects}
</description>

<parameters>
#### Required Parameters

**{parameter_name}** (`{type}`)
- **Description**: {What this parameter does}
- **Format**: {Expected format}
- **Selection**: {How user selects - dropdown, manual entry, etc.}
- **Example**: `{concrete_example}`

**{parameter_name}** (`{type}`)
- **Description**: {Description}
- **Example**: `{example}`

#### Optional Parameters

**{parameter_name}** (`{type}`)
- **Description**: {What this parameter does}
- **Default**: `{default_value}`
- **Impact**: {How this affects trigger behavior}
- **Recommendation**: {When to use/not use}
- **Example**: `{example}`

#### Filtering Parameters

**{filter_parameter}** (`{type}`)
- **Description**: {What can be filtered}
- **Filter Type**: {Server-side|Client-side}
- **Performance Impact**: {How it affects API calls}
- **Syntax**: {Filter syntax if applicable}
- **Example**: `{example filter expression}`
</parameters>

<behavior>
## Polling Mechanism

**How It Works**:
1. {Step 1 of polling process}
2. {Step 2 of polling process}
3. {Step 3 of polling process}

**Polling Frequency**:
- Minimum: {X} minutes
- Maximum: {Y} minutes
- Default: {Z} minutes
- Adjustable: {yes|no}

**Batch Behavior**:
- Items per trigger execution: {X} (default: {Y})
- Batch processing: {yes|no}
- Order: {chronological|reverse chronological|random}

**Deduplication**:
- Method: {How duplicates are prevented}
- Reliability: {High|Medium|Low}
- Edge cases: {Known scenarios where duplicates may occur}

**State Management**:
- Tracks: {What is tracked between runs}
- Reset behavior: {What happens if flow is disabled/re-enabled}
- Historical data: {Does it process old items? How far back?}
</behavior>

<outputs>
**Trigger Output Structure**:
```json
{
  "id": "unique-item-id",
  "created": "2024-10-31T12:00:00Z",
  "modified": "2024-10-31T12:30:00Z",
  "property1": "value1",
  "property2": {
    "nested": "value2"
  },
  "array_property": [
    {"item": 1},
    {"item": 2}
  ]
}
```

**Dynamic Content Available**:

**Core Fields**:
- **`id`**: {Description and typical use}
- **`created`**: {Description and typical use}
- **`modified`**: {Description and typical use}

**Business Fields**:
- **`property1`**: {Description and typical use}
- **`property2`**: {Description and typical use}
- **`property2/nested`**: {How to access nested properties}

**Collection Fields**:
- **`array_property`**: {Description}
  - Access with: `Apply to each` action
  - Item structure: {Description of array items}

**Metadata Fields**:
- **`@odata.etag`**: {Description if OData}
- **`_metadata`**: {Description of metadata}

## Expression Examples

**Access trigger output**:
```
@triggerOutputs()?['body/property1']
```

**Access nested property**:
```
@triggerBody()?['property2/nested']
```

**Check for null/empty**:
```
@empty(triggerOutputs()?['body/property1'])
```
</outputs>

<limitations>
### Polling Limitations
- **Delay**: {X}-{Y} minute delay between event and trigger
- **Missed Events**: {Scenarios where events might be missed}
- **Historical Limit**: {How far back it can detect changes}

### Item Limitations
- **Size**: Items over {X}MB are {skipped|truncated|fail}
- **Type**: {Unsupported item types}
- **Count**: Max {X} items per execution

### Filtering Limitations
- **Server-Side**: {What can be filtered at source}
- **Client-Side**: {What requires Condition action}
- **Performance**: {Filtering impact on API calls}

### State Limitations
- **Reset Behavior**: {What happens when flow restarted}
- **Backfill**: {Does it process old items? Limitations?}
- **Concurrent Flows**: {Behavior with multiple flows using same trigger}
</limitations>

<filtering>
## Filtering Strategies

### Server-Side Filtering (Recommended)
**Where**: In trigger configuration
**Benefits**:
- Reduces API calls
- Improves performance
- Lowers throttling risk

**Available Filters**:
1. **{Filter Type 1}**: {Description}
   - Syntax: `{example}`
   - Use case: {When to use}

2. **{Filter Type 2}**: {Description}
   - Syntax: `{example}`
   - Use case: {When to use}

### Client-Side Filtering
**Where**: Using Condition action after trigger
**When to Use**:
- Complex logic not supported by server-side filters
- Multiple conditions with OR logic
- Dynamic filter criteria

**Pattern**:
```
Trigger → Condition → (Yes branch) → Continue flow
                   ↘ (No branch) → Terminate
```

### Hybrid Approach
**Best Practice**: Combine both
1. Server-side: Filter {X} (broad filter)
2. Client-side: Filter {Y} (fine-grained logic)

**Example**:
- Server: `created > yesterday`
- Client: `status = 'pending' AND priority = 'high'`
</filtering>

<use_cases>
1. **{Use Case 1 Title}**
   - **Scenario**: {When you would use this trigger}
   - **Why This Trigger**: {Why it's appropriate}
   - **Typical Flow**:
     ```
     This Trigger → {Action 1} → {Action 2} → {Action 3}
     ```
   - **Considerations**: {Important notes}

2. **{Use Case 2 Title}**
   - **Scenario**: {Scenario description}
   - **Alternative**: Consider [{Other Trigger}](#trigger-id) if {condition}
   - **Pattern**: {Workflow pattern}

3. **{Use Case 3 Title}**
   - **Scenario**: {Scenario description}
   - **Combined With**: [{Action}](./actions.md#action-id)
   - **Best For**: {Optimal use case}
</use_cases>

<best_practices>
### Performance Optimization

1. **Minimize API Calls**
   - Use server-side filtering maximally
   - Adjust polling frequency to actual need
   - Consider trigger conditions carefully

2. **Batch Processing**
   - Enable {feature} for bulk operations
   - Use {action} for efficient processing
   - Implement pagination for large result sets

3. **Caching Strategy**
   - Cache {what} to avoid redundant calls
   - Use variables for repeated values
   - Implement conditional logic to skip unnecessary actions

### Reliability

1. **Handle Missing Data**
   - Always check for null/empty values
   - Use default values or terminate gracefully
   - Log unexpected data patterns

2. **Idempotency**
   - Design actions to be repeatable
   - Use unique identifiers
   - Implement duplicate detection

3. **Error Recovery**
   - Add error scopes around critical actions
   - Implement retry logic with backoff
   - Log failures for debugging

### Monitoring

1. **Track Metrics**
   - Monitor trigger execution frequency
   - Track API consumption
   - Alert on failure rates

2. **Debugging**
   - Enable flow run history
   - Log key decision points
   - Save problematic inputs for analysis

3. **Optimization**
   - Review trigger frequency vs. actual needs
   - Analyze performance bottlenecks
   - Refine filters based on actual data patterns
</best_practices>

<example>
### Example 1: {Scenario Name}

**Objective**: {What you're trying to accomplish}

**Trigger Configuration**:
```json
{
  "trigger": "{trigger_technical_name}",
  "parameters": {
    "param1": "concrete-value",
    "param2": "filtering-expression",
    "frequency": "minute",
    "interval": 5
  }
}
```

**Polling Behavior**:
- Checks every {X} minutes
- Returns up to {Y} new items per execution
- Filters to {description of filter}

**Expected Output**:
```json
{
  "id": "item-123",
  "name": "Example Item",
  "status": "new",
  "created": "2024-10-31T12:00:00Z"
}
```

**Subsequent Actions**:
```
Trigger → Condition (check status = 'new')
         ↘ Yes → Update item action
         ↘ No → Terminate
```

**Flow Frequency**: Expect {X} executions per hour under normal load

---

### Example 2: {Advanced Scenario}

**Objective**: {Complex use case}

**Configuration**:
```json
{
  "trigger": "{trigger_technical_name}",
  "parameters": {
    "param1": "@{parameters('dynamic_value')}",
    "filter": "status eq 'pending' and priority eq 'high'"
  }
}
```

**Dynamic Content Usage**:
```
Access item ID: @triggerOutputs()?['body/id']
Access nested field: @triggerBody()?['metadata/category']
Loop through array: Apply to each on @triggerBody()?['items']
```

**Advanced Pattern**: {Description of pattern}

</example>

<performance_impact>
## API Consumption

**Per Execution**:
- Base call: {X} API call(s)
- Per item returned: {Y} additional call(s)
- Average total: ~{Z} calls per execution

**Per Hour** (with default settings):
- Polling frequency: Every {X} minutes
- Executions per hour: {Y}
- API calls per hour: ~{Z}

**Optimization Impact**:
- With optimal filtering: Reduce by {X}%
- With increased interval: {calculation}
- With webhook alternative: Reduce by {Y}% (if available)

## Resource Usage

**Memory**: {low|medium|high}
- Per item: ~{X}KB
- Per execution: ~{Y}MB

**Processing Time**: {low|medium|high}
- Average: {X} seconds per execution
- Large batches: Up to {Y} seconds

**Concurrency**:
- Max concurrent runs: {X}
- Queuing behavior: {description}

## Scaling Considerations

**Low Volume** (< {X} items/day):
- Recommendation: {specific settings}
- Expected cost: {low|medium|high}

**Medium Volume** ({X}-{Y} items/day):
- Recommendation: {specific settings}
- Consider: {optimizations}

**High Volume** (> {Y} items/day):
- Recommendation: {specific settings}
- Required: {necessary optimizations}
- Alternative: Consider [{webhook trigger}](#trigger-webhook-id) if available
</performance_impact>

<common_errors>
### Error: Trigger Not Firing

<error ref="err-trigger-001">
- **Symptoms**: Flow never executes, even when data changes
- **Possible Causes**:
  1. {Cause 1}
  2. {Cause 2}
  3. {Cause 3}
- **Diagnostic Steps**:
  1. {Check X}
  2. {Verify Y}
  3. {Test Z}
- **Solutions**:
  1. {Solution 1}
  2. {Solution 2}
- **Prevention**: {How to avoid}
</error>

### Error: Duplicate Triggers

<error ref="err-trigger-002">
- **Symptoms**: Same item triggers flow multiple times
- **Causes**: {Why this happens}
- **Fix**: {How to resolve}
- **Pattern**: {Deduplication pattern to implement}
</error>

### Error: Missing Items

<error ref="err-trigger-003">
- **Symptoms**: Known changes don't trigger flow
- **Causes**: {Common reasons}
- **Fix**: {Resolution steps}
- **Limitation**: See [limitation](#lim-XXX)
</error>

### Throttling Errors

<error ref="err-trigger-429">
- **Symptoms**: "Too many requests" in trigger history
- **Causes**: {Why throttling occurs}
- **Immediate Fix**: {Quick solution}
- **Long-term Solution**: {Sustainable approach}
- **Reference**: [API Limits](./overview.md#api_limits)
</error>
</common_errors>

<related_triggers>
### Alternative Triggers

**[{Trigger Name}](#trigger-alt-id)**
- **Use Instead When**: {Condition}
- **Key Difference**: {Main distinction}
- **Trade-offs**: {Pros and cons}

**[{Another Trigger}](#trigger-alt-id-2)**
- **Use Instead When**: {Condition}
- **Comparison**: {How they differ}

### Complementary Triggers

**[{Trigger Name}](#trigger-comp-id)**
- **Use Together For**: {Combined use case}
- **Pattern**: {How they work together}

### Related Actions

Often used with these actions:
- **[{Action}](./actions.md#action-id)**: {Why commonly paired}
- **[{Action}](./actions.md#action-id)**: {Why commonly paired}

### See Also
- Overview: [Common Use Cases](./overview.md#common_use_cases)
- Related Connector: [{Connector}](../Connector/triggers.md)
</related_triggers>

<troubleshooting>
### Trigger Performance Issues

**Problem**: Trigger is slow or delayed
1. **Check**: {What to verify}
2. **Optimize**: {How to improve}
3. **Consider**: {Alternative approaches}

### Unexpected Behavior

**Problem**: Trigger fires at wrong times
1. **Verify**: {Configuration to check}
2. **Review**: {Settings to examine}
3. **Test**: {How to validate}

### Data Quality Issues

**Problem**: Output data is incomplete or incorrect
1. **Investigate**: {Where to look}
2. **Validate**: {How to check}
3. **Resolve**: {Steps to fix}
</troubleshooting>

</trigger>

---

{Repeat the above <trigger> template for each trigger in the polling category}

---

## Webhook Triggers

{Repeat trigger sections with appropriate modifications for Webhook triggers}

---

## Scheduled Triggers

{Repeat trigger sections with appropriate modifications for Scheduled triggers}

---

## Instant Triggers

{Repeat trigger sections with appropriate modifications for Instant/Manual triggers}

---

<trigger_index>
## Quick Reference Index

### By Type
**Polling Triggers**:
- [{Trigger}](#trigger-id) - {One-line description}
- [{Trigger}](#trigger-id) - {One-line description}

**Webhook Triggers**:
- [{Trigger}](#trigger-id) - {One-line description}

**Scheduled Triggers**:
- [{Trigger}](#trigger-id) - {One-line description}

**Instant Triggers**:
- [{Trigger}](#trigger-id) - {One-line description}

### By Latency
**Real-time (< 1 min)**:
- [{Trigger}](#trigger-id)

**Near real-time (1-5 min)**:
- [{Trigger}](#trigger-id)

**Delayed (5+ min)**:
- [{Trigger}](#trigger-id)

### By Use Case
**{Use Case Category}**:
- [{Trigger}](#trigger-id) - {When to use}
- [{Trigger}](#trigger-id) - {When to use}

**{Another Use Case}**:
- [{Trigger}](#trigger-id) - {When to use}
</trigger_index>

<trigger_comparison>
## Trigger Selection Guide

### Choose polling trigger when:
- {Condition 1}
- {Condition 2}
- {Condition 3}

### Choose webhook trigger when:
- {Condition 1}
- {Condition 2}
- {Condition 3}

### Choose scheduled trigger when:
- {Condition 1}
- {Condition 2}
- {Condition 3}

### Choose instant trigger when:
- {Condition 1}
- {Condition 2}
- {Condition 3}
</trigger_comparison>

<related_docs>
- **Overview**: [overview.md](./overview.md) - Connector capabilities and limitations
- **Actions**: [actions.md](./actions.md) - Available actions for this connector
- **Official Docs**: {Microsoft Learn URL}
</related_docs>
