# N8N Core Nodes Overview

---
type: category-overview
category: Core Nodes
node_count: 15+
version: 1.0
last_updated: 2025-10-31
keywords: [core, built-in, http, webhook, code, schedule, data-transformation, logic]
official_docs_url: https://docs.n8n.io/integrations/builtin/core-nodes/
---

<description>
Core nodes are built-in N8N nodes that provide essential functionality for workflow automation without requiring external service integrations. These nodes handle HTTP requests, webhooks, data transformation, scheduling, conditional logic, and custom code execution. Core nodes are always available and require no installation or additional configuration beyond the workflow itself.
</description>

<core_categories>
## Node Categories

### HTTP & API Integration
- **HTTP Request**: Make API calls to any REST endpoint
- **Webhook**: Receive HTTP requests from external sources
- **HTTP Request Tool**: HTTP requests for AI agent tools

### Data Transformation
- **Set**: Transform, rename, and manipulate data fields
- **Code**: Execute custom JavaScript or Python code
- **Function**: Transform data with JavaScript expressions
- **Item Lists**: Split, merge, and aggregate items

### Flow Control & Logic
- **IF**: Conditional branching based on data
- **Switch**: Multi-way branching
- **Merge**: Combine data from multiple branches
- **Split In Batches**: Process large datasets in chunks
- **Loop Over Items**: Iterate over items with custom logic

### Scheduling & Triggers
- **Schedule**: Time-based workflow triggers (cron)
- **Wait**: Add delays in workflows
- **Execute Workflow**: Trigger other workflows

### Utilities
- **No Operation**: Pass-through for testing
- **Stop And Error**: Stop execution with custom error
- **Sticky Note**: Add documentation to workflows
</core_categories>

<node_listing>
## Available Core Nodes

### [HTTP Request](./http-request.md) ⭐ Most Used
**Purpose**: Make HTTP requests to any REST API

**Key Features**:
- All HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Multiple authentication schemes
- cURL import
- Pagination and batching
- Automatic retries

**Use Cases**:
- API integrations
- Data fetching
- Webhooks
- File uploads/downloads

**Complexity**: Low-Medium

---

### Webhook ⭐ Essential
**Purpose**: Receive HTTP requests from external sources

**Key Features**:
- Production and test webhooks
- Multiple authentication methods
- Custom response handling
- URL parameters and headers

**Use Cases**:
- Receive form submissions
- Third-party notifications
- Incoming API calls
- Real-time triggers

**Complexity**: Low

**Documentation**: Coming soon

---

### Code ⭐ Advanced
**Purpose**: Execute custom JavaScript or Python code

**Key Features**:
- JavaScript and Python support
- Access to N8N context ($input, $json, $items)
- npm package imports
- Custom transformations

**Use Cases**:
- Complex data transformations
- Custom business logic
- API response parsing
- Advanced calculations

**Complexity**: High

**Documentation**: Coming soon

---

### Schedule ⭐ Essential
**Purpose**: Trigger workflows on a schedule

**Key Features**:
- Cron expressions
- Interval scheduling
- Timezone support
- Skip on active execution

**Use Cases**:
- Daily reports
- Periodic data syncs
- Maintenance tasks
- Scheduled notifications

**Complexity**: Low

**Documentation**: Coming soon

---

### Set
**Purpose**: Transform and manipulate data

**Key Features**:
- Rename fields
- Add/remove fields
- Data type conversion
- Expression-based values

**Use Cases**:
- Data normalization
- Field mapping
- Prepare API requests
- Clean data

**Complexity**: Low

**Documentation**: Coming soon

---

### IF
**Purpose**: Conditional logic branching

**Key Features**:
- Multiple conditions (AND/OR)
- Various operators (equals, contains, greater than, etc.)
- Expression support
- True/False branches

**Use Cases**:
- Data filtering
- Error handling
- Business logic
- Workflow routing

**Complexity**: Low

**Documentation**: Coming soon

---

### Merge
**Purpose**: Combine data from multiple branches

**Key Features**:
- Multiple merge modes (append, merge by key, etc.)
- Configurable merge logic
- Handle duplicate keys

**Use Cases**:
- Combine API responses
- Join data from multiple sources
- Aggregate results
- Data enrichment

**Complexity**: Medium

**Documentation**: Coming soon

---

### Split In Batches
**Purpose**: Process large datasets in chunks

**Key Features**:
- Configurable batch size
- Reset between runs
- Process in parallel

