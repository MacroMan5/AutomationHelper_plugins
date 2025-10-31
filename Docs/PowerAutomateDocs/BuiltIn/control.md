# Control Connector

## Overview
**Triggers**: 0
**Actions**: 6

The Control connector provides logical branching and flow organization capabilities.

## Actions

### Condition
**Description**: Evaluates a condition and branches execution
**Parameters**:
- Value to test (left side)
- Operator (equals, not equals, greater than, less than, etc.)
- Compare value (right side)

**Structure**:
```
If condition is true:
  → Yes branch actions
Else:
  → No branch actions
```

**Use Cases**:
- Value comparison
- Status checking
- Decision points

**Best Practices**:
- Use "and" / "or" for compound conditions
- Nest sparingly for readability
- Consider Switch for multiple paths

---

### Apply to each
**Description**: Iterates over array items
**Parameters**:
- Array to iterate (required)
- Actions to perform (inside loop)

**Critical Notes**:
- Runs sequentially by default
- Enable "Concurrency Control" for parallel processing
- Max 50 concurrent iterations
- May cause throttling with high volume

**Use Cases**:
- Processing array items
- Batch operations
- Data transformation loops

**Best Practices**:
- Limit array size or use pagination
- Add error handling inside loop
- Use concurrency for independent operations
- Avoid nested loops when possible

---

### Do until
**Description**: Repeats actions until condition is met
**Parameters**:
- Condition to evaluate
- Actions to repeat
- Timeout (default: PT1H - 1 hour)
- Count limit (default: 60)

**Warning**: Can cause infinite loops if condition never met

**Use Cases**:
- Polling for status changes
- Retry logic
- Waiting for async operations

**Best Practices**:
- Always set timeout and count limits
- Include delay in loop to avoid throttling
- Use increment variable to track iterations
- Have exit condition guaranteed to occur

---

### Scope
**Description**: Groups actions for organization and error handling
**Parameters**:
- Actions to group (inside scope)

**Benefits**:
- Logical organization
- Collective error handling
- Configure run after based on scope status
- Collapsible in designer

**Scope Status**:
- Succeeded: All actions successful
- Failed: Any action failed
- Cancelled: User cancelled
- Skipped: Condition not met
- TimedOut: Exceeded timeout

**Use Cases**:
- Try-catch patterns
- Logical grouping
- Transaction-like behavior
- Error isolation

**Best Practices**:
- Name scopes descriptively
- Use for error handling
- Follow with "Configure run after"
- Keep scope focused on related actions

---

### Switch
**Description**: Multi-way branching based on value
**Parameters**:
- Expression to evaluate
- Cases (multiple)
- Default case (optional)

**Structure**:
```
Switch on: status
  Case "Approved": → Approval actions
  Case "Rejected": → Rejection actions
  Case "Pending": → Pending actions
  Default: → Fallback actions
```

**Use Cases**:
- Multiple status values
- Category-based routing
- Type-based processing

**Best Practices**:
- Include default case
- Keep case actions focused
- Consider condition for 2 paths only
- Use with enumerations/status values

---

### Terminate
**Description**: Stops flow execution immediately
**Parameters**:
- Status (required): Succeeded, Cancelled, Failed

**Effects**:
- Stops all execution
- Sets flow run status
- No further actions run
- Triggers cannot be undone

**Use Cases**:
- Early exit on validation failure
- Stop on critical errors
- End on success condition
- Cancel on timeout

**Best Practices**:
- Provide clear failure messages
- Use appropriate status
- Document why termination occurs
- Avoid terminate in try-catch unless intentional

---

## Control Flow Patterns

### Try-Catch Pattern
```
Scope (Try)
  → Main actions
Scope (Catch) - Configure run after "Try" fails
  → Error handling actions
```

### Retry Pattern
```
Do until (Success OR MaxRetries)
  → Action to retry
  → Condition check
  → Increment retry counter
  → Delay between retries
```

### Parallel Processing
```
Apply to each (with concurrency enabled)
  → Independent operations
```

### Conditional Execution
```
Condition
  → If Yes: Primary path
  → If No: Alternative path
```

## Best Practices

### Performance
1. Enable concurrency in Apply to each when operations are independent
2. Use Switch instead of nested Conditions
3. Minimize actions inside loops
4. Set appropriate timeouts on Do until

### Reliability
1. Always include timeout on Do until
2. Add error handling with Scope
3. Use Terminate with descriptive messages
4. Implement retry logic for transient failures

### Maintainability
1. Name all control actions descriptively
2. Use Scope to organize related actions
3. Comment complex conditions
4. Keep nesting depth minimal

### Error Handling
1. Wrap risky operations in Scope
2. Configure run after for error paths
3. Log errors before Terminate
4. Provide actionable error messages
