# Variable Connector

## Overview
**Triggers**: 0
**Actions**: 6

The Variable connector provides state management capabilities within flows, allowing storage and manipulation of values across actions.

## Variable Types

1. **String** - Text values
2. **Integer** - Whole numbers
3. **Float** - Decimal numbers
4. **Boolean** - true/false
5. **Array** - Collections of items
6. **Object** - JSON objects

## Actions

### Initialize variable
**Description**: Creates and sets initial value for a variable
**Parameters**:
- Name (required) - Variable name (alphanumeric, no spaces)
- Type (required) - String, Integer, Float, Boolean, Array, Object
- Value (optional) - Initial value

**Important Notes**:
- **Must be initialized before use**
- Can only initialize once per variable name
- Scope is entire flow
- Place near start of flow
- Cannot reinitialize

**Use Cases**:
- Counter initialization
- Flag setting
- Data accumulation
- State tracking

**Examples**:

**String variable**:
```
Name: userName
Type: String
Value: "John Doe"
```

**Integer counter**:
```
Name: itemCount
Type: Integer
Value: 0
```

**Boolean flag**:
```
Name: hasError
Type: Boolean
Value: false
```

**Array**:
```
Name: userList
Type: Array
Value: []
```

**Object**:
```
Name: config
Type: Object
Value: {"retries": 3, "timeout": 30}
```

**Best Practices**:
- Initialize all variables at flow start
- Use descriptive names
- Set appropriate initial values
- Document variable purpose
- Group related initializations

---

### Set variable
**Description**: Updates value of existing variable
**Parameters**:
- Name (required) - Existing variable name
- Value (required) - New value

**Important Notes**:
- Variable must be initialized first
- Replaces entire value (not merge)
- Type must match initialization
- Use in loops to track state

**Use Cases**:
- Update status
- Reset values
- Replace data
- State changes

**Examples**:

**Update string**:
```
Name: status
Value: "Completed"
```

**Reset counter**:
```
Name: counter
Value: 0
```

**Update object**:
```
Name: result
Value: {"success": true, "message": "Done"}
```

**Best Practices**:
- Validate value before setting
- Maintain type consistency
- Use meaningful variable names
- Update in logical sequence

---

### Increment variable
**Description**: Increases integer or float variable by specified amount
**Parameters**:
- Name (required) - Variable name
- Value (required) - Amount to increment (can be negative)

**Type Support**: Integer, Float only

**Use Cases**:
- Loop counters
- Progress tracking
- Retry counters
- Statistics accumulation

**Examples**:

**Increment by 1**:
```
Name: counter
Value: 1
```

**Increment by 10**:
```
Name: totalScore
Value: 10
```

**Increment with dynamic value**:
```
Name: runningTotal
Value: @{items('Apply_to_each')?['amount']}
```

**Best Practices**:
- Use for counting operations
- Initialize to 0 before incrementing
- Consider overflow with large numbers
- Use in loop counters

---

### Decrement variable
**Description**: Decreases integer or float variable by specified amount
**Parameters**:
- Name (required) - Variable name
- Value (required) - Amount to decrement

**Type Support**: Integer, Float only

**Use Cases**:
- Countdown timers
- Remaining items tracking
- Decrementing quotas
- Reverse counters

**Examples**:

**Decrement by 1**:
```
Name: remainingAttempts
Value: 1
```

**Decrement quota**:
```
Name: availableSlots
Value: @{items('Apply_to_each')?['slotsUsed']}
```

**Best Practices**:
- Check for negative values
- Initialize to appropriate starting value
- Use for countdown scenarios
- Monitor lower bounds

---

### Append to array variable
**Description**: Adds item to end of array variable
**Parameters**:
- Name (required) - Array variable name
- Value (required) - Item to append

**Type Support**: Array only

**Important Notes**:
- Does not check for duplicates
- Maintains insertion order
- No size limit (but consider performance)
- Can append any JSON value

**Use Cases**:
- Collecting results
- Building lists
- Accumulating data
- Creating batches

**Examples**:

**Append string**:
```
Name: userNames
Value: "Alice"
```

**Append object**:
```
Name: results
Value: {
  "id": 123,
  "name": "Item",
  "status": "Success"
}
```

**Append from loop**:
```
Name: processedItems
Value: @{items('Apply_to_each')}
```

**Best Practices**:
- Initialize as empty array first
- Consider memory with large arrays
- Use for accumulation patterns
- Process in batches if needed

---

### Append to string variable
**Description**: Concatenates value to end of string variable
**Parameters**:
- Name (required) - String variable name
- Value (required) - String to append

**Type Support**: String only

**Use Cases**:
- Building messages
- Creating logs
- Concatenating text
- URL construction

