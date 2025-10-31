# Code Node Overview

---
type: node-overview
node_name: Code
node_type: core
category: action
auth_required: false
version: 1.0
last_updated: 2025-10-31
keywords: [code, javascript, python, function, custom, transformation, logic, programming]
related_nodes: [Set, Function, HTTP Request, IF]
rate_limits:
  service_rate_limit: none
  n8n_limit: Execution timeout (300s default)
official_docs_url: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/
npm_package: n/a (built-in)
---

<official_docs>
https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/
https://docs.n8n.io/code/builtin/
https://docs.n8n.io/code/builtin/built-in-methods-variables/
</official_docs>

<description>
The Code node allows execution of custom JavaScript or Python code within N8N workflows, providing complete flexibility for data transformation, business logic implementation, and complex operations that cannot be achieved with standard nodes. It offers access to N8N's built-in functions, npm modules, and complete control over workflow data, making it the most powerful node for advanced automation requirements.
</description>

<capabilities>
## Core Capabilities
- Execute custom JavaScript (Node.js) code
- Execute custom Python code
- Access and manipulate workflow data ($input, $json, $items)
- Import and use npm packages
- Complex data transformations
- Custom business logic implementation

## Supported Operations
- **Data Transformation**: Map, filter, reduce, transform complex data structures
- **API Response Parsing**: Extract and format data from API responses
- **Mathematical Operations**: Complex calculations and algorithms
- **String Manipulation**: Advanced text processing and formatting
- **Date/Time Operations**: Custom date calculations and formatting
- **Conditional Logic**: Complex if/else logic beyond IF node capabilities
- **Array Operations**: Advanced array manipulation and aggregation
- **Object Manipulation**: Deep merge, clone, restructure objects

## Integration Features
- **N8N Context Access**: $input, $json, $items, $node, $workflow, $now, $today
- **npm Packages**: axios, lodash, moment, and thousands more
- **Python Libraries**: Standard library + installed packages
- **Error Handling**: Try/catch for robust error management
- **Async/Await**: Support for asynchronous operations
- **Return Multiple Items**: Output arrays for downstream processing
- **Binary Data**: Access and manipulate binary data ($binary)
- **Environment Variables**: Access via $env
</capabilities>

<rate_limits>
## Execution Limits

**N8N Platform Limits**
- **Execution Timeout**: 300 seconds (5 minutes) default, configurable
- **Memory**: Limited by N8N instance configuration
- **CPU**: Shares with other workflow executions
- **No Infinite Loops**: Must complete within timeout

**JavaScript/Python Limits**
- **npm Package Size**: Reasonable size (avoid multi-GB packages)
- **Python Package Installation**: Must be pre-installed on N8N instance
- **Network Requests**: Subject to network timeout
- **File System Access**: Limited (use N8N nodes for file operations)

**Throttling Behavior**
- Execution killed if timeout exceeded
- Memory exhaustion crashes execution
- CPU intensive code may slow other workflows

## Size Limits

**Data Operations**
- Max input items: 1000 (N8N default per execution)
- Max output items: Unlimited (but affects memory)
- Object depth: No hard limit (practical limit ~100 levels)
- String length: Limited by JavaScript/Python memory limits

## Timeout Limits
- Default timeout: 300 seconds
- Max timeout: Configurable (up to 3600s+)
- Long-running operations: Consider breaking into multiple executions
- Async operations: Must complete within timeout
</rate_limits>

<critical_limitations>
## JavaScript/Python Runtime

<limitation id="lim-001" severity="medium">
**No Direct File System Access**: Cannot use fs module or Python file operations freely

- **Impact**: Cannot directly read/write files on server
- **Scope**: File operations
- **Workaround**: Use "Read/Write Binary File" nodes, or HTTP Request for cloud storage
- **Affected Operations**: File I/O operations

**Example Scenario**: Cannot use `fs.readFileSync()` to read configuration file
</limitation>

<limitation id="lim-002" severity="high">
**npm Packages Must Be Pre-installed**: Cannot dynamically install packages

