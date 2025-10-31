# Data Operation Connector

## Overview
**Triggers**: 0
**Actions**: 7

The Data Operation connector handles data transformation and manipulation without requiring external services.

## Actions

### Compose
**Description**: Creates or transforms data of any type
**Parameters**:
- Inputs (required) - Any data type or expression

**Returns**: Transformed data

**Use Cases**:
- Data restructuring
- Expression evaluation
- Object creation
- Value transformation
- Testing expressions

**Examples**:
```
Simple value: "Hello World"
Expression: @{items('Apply_to_each')?['Name']}
Object: {"name": "John", "age": 30}
Array: ["item1", "item2", "item3"]
```

**Best Practices**:
- Use for complex expressions
- Name compose actions descriptively
- Reference outputs in subsequent actions
- Test transformations incrementally

---

### Create CSV table
**Description**: Converts array to CSV format
**Parameters**:
- From (required) - Array of objects
- Columns (optional) - Automatic or Custom

**Returns**: CSV formatted string

**Column Options**:
- Automatic: Uses all properties from first object
- Custom: Specify header and value mapping

**Use Cases**:
- Export to CSV file
- Email data as CSV
- Data interchange format

**Example Input**:
```json
[
  {"Name": "Alice", "Age": 30},
  {"Name": "Bob", "Age": 25}
]
```

**Example Output**:
```
Name,Age
Alice,30
Bob,25
```

**Best Practices**:
- Ensure consistent object structure
- Use custom columns for control
- Handle empty arrays
- Encode special characters

---

### Create HTML table
**Description**: Converts array to HTML table
**Parameters**:
- From (required) - Array of objects
- Columns (optional) - Automatic or Custom

**Returns**: HTML table markup

**Use Cases**:
- Email formatting
- Web page generation
- Report creation
- Visual data presentation

**Example Input**:
```json
[
  {"Product": "Laptop", "Price": 999},
  {"Product": "Mouse", "Price": 25}
]
```

**Example Output**:
```html
<table>
  <thead><tr><th>Product</th><th>Price</th></tr></thead>
  <tbody>
    <tr><td>Laptop</td><td>999</td></tr>
    <tr><td>Mouse</td><td>25</td></tr>
  </tbody>
</table>
```

**Best Practices**:
- Style with CSS in email clients
- Validate HTML output
- Handle null values
- Test with various data types

---

### Filter array
**Description**: Filters array based on condition
**Parameters**:
- From (required) - Array to filter
- Condition (required) - Filter expression

**Returns**: Filtered array (subset)

**Use Cases**:
- Data filtering
- Conditional processing
- Removing unwanted items
- Pre-processing before loops

**Example**:
```
From: [
  {"status": "active", "name": "Item1"},
  {"status": "inactive", "name": "Item2"},
  {"status": "active", "name": "Item3"}
]

Condition: status equals "active"

Result: [
  {"status": "active", "name": "Item1"},
  {"status": "active", "name": "Item3"}
]
```

**Best Practices**:
- Filter before Apply to each
- Use simple conditions when possible
- Check for empty result arrays
- Consider performance with large arrays

---

### Join
**Description**: Joins array elements into string with delimiter
**Parameters**:
- From (required) - Array of values
- Join with (required) - Delimiter string

**Returns**: Single concatenated string

**Use Cases**:
- Creating comma-separated lists
- Building URL parameters
- Formatting multi-value fields
- Email recipient lists

**Example**:
```
From: ["apple", "banana", "cherry"]
Join with: ", "
Result: "apple, banana, cherry"
```

**Best Practices**:
- Handle empty arrays
- Choose appropriate delimiter
- Consider string length limits
- Trim whitespace if needed

---

### Parse JSON
**Description**: Parses JSON string into structured data
**Parameters**:
- Content (required) - JSON string
- Schema (required) - JSON schema definition

**Returns**: Structured object with properties

**Critical Notes**:
- **Schema must be defined** for dynamic content access
- Use "Generate from sample" to create schema
- Invalid JSON causes flow failure
- Nested objects require nested schema

**Use Cases**:
- HTTP response parsing
- Configuration file reading
- Dynamic content handling
- API integration

**Example**:
```
Content: {"name": "John", "age": 30, "city": "NYC"}

Schema: {
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer"},
    "city": {"type": "string"}
  }
}

Access: @{body('Parse_JSON')?['name']} → "John"
```

**Best Practices**:
- Generate schema from sample payload
- Add error handling for invalid JSON
- Use optional properties for nullable fields
- Validate JSON before parsing

---

### Select
**Description**: Transforms array items by mapping properties
**Parameters**:
- From (required) - Source array
- Map (required) - Property mappings (key-value pairs)

**Returns**: New array with transformed objects

**Use Cases**:
- Property renaming
- Data reshaping
- Extracting specific fields
- Format conversion

**Example**:
```
From: [
  {"firstName": "John", "lastName": "Doe", "email": "john@example.com"},
  {"firstName": "Jane", "lastName": "Smith", "email": "jane@example.com"}
]

Map:
  name: @{item()?['firstName']} @{item()?['lastName']}
  contact: @{item()?['email']}

Result: [
  {"name": "John Doe", "contact": "john@example.com"},
  {"name": "Jane Smith", "contact": "jane@example.com"}
]
```

**Best Practices**:
- Use Select before Create CSV/HTML table
- Rename properties for clarity
- Combine or split fields as needed
- Test with sample data

---

## Common Data Operation Patterns

### Pattern 1: Filter and Transform
```
Filter array → Select → Create CSV table
```

### Pattern 2: Parse and Process
```
Parse JSON → Compose (extract specific value) → Use in actions
```

### Pattern 3: Array to String
```
Filter array → Select (extract property) → Join
```

### Pattern 4: Data Enrichment
```
Original array → Apply to each → Compose (add properties) → Result array
```

### Pattern 5: CSV Export
```
Get items → Select (map properties) → Create CSV table → Create file
```

## Best Practices

### Performance
1. Filter arrays early to reduce processing
2. Use Select to reduce data size
3. Parse JSON once and reuse
4. Avoid unnecessary transformations

### Error Handling
1. Validate JSON before Parse JSON
2. Check array length before operations
3. Handle null values in transformations
4. Use try-catch with Scope for risky operations

### Maintainability
1. Name actions descriptively
2. Document complex expressions
3. Use Compose to test expressions
4. Keep transformations simple and focused

### Common Pitfalls
1. **Parse JSON without schema** - Won't work with dynamic content
2. **Empty arrays** - Check length before processing
3. **Invalid JSON** - Validate format first
4. **Large datasets** - Consider pagination
5. **Null values** - Use null-coalescing operators