**Examples**:

**Append text**:
```
Name: logMessage
Value: " - Processing completed"
```

**Append with newline**:
```
Name: report
Value: "@{items('Apply_to_each')?['name']} - Success\n"
```

**Build CSV**:
```
Name: csvData
Value: "@{items('Apply_to_each')?['name']},@{items('Apply_to_each')?['value']}\n"
```

**Best Practices**:
- Initialize to empty string or header
- Consider string length limits
- Add delimiters/newlines as needed
- Use Join for arrays instead

---

## Variable Patterns

### Pattern 1: Loop Counter
```
Initialize variable (counter, 0)
→ Do until (counter equals 10)
  → Actions
  → Increment variable (counter, 1)
```

### Pattern 2: Data Collection
```
Initialize variable (results, [])
→ Apply to each
  → Actions
  → Append to array (results, item data)
→ Process accumulated results
```

### Pattern 3: Error Tracking
```
Initialize variable (hasError, false)
→ Scope (Try)
  → Actions
→ Scope (Catch) - runs after Try fails
  → Set variable (hasError, true)
→ Condition (hasError equals true)
  → Handle error
```

### Pattern 4: Retry Logic
```
Initialize variable (retryCount, 0)
→ Do until (success OR retryCount >= 3)
  → Try action
  → If failed: Increment (retryCount, 1)
```

### Pattern 5: Accumulator
```
Initialize variable (total, 0)
→ Apply to each (items)
  → Increment variable (total, item.amount)
→ Use total
```

### Pattern 6: Status Tracking
```
Initialize variable (status, "Starting")
→ Set variable (status, "Processing")
→ Actions
→ Set variable (status, "Completed")
```

### Pattern 7: Message Builder
```
Initialize variable (message, "Report:\n")
→ Apply to each
  → Append to string (message, "- " + item + "\n")
→ Send email (message)
```

## Best Practices

### Initialization
1. Initialize all variables at flow start
2. Use clear, descriptive names
3. Set appropriate initial values
4. Document complex variables
5. Group related initializations

### Naming Conventions
- Use camelCase: `itemCount`, `hasError`
- Be descriptive: `totalProcessed` not `total`
- Indicate type if ambiguous: `userList`, `errorFlag`
- Avoid reserved words
- Keep names concise but clear

### Performance
1. Don't create unnecessary variables
2. Clear large arrays when no longer needed
3. Use appropriate types (integer vs float)
4. Avoid string concatenation in tight loops
5. Consider array size for append operations

### Reliability
1. Always initialize before use
2. Maintain type consistency
3. Handle null/empty values
4. Reset counters appropriately
5. Validate values before operations

### Debugging
1. Add compose actions to inspect values
2. Use descriptive variable names
3. Initialize with recognizable defaults
4. Log variable state at key points
5. Check variable scope

## Common Pitfalls

1. **Not initializing** - Variable must be initialized first
2. **Re-initializing** - Can only initialize once per variable
3. **Type mismatch** - Setting wrong type causes errors
4. **String length** - Very long strings cause performance issues
5. **Array size** - Large arrays consume memory
6. **Wrong scope** - Variables exist for entire flow only
7. **Concurrent modifications** - In parallel loops, behavior may be unexpected
8. **Null handling** - Check for null before operations

## Variable Scope

**Flow-level scope**:
- Variables accessible throughout entire flow
- Not shared between flow runs
- Not persisted after flow completes
- Each run has independent variable values

**Not available**:
- Scope-level variables
- Child flow access to parent variables
- Cross-flow variable sharing

## Limitations

1. **Maximum variables**: No documented hard limit, but consider performance
2. **Variable name**: Alphanumeric only, no spaces or special characters
3. **String length**: No hard limit, but performance degrades with very long strings
4. **Array size**: No hard limit, but memory considerations apply
5. **No variable deletion**: Once initialized, exists for flow duration
6. **No type conversion**: Must maintain consistent type

## Type-Specific Considerations

### String
- No length limit but consider performance
- Use for text, status values, messages
- Append builds incrementally
- Consider Join for arrays instead of repeated appends

### Integer
- Whole numbers only
- Use for counts, IDs, indices
- Increment/Decrement available
- Consider overflow with very large values

### Float
- Decimal numbers
- Use for calculations, percentages, measurements
- Be aware of floating-point precision issues
- Increment/Decrement available

### Boolean
- true or false only
- Use for flags, status indicators
- Set to true/false explicitly
- Common in conditional logic

### Array
- Can contain any JSON values
- Maintains insertion order
- No duplicate checking
- Use for collections, batches, results
- Consider size for performance

### Object
- JSON object structure
- Use for complex data
- Set replaces entire object (no merge)
- Access properties with expressions