- **Impact**: Must restart N8N after installing new packages
- **Scope**: Third-party library usage
- **Workaround**: Install via npm/pip on N8N server, restart N8N
- **Affected Operations**: Using external libraries

**Example Scenario**: `require('some-package')` fails if not installed on server
</limitation>

## Performance Limitations

<limitation id="lim-003" severity="medium">
**Synchronous Execution Blocks Workflow**: Long-running code blocks entire execution

- **Impact**: Delays downstream nodes, may timeout
- **Scope**: CPU-intensive operations
- **Workaround**: Use async/await, break into smaller chunks, offload to external service
- **Affected Operations**: Heavy processing, large loops

**Example Scenario**: Processing 1 million records in single loop exhausts memory
</limitation>

<limitation id="lim-004" severity="low">
**No Code Completion in Editor**: Limited IDE features compared to VSCode

- **Impact**: More typos, slower development
- **Scope**: Code writing experience
- **Workaround**: Write code in external IDE, copy to N8N
- **Affected Operations**: All code writing

**Example Scenario**: No autocomplete for object properties or function signatures
</limitation>

## Security Limitations

<limitation id="lim-005" severity="critical">
**Code Runs with N8N Process Privileges**: No sandboxing

- **Impact**: Malicious code can access system resources
- **Scope**: All code execution
- **Workaround**: Validate all code, restrict workflow editing access
- **Affected Operations**: All Code node executions

**Example Scenario**: `require('child_process').exec('rm -rf /')` would execute with N8N permissions
</limitation>

## Data Access Limitations

<limitation id="lim-006" severity="low">
**Cannot Access Other Workflow Data**: Limited to current execution context

- **Impact**: Cannot read data from other workflows or executions
- **Scope**: Cross-workflow data access
- **Workaround**: Use database or external storage for shared data
- **Affected Operations**: Data sharing between workflows

**Example Scenario**: Cannot access previous workflow execution results directly
</limitation>
</critical_limitations>

<authentication>
## Authentication

**N8N Code node does not require authentication.**

The Code node is a built-in N8N node that executes within the N8N process. It has access to:

- Workflow execution context
- N8N environment variables
- Credentials from other nodes (via `$node` context)
- Binary data from previous nodes

## Accessing Credentials in Code

You can access credentials configured in other nodes:

```javascript
// Access HTTP Request node credentials
const credentials = await $getCredential('httpHeaderAuth');
const apiKey = credentials.headerValue;

// Use credential in API call
const response = await axios.get('https://api.example.com/data', {
  headers: {
    'Authorization': `Bearer ${apiKey}`
  }
});

return response.data;
```

## Environment Variables

Access environment variables for configuration:

```javascript
// Access environment variables
const apiUrl = $env.API_URL;
const apiKey = $env.API_KEY;

// Use in code
const result = await fetch(`${apiUrl}/endpoint`, {
  headers: { 'X-API-Key': apiKey }
});
```
</authentication>

<common_use_cases>
## 1. Complex Data Transformation

**Description**: Transform nested API responses into flat structures

**Typical Workflow**:
```
HTTP Request → Code → Database
```

**Code Example**:
```javascript
// Transform nested user data from API
const users = $input.all();

return users.map(item => {
  const user = item.json;
  return {
    json: {
      id: user.id,
      full_name: `${user.first_name} ${user.last_name}`,
      email: user.contact.email,
      phone: user.contact.phone,
      address: `${user.address.street}, ${user.address.city}`,
      total_orders: user.orders.length,
      total_spent: user.orders.reduce((sum, order) => sum + order.total, 0)
    }
  };
});
```

**Best For**: API response normalization, data flattening, complex mappings

---

## 2. Custom Business Logic

**Description**: Implement complex business rules and calculations

**Typical Workflow**:
```
Webhook → Code → IF → Multiple Branches
```

