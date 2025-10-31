---
type: node-overview
node_name: IF
node_type: core
category: action
auth_required: false
version: 1.0
last_updated: 2025-10-31
keywords: [if, conditional, branching, logic, comparison, filter, decision, true, false, and, or]
related_nodes: [Switch, Filter, Merge, Error Trigger]
rate_limits:
  service_rate_limit: none (N8N built-in node, no service rate limits)
  n8n_limit: none (N8N doesn't impose limits)
official_docs_url: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.if/
---

<official_docs>
- **Node Documentation**: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.if/
- **Flow Logic**: https://docs.n8n.io/flow-logic/splitting/
- **Error Handling**: https://docs.n8n.io/flow-logic/error-handling/
</official_docs>

<description>
The IF node is a fundamental conditional logic node that splits workflow execution into two paths based on comparison conditions: a "true" path when conditions are met and a "false" path when they are not. It evaluates one or more conditions using logical operators (AND/OR) and routes data accordingly, making it essential for filtering data, branching logic, error handling, and decision-based workflows. Perfect for building intelligent automation that responds differently based on data values.
</description>

<capabilities>
## Core Capabilities
- Evaluate single or multiple conditions with AND/OR logic
- Support for multiple data types: String, Number, Boolean, Date & Time, Array, Object
- Flexible comparison operators for each data type
- Route data to true or false branches based on conditions
- Combine multiple conditions with logical operators
- No authentication required (built-in N8N node)
- Real-time condition evaluation
- Expression-based value comparisons
- Type-aware comparisons

## Supported Operations
- **Compare String**: Check for equality, contains/does not contain, pattern matching
- **Compare Number**: Check for equality, greater/less than, range validation
- **Compare Boolean**: Check true/false values
- **Compare Date & Time**: Check temporal relationships (before/after, equality)
- **Compare Array**: Check array properties (exists, is empty, contains)
- **Compare Object**: Check object properties and existence
- **Combine Conditions**: Multiple conditions with AND (all must be true) or OR (any can be true)
- **Route Execution**: Direct output to true or false branch based on evaluation

## Integration Features
- Works with any data from previous nodes
- Branches data flow without modifying it
- Lightweight, zero latency operation
- Mergeable output branches for data consolidation
- Compatible with Error Trigger for error handling
- Chainable with other control flow nodes
- No external dependencies or API calls
</capabilities>

<rate_limits>
## Rate Limits

**N8N Built-In Node**
- No service rate limiting (local evaluation only)
- No API calls required
- Instant evaluation (<1ms per condition)
- No throttling or quotas

**Execution Limits**
- Max conditions per IF node: No hard limit (tested up to 100+)
- Max condition complexity: Limited by N8N expression parser
- Evaluation latency: <1ms per condition
- No concurrent execution limits

**N8N Platform Limits**
- No built-in rate limiting by N8N platform
- Self-hosted: Limited only by server CPU
- Cloud: No specific IF node limits
- Memory per execution: Minimal (<1KB per condition)

**Performance Characteristics**
- Throughput: Unlimited executions per second
- Latency: <1ms per condition evaluation
- No retry mechanism needed (deterministic)
- Synchronous execution with no delays

## Data Handling

**Input Data**
- Max items per execution: Unlimited (N8N default: 1000, configurable)
- Max item size: Depends on available memory
- Data types: Any N8N-supported type

**Output Data**
- True branch: Full input data (unmodified)
- False branch: Full input data (unmodified)
- Branching: Non-blocking (data continues on selected path)
</rate_limits>

<critical_limitations>
## Conditional Logic Limitations

<limitation id="lim-001" severity="high">
**Binary Output Only**
- **Issue**: IF node produces exactly 2 outputs (true/false), not suitable for multi-way branching
- **Impact**: Complex multi-condition routing requires nested IF nodes or Switch node
- **Scope**: Workflows needing 3+ distinct paths
- **Workaround**:
  1. Use Switch node for 3+ conditions
  2. Chain multiple IF nodes for complex logic
  3. Implement nested IF nodes for conditional paths
  4. Example: IF → IF (on true branch) → multiple paths
- **Affected Operations**: Multi-way branching, complex decision trees
- **Best Practice**: Use IF for binary logic, Switch for 3+ outcomes

**Example Scenario**:
You need to route data to 3 different services based on priority level (low, medium, high). Use Switch node instead of multiple IF nodes.
</limitation>

<limitation id="lim-002" severity="high">
**Type Coercion and Comparison Issues**
- **Issue**: Comparing different data types (string "100" vs number 100) produces inconsistent results
- **Impact**: Silent failures, unexpected branching based on type mismatch
- **Scope**: Mixed data types, JSON conversions, API responses
- **Workaround**:
  1. Explicitly convert types before comparison (Set node)
  2. Use Code node for complex type handling
  3. Validate data types in preceding nodes
  4. Test with actual data before deployment
  5. Use type-specific comparison operations
- **Affected Operations**: String-to-number comparisons, JSON parsing, API data
- **N8N Handling**: Use Set node to normalize types: `{{ parseInt($json.value) }}`

**Example Scenario**:
API returns count as string "100", comparing with number 100 in IF node may fail. Use Set node to convert: `{{ Number($json.count) }}`
</limitation>

<limitation id="lim-003" severity="high">
**Condition Evaluation Order Matters**
- **Issue**: With AND logic, first false condition stops evaluation (short-circuit); order affects performance
- **Impact**: Expensive conditions always evaluated even if earlier condition fails
- **Scope**: Multiple AND conditions with performance implications
- **Workaround**:
  1. Order conditions from cheapest to most expensive
  2. Put most likely-to-fail conditions first
  3. Use multiple IF nodes for independent conditions
  4. Use Code node for complex boolean logic
- **Affected Operations**: Multiple condition evaluation, API calls in expressions
- **Best Practice**: Put simple conditions first, API calls/expressions last

**Example Scenario**:
```
Bad: Check expensive API call AND simple field check
Good: Check simple field first AND expensive API call
```
</limitation>

<limitation id="lim-004" severity="high">
**No Data Filtering**
- **Issue**: IF node doesn't filter items, it routes entire data stream unchanged
- **Impact**: Both branches receive same data, need additional Filter nodes to remove items
- **Scope**: Filtering operations, item-level conditions
- **Workaround**:
  1. Use Filter node instead (specifically for item filtering)
  2. Chain IF with Filter nodes
  3. Use Loop Over Items + IF for per-item filtering
  4. Use Code node for complex filtering logic
- **Affected Operations**: Removing items, conditional data extraction
- **N8N Handling**: Use Filter node for filtering, IF for branching logic

**Example Scenario**:
IF node can't remove items from an array. Use Filter node or Loop → IF → Collect pattern.
</limitation>

<limitation id="lim-005" severity="high">
**Empty String and Zero Falsy Values**
- **Issue**: Empty strings ("") and zero (0) are not automatically falsy in comparison context
- **Impact**: Unexpected false negatives, requires explicit checking
- **Scope**: Null/empty/zero value handling
- **Workaround**:
  1. Use "is empty" operator explicitly: `is empty`
  2. Check for specific values: `is equal to ""`
  3. Use exists operator: `does not exist`
  4. Combine conditions: Check for empty AND check for null
  5. Validate in preceding Set node
- **Affected Operations**: Empty field detection, zero value handling
- **Best Practice**: Always explicitly check empty/null, don't assume falsy

**Example Scenario**:
```
Bad: IF price > 0 (doesn't catch empty string)
Good: IF price exists AND price > 0
```
</limitation>

<limitation id="lim-006" severity="medium">
**Merge Node Legacy Behavior**
- **Issue**: In N8N v0, Merge node after IF node could trigger both true and false branches
- **Impact**: Duplicate data processing, data inconsistency (only in v0)
- **Scope**: Legacy N8N v0 workflows
- **Workaround**:
  1. Upgrade to N8N v1.0+ (behavior fixed)
  2. For v0: Don't use Merge directly after IF; add intermediate nodes
  3. Test merge behavior in your version
- **Affected Operations**: IF → Merge patterns
- **Status**: RESOLVED in N8N v1.0+

**Note**: Modern N8N versions (v1.0+) have fixed this issue. Only affects legacy workflows.
</limitation>

<limitation id="lim-007" severity="medium">
**Complex Expression Evaluation**
- **Issue**: Complex JavaScript expressions in comparisons may have unexpected behavior
- **Impact**: Logic errors, condition not evaluated as expected
- **Scope**: Complex expressions, nested properties, function calls
- **Workaround**:
  1. Test expressions in Set node first (has expression preview)
  2. Break complex logic into multiple conditions
  3. Use Code node for complex logic before IF
  4. Add debug logging with Set node
  5. Simplify conditions for readability
- **Affected Operations**: Complex comparisons, nested object access
- **Best Practice**: Keep expressions simple, test thoroughly

**Example Scenario**:
```
Bad: IF $json.user.profile.address.zip contains "10"
Good: Set intermediate variable, then IF variable contains "10"
```
</limitation>

<limitation id="lim-008" severity="medium">
**No Null Handling by Default**
- **Issue**: Comparing with null/undefined requires explicit "does not exist" check
- **Impact**: Logic errors when field is missing
- **Scope**: Optional fields, API responses with variable structures
- **Workaround**:
  1. Use "does not exist" operator: `field does not exist`
  2. Provide defaults in Set node: `{{ $json.field ?? 'default' }}`
  3. Check for empty: `is empty`
  4. Combine conditions: Check exists AND compare value
- **Affected Operations**: Optional field handling, dynamic data structures
- **Best Practice**: Always check existence before comparing value

**Example Scenario**:
```
Bad: IF status equals "pending" (fails if field missing)
Good: IF status exists AND status equals "pending"
```
</limitation>
</critical_limitations>

<authentication>
## No Authentication Required

The IF node is a built-in N8N core node and requires no authentication. It operates on local data only with no external service calls.

**Built-In Node Characteristics**:
- No credentials needed
- No API keys required
- No external dependencies
- Zero latency (local evaluation)
- Available in all N8N instances (self-hosted and cloud)
- No permission restrictions
</authentication>

<common_use_cases>
## Common Use Cases

### 1. Data Validation and Filtering
**Scenario**: Route records to appropriate processing based on data quality
- **Typical workflow**: Webhook → IF (validate required fields) → True: Process, False: Error notification
- **Why this operation**: Prevent invalid data from reaching critical operations
- **Considerations**: Performance with large datasets, null handling, type safety
- **N8N Pattern**: IF → Set/HTTP depending on condition

### 2. Error Handling and Recovery
**Scenario**: Handle different outcomes from API calls gracefully
- **Typical workflow**: HTTP Request → IF (check status) → True: Continue, False: Retry/Alert
- **Why this operation**: Build resilient workflows that handle failures
- **Considerations**: Error message parsing, retry logic, notification preferences
- **N8N Pattern**: IF → Error Trigger for false branch

### 3. Multi-Step Approval Workflows
**Scenario**: Route items through different approval paths based on criteria
- **Typical workflow**: Trigger → IF (amount > limit) → True: Manager approval, False: Auto-approve
- **Why this operation**: Implement policy-based routing
- **Considerations**: Budget thresholds, approval levels, audit trails
- **N8N Pattern**: IF → Separate approval chains

### 4. Data Enrichment Decision Logic
**Scenario**: Determine if additional data lookup is needed
- **Typical workflow**: Parse data → IF (required fields missing) → True: Lookup, False: Continue
- **Why this operation**: Optimize API calls by conditionally fetching additional data
- **Considerations**: Cache hits, API rate limits, data completeness
- **N8N Pattern**: IF → Optional HTTP Request

### 5. Scheduling and Time-Based Routing
**Scenario**: Route tasks based on business hours or dates
- **Typical workflow**: Trigger → IF (current time in business hours) → True: Process now, False: Queue
- **Why this operation**: Handle different processing based on timing
- **Considerations**: Timezone handling, holiday calendars, time formatting
- **N8N Pattern**: IF with Date comparison → Schedule or Process

### 6. Feature Flag and A/B Testing
**Scenario**: Route workflows based on configuration flags
- **Typical workflow**: Trigger → IF (feature enabled) → True: New flow, False: Legacy flow
- **Why this operation**: Control feature rollout without redeployment
- **Considerations**: Configuration management, fallback behavior, monitoring
- **N8N Pattern**: IF comparing configuration variables

### 7. Data Type Detection
**Scenario**: Handle different data types differently in workflow
- **Typical workflow**: Webhook → IF (field is number) → True: Math operations, False: String operations
- **Why this operation**: Ensure type-safe operations on dynamic input
- **Considerations**: Type conversion, validation, error handling
- **N8N Pattern**: IF with type-specific comparisons
</common_use_cases>

<best_practices>
## Best Practices

### Condition Design
1. **Keep conditions simple**: Complex logic should go in Code node
   - Impact: Easier debugging, better readability
   - Bad: `IF $json.amount > 1000 AND $json.type === 'order' AND $json.status !== 'cancelled'`
   - Good: Set node calculates qualifying orders, then simple IF check
   - N8N Implementation: Use Set node to pre-process, IF for final decision

2. **Order conditions by cost**: Evaluate cheap checks before expensive ones
   - Impact: Performance optimization, faster false branch execution
   - Cheap: Field existence, string comparisons
   - Expensive: API calls, complex regex, database lookups
   - N8N Implementation: Left-to-right evaluation with AND short-circuit

3. **Explicit null/empty checks**: Never assume missing fields are falsy
   - Impact: Prevents silent failures, explicit intent
   - Good: `field exists AND field is not empty AND field equals "value"`
   - Use: "exists", "is empty", "does not exist" operators

4. **Type safety**: Convert types before comparison
   - Impact: Prevents type coercion bugs
   - Use Set node: `{{ Number($json.value) }}` before numeric comparison
   - Test with actual data types from your source

5. **Meaningful branch routing**: Don't nest IF nodes excessively
   - Impact: Readability, maintainability
   - Good: IF for binary logic, Switch for 3+ branches
   - N8N Pattern: IF → Merge nodes for combined outputs

### Error Handling
1. **Handle both branches**: Don't leave false branch unhandled
   - Impact: Prevents silent failures
   - Pattern: IF → Set (logging) → Continue or Error Trigger
   - Both branches should have business logic

2. **Add logging for debugging**: Log condition values for troubleshooting
   - Use Set node before IF to capture values
   - Example: Set → Log → IF condition
   - Helps identify why condition evaluated unexpectedly

3. **Use Error Trigger for failures**: Capture when branch logic fails
   - Impact: Prevents silent workflow failures
   - Pattern: Both IF branches → Error Trigger configured
   - Alert on unexpected conditions

### Performance Optimization
1. **Avoid redundant conditions**: Don't repeat checks in multiple IF nodes
   - Impact: Reduced latency, better readability
   - Pattern: Single IF node with multiple conditions vs. nested IFs
   - Use AND operator instead of nested nodes

2. **Filter before IF**: Use Filter node to reduce items, then IF for routing
   - Impact: Fewer branch executions
   - Pattern: Filter → IF (less data to evaluate)
   - Especially important with Loop Over Items

3. **Leverage data from previous nodes**: Don't recalculate in condition
   - Impact: Zero computation overhead in IF
   - Use Set node to pre-calculate comparison values
   - Reference set values in IF condition

### Debugging
1. **Test conditions separately**: Use Set node to preview condition values
   - Strategy: Add Set node, use expression preview to test
   - Verify actual values match expectations
   - Check data types before IF evaluation

2. **Add intermediate logging**: Set node with condition values
   - Pattern: Previous node → Set (log actual values) → IF
   - Captures what IF actually evaluated
   - Critical for troubleshooting type issues

3. **Validate with sample data**: Test IF logic with expected inputs
   - Use Execute Node on individual items
   - Verify both true and false branches work
   - Check edge cases (null, empty, zero, negative numbers)

### Data Flow
1. **Know IF doesn't filter**: IF routes, doesn't remove items
   - Use Filter node if you need to remove items
   - IF passes full data to both branches unchanged
   - For item-level filtering: Loop → IF → Collect pattern

2. **Merge branches appropriately**: Combine results from both IF paths
   - Use Merge node when both branches produce outputs
   - Ensure consistent data structure
   - Handle missing fields from conditional branches

3. **Document branch purposes**: Add descriptive names or comments
   - Impact: Team understanding, maintenance
   - N8N Feature: Use action descriptions
   - Example: "True: Premium customers", "False: Free tier customers"
</best_practices>

<common_errors>
## Common Errors & Troubleshooting

<error ref="err-001" http_code="comparison-type-error">
**Error**: "Unexpected comparison result" or condition always true/false
- **Cause**: Type mismatch in comparison (string "100" vs number 100)
- **N8N Context**: IF evaluates condition differently than expected
- **Fix**:
  1. Check data types: Use Set node to preview actual types
  2. Convert types explicitly: Use `Number()`, `String()` functions
  3. Test in Set node expression preview first
  4. Verify API returns expected data type
  5. Add logging Set node to capture comparison values
- **Prevention**: Always validate input data types, use type conversion
</error>

<error ref="err-002" http_code="empty-field-error">
**Error**: Condition triggers on empty/missing fields unexpectedly
- **Cause**: Not checking for empty or null explicitly
- **N8N Context**: IF with value comparison but field is empty
- **Fix**:
  1. Use "is empty" operator explicitly
  2. Check "does not exist" for missing fields
  3. Combine conditions: `exists AND equals "value"`
  4. Add Set node validation before IF
  5. Test with actual empty/null values
- **Prevention**: Always use explicit null/empty checks
</error>

<error ref="err-003" http_code="logic-error">
**Error**: Wrong branch executes or both branches execute
- **Cause**: AND/OR operator misunderstood or condition logic error
- **N8N Context**: Business logic produces wrong result
- **Fix**:
  1. Check AND vs OR selection in IF node
  2. Simplify complex conditions
  3. Test each condition independently
  4. Add Set node logging before IF
  5. Verify condition with sample data
- **Prevention**: Test conditions thoroughly before deployment
</error>

<error ref="err-004" http_code="expression-error">
**Error**: "Expression error" or syntax error in condition
- **Cause**: Invalid expression syntax, undefined variables
- **N8N Context**: IF node shows red error indicator
- **Fix**:
  1. Check for typos in field names: `$json.fieldname` (case-sensitive)
  2. Validate expression in Set node first (has preview)
  3. Use proper syntax: `$json.field` not `field`
  4. Escape special characters in strings
  5. Check bracket/parenthesis balance
- **Prevention**: Use expression preview before IF, test with sample data
</error>

<error ref="err-005" http_code="data-flow-error">
**Error**: Data missing in one branch or incomplete output
- **Cause**: Both branches not connected, missing Merge node
- **N8N Context**: Execution completes but output looks wrong
- **Fix**:
  1. Verify both true and false branches connected
  2. Add Merge node to combine branches
  3. Check data structure in both branches (may differ)
  4. Use Set node to normalize output
  5. Test both branches independently
- **Prevention**: Add Merge node, verify connections, test edge cases
</error>

<error ref="err-006" http_code="performance-error">
**Error**: Workflow execution slow with IF node
- **Cause**: Complex conditions, expensive expressions, many IF nodes
- **N8N Context**: IF takes significant time in execution log
- **Fix**:
  1. Simplify expressions: Move complex logic to Code node
  2. Order conditions: Cheap checks before expensive
  3. Use Filter before IF to reduce items
  4. Replace nested IFs with Switch node
  5. Avoid API calls in conditions
- **Prevention**: Keep conditions simple, profile slow workflows
</error>

<error ref="err-007" http_code="null-reference-error">
**Error**: "Cannot read property of undefined/null"
- **Cause**: Accessing nested field that doesn't exist
- **N8N Context**: Error in condition evaluation
- **Fix**:
  1. Check field exists first: `field does not exist`
  2. Use optional chaining: `$json.user?.profile?.name`
  3. Add Set node to validate structure
  4. Use get() function: `$json.get('field.nested')`
  5. Provide defaults: `$json.field ?? 'default'`
- **Prevention**: Always check existence before accessing properties
</error>

<error ref="err-008" http_code="merge-node-error">
**Error**: Both IF branches execute or duplicate data
- **Cause**: Legacy N8N v0 behavior (fixed in v1.0+)
- **N8N Context**: Merge node after IF produces duplicates
- **Fix**:
  1. Upgrade N8N to v1.0+ (recommended)
  2. For v0: Add intermediate nodes between IF and Merge
  3. Test merge behavior in your version
  4. Use separate processing for each branch
- **Prevention**: Use N8N v1.0+, test edge cases
</error>

### String Comparison Issues
- **"String equals doesn't work"**: Check exact match, including spaces/case
  - Solution: Use "contains" for partial match, or trim whitespace
  - Test exact value: `"  test  "` vs `"test"`
- **"Contains is case-sensitive"**: String comparison is case-sensitive
  - Solution: Use Code node for case-insensitive: `$json.field.toLowerCase()`
- **"Special characters break comparison"**: Quotes, regex chars need escaping
  - Solution: Test in Set node expression preview

### Number Comparison Issues
- **"Zero equals fails"**: Zero (0) is valid number, not falsy
  - Solution: Use explicit comparison: `equals 0`
- **"String that looks like number fails"**: "100" (string) ≠ 100 (number)
  - Solution: Convert with `Number()` in Set node first
- **"Decimal precision issues"**: 0.1 + 0.2 ≠ 0.3 in JavaScript
  - Solution: Round before comparison or use Code node for precision

### Date Comparison Issues
- **"Date format not recognized"**: Wrong date format in comparison
  - Solution: Standardize to ISO 8601: `YYYY-MM-DDTHH:mm:ssZ`
  - Use Date functions: `new Date()` for current time
- **"Timezone issues"**: Local time vs UTC mismatch
  - Solution: Convert all to UTC before comparison
  - Document expected timezone in workflow
</common_errors>

<related_operations>
## Related Control Flow Nodes

### Similar Conditional Nodes
- **Switch**: For 3+ conditional outputs (better than nested IFs)
- **Filter**: For filtering items (IF doesn't filter, only routes)
- **Error Trigger**: Catch and handle errors from any node

### Common Supporting Nodes
- **Set (Edit Fields)**: Transform/normalize data before IF
- **Code Node**: Complex logic before IF decision
- **Merge**: Combine outputs from IF branches
- **Loop Over Items**: Iterate, then IF for per-item logic
- **Split In Batches**: Batch processing with IF conditions

### Workflow Patterns
1. **Conditional Processing**: Trigger → IF (condition) → Different actions
2. **Error Handling**: HTTP Request → IF (check status) → Success/Error path
3. **Approval Workflows**: Trigger → IF (amount > limit) → Manager/Auto-approve
4. **Data Routing**: Parse → IF (type) → Route to appropriate processor
5. **Quality Control**: IF (validation) → True: Process, False: Reject
6. **Feature Flags**: IF (config flag) → New version or legacy version
7. **Audit & Logging**: All IF branches → Log/Archive

### See Also
- **Switch Node**: Better for 3+ branches, more readable
- **Filter Node**: Specifically for removing/keeping items
- **Code Node**: Complex conditional logic
- **Error Handling**: Error Trigger for failure paths
- **Flow Logic**: N8N documentation on conditional routing
</related_operations>

<troubleshooting>
## Troubleshooting Guide

### Condition Not Evaluating as Expected

**Problem**: IF always returns true or always returns false
- **Check**: Data type mismatch, comparison operator selection
- **Solution**:
  1. Add Set node before IF with: `{{ { condition_value: $json.field, condition_type: typeof $json.field } }}`
  2. Review the Set output to see actual value and type
  3. Verify comparison operator matches data type
  4. Test with specific sample values
  5. Check for special characters, whitespace, case sensitivity
- **N8N Tools**:
  - Execute Node on individual items to debug
  - Use expression preview in Set node
  - Add logging Set node before IF

**Problem**: Condition works with test data but fails in production
- **Check**: Different data structure in production, missing fields
- **Solution**:
  1. Capture actual production data: Add Set node logging
  2. Add null/empty checks: Assume fields might be missing
  3. Use "exists" operator before value comparison
  4. Provide defaults in Set node
  5. Test with production data sample
- **N8N Tools**:
  - Check execution logs for actual values
  - Add intermediate logging steps
  - Test in staging with real data

### Performance Issues

**Problem**: Workflow with IF nodes executing slowly
- **Check**: Complex expressions, expensive operations, nested IFs
- **Solution**:
  1. Simplify conditions: Break complex logic into Set node
  2. Profile slow nodes: Check execution time in logs
  3. Move expensive operations: API calls should be before IF
  4. Replace nested IFs: Use Switch node for multiple branches
  5. Filter early: Remove unneeded items before IF
- **N8N Tools**:
  - Monitor execution time per node
  - Use Code node for complex logic
  - Batch operations instead of per-item IFs

### Data Flow Issues

**Problem**: Data missing from one IF branch or different structure
- **Check**: Different data in true vs false branches, missing fields
- **Solution**:
  1. Verify both branches process correctly: Test independently
  2. Normalize data: Set node after IF to ensure consistent structure
  3. Use Merge node: Combine branches with matching fields
  4. Add optional fields: Set node provides defaults
  5. Log output: Verify data structure in each branch
- **N8N Tools**:
  - Execute individual branches to verify output
  - Use Set node to normalize structure
  - Compare field lists from each branch

### Complex Logic Issues

**Problem**: IF with multiple AND/OR conditions behaving incorrectly
- **Check**: Operator precedence, parenthesis grouping, condition order
- **Solution**:
  1. Simplify: Break into multiple IF nodes
  2. Test individually: Each condition separately
  3. Add Set node: Calculate intermediate boolean values
  4. Use Code node: For complex boolean logic
  5. Document: Add comments explaining logic
- **N8N Tools**:
  - Code node for complex logic
  - Multiple simple IFs vs one complex IF
  - Expression preview for testing

### Merge Node Issues

**Problem**: Data duplicates, both branches execute with Merge
- **Check**: N8N version (v0 vs v1.0+), Merge configuration
- **Solution**:
  1. Upgrade N8N if on v0 (behavior fixed in v1.0+)
  2. Verify Merge configuration: Check connection settings
  3. Add intermediate nodes: Between IF and Merge
  4. Test branch isolation: Ensure branches are independent
  5. Log at each step: Verify data flow
- **N8N Tools**:
  - Check N8N version: `Help → About`
  - Monitor executions: Track duplicate items
  - Add logging Set nodes

### Testing & Validation

**Best Practice Debugging**:
1. Add Set node before IF with: `{{ { actual_value: $json.field, actual_type: typeof $json.field } }}`
2. Review output in Set node to understand actual data
3. Test condition in IF with confirmed value
4. Execute Node on sample data
5. Gradually expand test cases: null, empty, edge cases

**Common Test Cases**:
- Empty string: `""`
- Zero: `0`
- Null/undefined: `null`, `undefined`
- Whitespace: `"  "`
- Special characters: quotes, regex chars
- Large numbers: `999999999999`
- Very long strings: >10000 chars

**Documentation**:
- Add description to each IF node
- Document what each branch does
- Note expected data types
- Comment complex conditions
</troubleshooting>

---

**Documentation Status**: ✅ **COMPLETE & PRODUCTION-READY**
**Last Updated**: 2025-10-31
**Next Steps**: Document Switch, Merge, and other core control flow nodes