**Use Cases**:
- Handle rate limits
- Process large files
- Batch API calls
- Memory management

**Complexity**: Medium

**Documentation**: Coming soon

</node_listing>

<getting_started>
## Getting Started with Core Nodes

### Essential Nodes for Beginners
1. **HTTP Request**: Learn to call APIs
2. **Webhook**: Receive data from external sources
3. **Set**: Transform data between nodes
4. **IF**: Add conditional logic

### Recommended Learning Path
1. Start with HTTP Request for simple API calls
2. Add IF nodes for conditional processing
3. Use Set to transform data formats
4. Implement Schedule for automation
5. Add error handling with try/catch patterns

### Common Patterns

**Pattern 1: API Data Fetching**
```
Schedule → HTTP Request (GET) → Set → Database
```

**Pattern 2: Webhook Processing**
```
Webhook → IF → HTTP Request → Send Notification
```

**Pattern 3: Batch Processing**
```
Schedule → HTTP Request → Split In Batches → Loop → Process
```

**Pattern 4: Data Transformation Pipeline**
```
Trigger → Set → Code → IF → Multiple Outputs
```
</getting_started>

<best_practices>
## Core Nodes Best Practices

### HTTP Request
- Always use credential store for authentication
- Enable retry for transient failures
- Use pagination for large datasets
- Import cURL from API docs

### Webhook
- Use authentication on production webhooks
- Validate incoming data
- Return appropriate HTTP status codes
- Test with test webhook first

### Code
- Keep code simple and maintainable
- Use built-in functions when available
- Handle errors explicitly
- Comment complex logic

### Set
- Use expressions for dynamic values
- Validate data types
- Document field mappings
- Keep transformations simple

### IF
- Use clear, meaningful condition names
- Combine related conditions
- Avoid nested IFs (use Switch instead)
- Handle both branches

### Scheduling
- Use appropriate cron expressions
- Set correct timezone
- Consider execution time
- Avoid overlapping executions

## General Best Practices

1. **Error Handling**: Add error handling to all critical nodes
2. **Logging**: Use Sticky Notes to document complex logic
3. **Testing**: Test with sample data before production
4. **Modularity**: Break complex workflows into sub-workflows
5. **Naming**: Use clear, descriptive node names
6. **Expressions**: Validate expressions in expression editor
7. **Performance**: Minimize unnecessary nodes
8. **Security**: Never hardcode credentials
</best_practices>

<troubleshooting>
## Common Issues Across Core Nodes

### Execution Failures
**Problem**: Workflow stops unexpectedly

**Solutions**:
- Enable "Continue On Fail" for error handling
- Add IF nodes to validate data
- Check execution logs for details
- Test nodes individually

### Data Format Errors
**Problem**: "Cannot read property of undefined"

**Solutions**:
- Use Set node to ensure required fields
- Add IF to check field existence
- Use Code node for complex transformations
- Validate expressions in editor

### Performance Issues
**Problem**: Workflow takes too long

**Solutions**:
- Use batching for large datasets
- Add delays between API calls
- Optimize expressions
- Split into sub-workflows

### Authentication Errors
**Problem**: HTTP Request fails with 401/403

**Solutions**:
- Verify credentials in credential store
- Check API key permissions
- Test credentials independently
- Review API documentation
</troubleshooting>

<related_docs>
## Documentation

### Individual Node Docs
- **[HTTP Request](./http-request.md)** - Comprehensive HTTP API integration guide
- **Webhook** - Coming soon
- **Code** - Coming soon
- **Schedule** - Coming soon
- **Set** - Coming soon

### External Resources
- **Official N8N Core Nodes**: https://docs.n8n.io/integrations/builtin/core-nodes/
- **N8N Community**: https://community.n8n.io/
- **Video Tutorials**: https://www.youtube.com/c/n8n-io
- **Workflow Templates**: https://n8n.io/workflows/

## Related Categories
- **[AI Nodes](../AI/overview.md)** - AI and LLM integrations
- **[App Nodes](../Apps/overview.md)** - Third-party service integrations
- **[Database Nodes](../Database/overview.md)** - Database connections

</related_docs>

<metadata_summary>
## Document Information

- **Last Updated**: 2025-10-31
- **Version**: 1.0
- **Documented Nodes**: 1/15+ (7% complete)
- **Priority Nodes Remaining**: Webhook, Code, Schedule, Set, IF
- **Next Review**: 2025-11-15
</metadata_summary>