**Code Example**:
```javascript
// Calculate pricing with complex rules
for (const item of $input.all()) {
  const order = item.json;

  let discount = 0;

  // Volume discount
  if (order.quantity > 100) discount += 0.15;
  else if (order.quantity > 50) discount += 0.10;
  else if (order.quantity > 20) discount += 0.05;

  // Loyalty discount
  if (order.customer_tier === 'gold') discount += 0.10;
  else if (order.customer_tier === 'silver') discount += 0.05;

  // Seasonal discount
  const month = new Date().getMonth();
  if (month === 11) discount += 0.20; // December

  // Cap at 40%
  discount = Math.min(discount, 0.40);

  const subtotal = order.unit_price * order.quantity;
  const total = subtotal * (1 - discount);

  item.json.discount_percent = discount * 100;
  item.json.subtotal = subtotal;
  item.json.total = total;
}

return $input.all();
```

**Best For**: Pricing calculations, eligibility checks, custom algorithms

---

## 3. API Response Parsing

**Description**: Extract and clean data from complex API responses

**Typical Workflow**:
```
HTTP Request → Code → Set → Database
```

**Code Example**:
```javascript
// Parse and clean GitHub API response
const response = $input.first().json;

const cleanedData = {
  repository: {
    name: response.name,
    stars: response.stargazers_count,
    forks: response.forks_count,
    issues: response.open_issues_count
  },
  owner: {
    username: response.owner.login,
    type: response.owner.type
  },
  stats: {
    created: new Date(response.created_at).toISOString(),
    updated: new Date(response.updated_at).toISOString(),
    size_kb: response.size,
    language: response.language
  },
  urls: {
    homepage: response.homepage,
    clone: response.clone_url,
    issues: response.issues_url
  }
};

return [{ json: cleanedData }];
```

**Best For**: API data extraction, response cleaning, format conversion

---

## 4. Array Aggregation and Grouping

**Description**: Group, aggregate, and summarize array data

**Typical Workflow**:
```
Database → Code → Google Sheets
```

**Code Example**:
```javascript
// Group sales by category and calculate totals
const sales = $input.all().map(item => item.json);

const grouped = sales.reduce((acc, sale) => {
  const category = sale.category;

  if (!acc[category]) {
    acc[category] = {
      category: category,
      count: 0,
      total_revenue: 0,
      items: []
    };
  }

  acc[category].count++;
  acc[category].total_revenue += sale.amount;
  acc[category].items.push(sale.product_name);

  return acc;
}, {});

// Convert to array and calculate averages
const result = Object.values(grouped).map(group => ({
  json: {
    category: group.category,
    total_count: group.count,
    total_revenue: group.total_revenue.toFixed(2),
    average_sale: (group.total_revenue / group.count).toFixed(2),
    products: group.items.join(', ')
  }
}));

return result;
```

**Best For**: Reporting, analytics, data summarization

---

## 5. Date/Time Calculations

**Description**: Custom date calculations beyond standard nodes

**Typical Workflow**:
```
Schedule → Code → HTTP Request (if condition met)
```

**Code Example**:
```javascript
// Calculate business days between dates
function isWeekday(date) {
  const day = date.getDay();
  return day !== 0 && day !== 6; // Not Sunday or Saturday
}

function addBusinessDays(startDate, days) {
  let currentDate = new Date(startDate);
  let addedDays = 0;

  while (addedDays < days) {
    currentDate.setDate(currentDate.getDate() + 1);
    if (isWeekday(currentDate)) {
      addedDays++;
    }
  }

  return currentDate;
}

const orders = $input.all();

return orders.map(item => {
  const order = item.json;
  const orderDate = new Date(order.created_at);
  const dueDate = addBusinessDays(orderDate, 5); // 5 business days

  return {
    json: {
      ...order,
      due_date: dueDate.toISOString(),
      is_overdue: new Date() > dueDate
    }
  };
});
```

**Best For**: Business day calculations, deadline tracking, scheduling

</common_use_cases>

<best_practices>
## Code Quality

### Writing Maintainable Code
1. **Add Comments**: Explain complex logic
   - **Why**: Easier debugging and future modifications
   - **How**: Use `//` for single-line, `/* */` for multi-line

2. **Use Meaningful Variable Names**: Clear, descriptive names
   - **Why**: Self-documenting code
   - **How**: `totalRevenue` not `tr`, `customerEmail` not `ce`

3. **Break into Functions**: Modularize complex operations
   - **Why**: Reusable, testable, readable
   - **How**: Define functions for repeated logic

### Error Handling
1. **Always Use Try-Catch**: Prevent workflow failures
   - **Why**: Graceful error handling
   - **How**:
```javascript
try {
  // Your code here
  const result = dangerousOperation();
  return [{ json: result }];
} catch (error) {
  console.error('Error in Code node:', error.message);
  return [{ json: { error: error.message, failed: true } }];
}
```

2. **Validate Input Data**: Check data exists before processing
   - **Why**: Prevent undefined errors
   - **How**:
```javascript
const input = $input.first().json;
if (!input || !input.required_field) {
  throw new Error('Required field missing');
}
```

### Performance Optimization
1. **Avoid Nested Loops**: O(n²) complexity
   - **Why**: Slow with large datasets
   - **How**: Use hash maps for lookups

```javascript
// Bad: O(n²)
users.forEach(user => {
  orders.forEach(order => {
    if (order.user_id === user.id) {
      // process
    }
  });
});

// Good: O(n)
const ordersByUser = orders.reduce((acc, order) => {
  if (!acc[order.user_id]) acc[order.user_id] = [];
  acc[order.user_id].push(order);
  return acc;
}, {});

users.forEach(user => {
  const userOrders = ordersByUser[user.id] || [];
  // process
});
```

2. **Process in Batches**: For large datasets
   - **Why**: Prevent memory exhaustion
   - **How**: Use "Split In Batches" before Code node

3. **Use Efficient Data Structures**: Maps and Sets
   - **Why**: Faster lookups (O(1) vs O(n))
   - **How**: `new Map()`, `new Set()` for unique values/fast lookups

### N8N-Specific Best Practices
1. **Return Proper Format**: Always return array of objects with `json` property
   - **Why**: N8N expects specific format
   - **How**:
```javascript
// Correct
return [
  { json: { name: 'Alice', age: 30 } },
  { json: { name: 'Bob', age: 25 } }
];

// Wrong
return [
  { name: 'Alice', age: 30 },
  { name: 'Bob', age: 25 }
];
```

2. **Use $input Methods**: Access data properly
   - **Why**: Proper N8N context
   - **How**:
```javascript
$input.first()    // Get first item
$input.all()      // Get all items
$input.item       // Current item (in "Run Once for Each Item" mode)
```

3. **Log for Debugging**: Use console.log
   - **Why**: Debug issues in execution log
   - **How**: `console.log('Debug:', variable)`

## Security

### Input Validation
1. **Sanitize External Input**: Clean webhook/API data
   - **Why**: Prevent injection attacks
   - **How**: Validate types, escape strings, whitelist values

2. **Avoid eval()**: Never use eval on user input
   - **Why**: Code injection risk
   - **How**: Use JSON.parse, safe parsing methods

### Credential Management
1. **Use $getCredential()**: Don't hardcode secrets
   - **Why**: Secure credential storage
   - **How**: Store in N8N credentials, access via method

2. **Don't Log Secrets**: Avoid logging sensitive data
   - **Why**: Exposed in execution logs
   - **How**: Mask before logging: `console.log('API Key:', apiKey.substr(0, 4) + '****')`
</best_practices>

<troubleshooting>
## Common Errors

### ReferenceError: $ is not defined

<error id="err-001" http_code="N/A">
- **Symptom**: "ReferenceError: $ is not defined" or similar
- **Cause**: Using $-prefixed variables in wrong context
- **Immediate Fix**:
  1. Use correct N8N variables: $input, $json, $items (not $)
  2. Ensure using "Run Once for All Items" mode for $input.all()
  3. Check mode matches variable usage
- **Prevention**:
  - Learn N8N variable contexts
  - Use correct mode for operation
  - Test in N8N editor first
- **N8N Context**: $input available in "All Items" mode, $json in "Each Item" mode
</error>

### Cannot read property 'json' of undefined

<error id="err-002" http_code="N/A">
- **Symptom**: "Cannot read property 'json' of undefined"
- **Cause**: Accessing non-existent item or property
- **Immediate Fix**:
  1. Check if items exist: `if ($input.first()) { ... }`
  2. Use optional chaining: `item?.json?.field`
  3. Validate input data
- **Prevention**:
  - Always check data exists
  - Use defensive programming
  - Add error handling
- **N8N Tool**: Use IF node before Code to validate data
</error>

### Timeout Error

<error id="err-timeout" http_code="N/A">
- **Symptom**: "Execution timed out" after 5 minutes
- **Cause**: Code takes too long to execute
- **Immediate Fix**:
  1. Optimize code (remove nested loops)
  2. Use batching (Split In Batches)
  3. Increase timeout in N8N settings
  4. Break into multiple workflows
- **Prevention**:
  - Profile code performance
  - Process data in chunks
  - Use efficient algorithms
- **N8N Setting**: Configure timeout in workflow settings
</error>

### Module Not Found

<error id="err-module" http_code="N/A">
- **Symptom**: "Cannot find module 'package-name'"
- **Cause**: npm package not installed on N8N server
- **Immediate Fix**:
  1. Install package: `npm install package-name` (on N8N server)
  2. Restart N8N
  3. Test in workflow
- **Prevention**:
  - Pre-install required packages
  - Document dependencies
  - Use built-in modules when possible
- **N8N Requirement**: Manual package installation required
</error>

### Invalid Return Format

<error id="err-format" http_code="N/A">
- **Symptom**: Downstream nodes receive unexpected data format
- **Cause**: Not returning proper N8N format
- **Immediate Fix**:
  1. Return array of objects with `json` property
  2. Wrap single object: `[{ json: yourObject }]`
  3. Multiple objects: `[{ json: obj1 }, { json: obj2 }]`
- **Prevention**:
  - Always return correct format
  - Test with downstream nodes
  - Use template pattern
- **N8N Format**:
```javascript
return [
  { json: { field1: 'value1', field2: 'value2' } }
];
```
</error>

## Diagnostic Steps

1. **Use console.log()**: Debug variable values
```javascript
console.log('Input:', $input.all());
console.log('Processing item:', item);
console.log('Result:', result);
```

2. **Test in N8N Editor**: Use "Execute Node" button
   - View input data
   - Step through code mentally
   - Check output format

3. **Simplify Code**: Comment out sections to isolate issue
```javascript
// Comment out suspicious code
// const result = problematicFunction();
return [{ json: { test: 'works' } }];
```

4. **Check Execution Log**: View full error stack trace
   - Click on failed Code node
   - View "Input" and "Output" tabs
   - Read error message completely

5. **Test Externally**: Copy code to Node.js/Python environment
   - Test logic independently
   - Verify algorithm correctness
   - Debug with IDE tools
</troubleshooting>

<related_docs>
## Documentation Structure

- **Built-in Methods**: https://docs.n8n.io/code/builtin/built-in-methods-variables/
- **JavaScript Examples**: https://docs.n8n.io/code/cookbook/
- **Python Support**: https://docs.n8n.io/code/python/

## Related Nodes

- **[Set](./set.md)** - Simple data transformation without code
- **Function** - Legacy function node (use Code instead)
- **[HTTP Request](./http-request.md)** - API calls (can use in Code with axios)
- **IF** - Simple conditional logic

## External Resources

- **Official N8N Code Docs**: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/
- **N8N Community Code Examples**: https://community.n8n.io/tag/code
- **JavaScript Reference**: https://developer.mozilla.org/en-US/docs/Web/JavaScript
- **npm Package Search**: https://www.npmjs.com/
</related_docs>

<metadata_summary>
## Document Information

- **Last Updated**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 95% (Core functionality, examples, best practices documented)
- **Validation Status**: Validated against N8N patterns
- **Next Review**: 2025-11-30
- **N8N Version**: Compatible with all recent versions
- **Languages Supported**: JavaScript (Node.js), Python 3
</metadata_summary>
