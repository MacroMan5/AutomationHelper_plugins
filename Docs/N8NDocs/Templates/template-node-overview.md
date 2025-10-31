# {NODE_NAME} Node Overview

<!--
INSTRUCTIONS FOR CLAUDE CODE:
1. Replace all {PLACEHOLDERS} with actual values
2. Fill YAML frontmatter with accurate metadata
3. Extract keywords from N8N documentation
4. Assign severity levels: critical, high, medium, low
5. Create unique IDs: lim-001, lim-002, err-001, etc.
6. Remove unused sections (don't leave empty)
7. For nodes without authentication, mark auth_required: false
-->

---
type: node-overview
node_name: {NODE_NAME}
node_type: core|app|ai|database|community
category: trigger|action|both
auth_required: true|false
version: 1.0
last_updated: {YYYY-MM-DD}
keywords: [{keyword1}, {keyword2}, {keyword3}, {category}, {use-case}]
related_nodes: [{Node1}, {Node2}]
rate_limits:
  service_rate_limit: {X requests per Y seconds (if applicable)}
  n8n_limit: none (N8N doesn't impose limits)
official_docs_url: {URL}
npm_package: {n8n-nodes-* if community node}
---

<official_docs>
{N8N Documentation URL for this node}
{NPM package URL if community node}
</official_docs>

<description>
{2-3 sentences describing node purpose, primary use cases, and value proposition}
</description>

<capabilities>
## Core Capabilities
- {Capability 1 - be specific}
- {Capability 2 - be specific}
- {Capability 3 - be specific}
- {Capability 4 - be specific}

## Supported Operations
- {Operation 1}: {brief description}
- {Operation 2}: {brief description}
- {Operation 3}: {brief description}
- {Operation 4}: {brief description}

## Integration Features
- {Feature 1 - e.g., "Webhook support for real-time events"}
- {Feature 2 - e.g., "Batch operations for bulk processing"}
- {Feature 3 - e.g., "Streaming support for large data"}
- {Feature 4 - e.g., "Built-in retry mechanism"}
</capabilities>

<rate_limits>
## Rate Limits

**Service-Level Throttling** (if applicable)
- **{X} requests per {Y} seconds** per account/API key
- Throttling scope: {per user / per app / per account}
- Retry-After header: {yes/no}
- N8N built-in retry: {yes/no}

**Operation-Specific Limits** (if applicable)
- {Operation name}: {X} requests per {Y} seconds
- {Operation name}: {X} requests per {Y} seconds

**N8N Platform Limits**
- No built-in rate limiting by N8N platform
- Self-hosted: Limited by server resources
- Cloud: {Specify cloud plan limits if applicable}

**Throttling Behavior**
- HTTP Status: {429 / other}
- Error message: "{typical error message}"
- N8N automatic retry: {yes/no}
- Recommended retry strategy: {exponential backoff / other}

## Size Limits

**Data Operations**
- Max items per execution: **{X}** (N8N default: 1000, configurable)
- Max item size: **{Y}KB/MB**
- Max request payload: **{Z}KB/MB**
- Memory limit: Depends on N8N instance configuration

**File Operations** (if applicable)
- Max file upload size: **{X}MB**
- Max file download size: **{Y}MB**
- Supported file types: {list}

## Timeout Limits
- Default timeout: **{X} seconds** (N8N default: 300s)
- Max timeout: **{Y} seconds** (configurable in N8N settings)
- Long-running operations: {supported/not supported}
- Async operations: {yes/no}
</rate_limits>

<critical_limitations>
## {Category 1 - e.g., "Authentication & Credentials"}

<limitation id="lim-001" severity="critical|high|medium|low">
**{Limitation Title}**: {Clear description of the limitation}

- **Impact**: {What operations/scenarios are affected}
- **Scope**: {When/where this applies}
- **Workaround**: {Solution or "None available"}
- **Affected Operations**: {List operations affected}

**Example Scenario**: {Concrete example of when user would hit this}
</limitation>

<limitation id="lim-002" severity="{level}">
**{Another Limitation}**: {Description}

- **Impact**: {Impact description}
- **Workaround**: {Workaround or "None"}
</limitation>

## {Category 2 - e.g., "Data Format Support"}

<limitation id="lim-003" severity="{level}">
{Content following same structure}
</limitation>

## {Category 3 - e.g., "Performance & Scale"}

<limitation id="lim-004" severity="{level}">
{Content following same structure}
</limitation>
</critical_limitations>

<authentication>
## Authentication Methods

{If auth_required: false, state "No authentication required - this is a built-in N8N node"}

### {Method 1 - e.g., OAuth2}
- Flow type: {Authorization Code / Client Credentials / other}
- Required credentials: {list}
- Token refresh: {automatic/manual}
- Credential storage: N8N encrypted credential store

### {Method 2 - e.g., API Key}
- Key location: {header / query parameter / body}
- Key name: {parameter name}
- How to obtain: {brief steps}

### {Method 3 - e.g., Basic Auth}
- Username/password required
- Credential storage: N8N encrypted credential store

## Credential Configuration in N8N

1. Navigate to **Credentials** in N8N
2. Click **Add Credential**
3. Select **{Credential Type}**
4. Fill in required fields:
   - **{Field 1}**: {description}
   - **{Field 2}**: {description}
5. Test connection
6. Save

## Required Permissions/Scopes

### {Service Name} Permissions
- **{Permission 1}**: {Why needed}
- **{Permission 2}**: {Why needed}
- **{Permission 3}**: {Why needed}

## Troubleshooting Authentication
- **Invalid credentials**: {How to diagnose and fix}
- **Token expiration**: {How N8N handles and renews}
- **Permission denied**: {Common causes and solutions}
</authentication>

<common_use_cases>
## 1. {Use Case Name}

**Description**: {What business problem this solves}

**Typical Workflow**:
```
Trigger: {trigger node}
↓
Node 1: {node name} - {purpose}
↓
Node 2: THIS NODE ({operation}) - {purpose}
↓
Node 3: {node name} - {purpose}
↓
Result: {outcome}
```

**Key Operations**: [{operation1}](./operations.md#op-id), [{operation2}](./operations.md#op-id)

**Best For**: {Scenarios where this pattern excels}

---

## 2. {Use Case Name}

{Same structure as above}

---

## 3. {Use Case Name}

{Same structure as above}

---

## 4. {Use Case Name}

{Same structure as above}

---

## 5. {Use Case Name}

{Same structure as above}
</common_use_cases>

<best_practices>
## Performance Optimization

### Execution Efficiency
1. **{Practice}**: {Explanation}
   - **Why**: {Benefit}
   - **How**: {Implementation in N8N}

2. **{Practice}**: {Explanation}
   - **Why**: {Benefit}
   - **How**: {Implementation}

### Throttling Management
1. **{Practice}**: {Explanation}
   - **N8N Setting**: {Which setting to configure}
   - **Recommended Value**: {What value to use}

2. **Implement Rate Limit Handling**: Use N8N built-in retry
   - **How**: Configure in node settings
   - **Backoff Strategy**: Exponential with max retries

### Data Processing
1. **Batch Operations**: Process items in batches
   - **Why**: Reduces API calls and memory usage
   - **How**: Use "Split in Batches" node before this node

2. **Pagination**: Handle large datasets with pagination
   - **Why**: Avoid memory issues and timeouts
   - **How**: {Specific implementation for this node}

## Reliability & Error Handling

### Retry Logic
1. **Enable Automatic Retry**: Configure retry settings in node
   - **Max Retries**: {recommended number}
   - **Retry Interval**: {recommended interval}
   - **Retry On**: {which HTTP codes to retry}

2. **Use Error Workflow**: Create dedicated error handling workflow
   - **Why**: Centralized error management
   - **How**: Link error workflow in N8N settings

### Error Recovery
1. **{Practice}**: {Explanation}
   - **N8N Feature**: {Which N8N feature to use}
   - **Implementation**: {Steps}

2. **Logging**: Enable execution logging
   - **Why**: Easier debugging and monitoring
   - **How**: N8N execution history + external logging

### Idempotency
1. **{Practice}**: {Explanation}
   - **Why**: Prevent duplicate processing
   - **How**: {Implementation strategy}

## Security Best Practices

### Credential Management
1. **Use N8N Credential Store**: Never hardcode credentials
   - **Why**: Encrypted storage, centralized management
   - **How**: Always use credential selector in nodes

2. **Rotate Credentials**: Regular credential rotation
   - **Why**: Security best practice
   - **How**: Update credentials in N8N credential manager

### Data Protection
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

### Access Control
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

## Workflow Design

### Node Placement
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

### Connection Management
1. **Reuse Credentials**: Use same credential across multiple nodes
   - **Why**: Easier management, consistent authentication
   - **How**: Select existing credential from dropdown

2. **Test Credentials**: Always test before production
   - **Why**: Catch authentication issues early
   - **How**: Use "Test step" button in N8N

### Data Flow
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}
</best_practices>

<troubleshooting>
## Common Errors

### Authentication Errors

<error id="err-401" http_code="401">
- **Symptom**: "Unauthorized" or "Invalid credentials"
- **Cause**: {Common causes}
- **Immediate Fix**:
  1. {Step 1}
  2. {Step 2}
  3. {Step 3}
- **Prevention**:
  - {How to avoid}
  - {Best practice}
- **N8N Logs**: Check execution logs for detailed error
- **Reference**: [Authentication](#authentication)
</error>

### Rate Limiting Errors

<error id="err-429" http_code="429">
- **Symptom**: "Too Many Requests" or "Rate limit exceeded"
- **Cause**: Exceeded service rate limits
- **Immediate Fix**:
  1. Enable retry with exponential backoff in node settings
  2. Add delay between executions
  3. Reduce concurrent executions
- **Prevention**:
  - Configure rate limiting in N8N
  - Use batch operations
  - Implement queue-based processing
- **N8N Feature**: Built-in retry mechanism
- **Reference**: [Rate Limits](#rate_limits)
</error>

### Timeout Errors

<error id="err-timeout" http_code="408|504">
- **Symptom**: "Request timeout" or "Gateway timeout"
- **Cause**: {Common causes}
- **Immediate Fix**:
  1. Increase timeout in node settings
  2. {Other fix}
- **Prevention**: {How to avoid}
- **N8N Setting**: Timeout configurable in node settings
- **Reference**: [Timeout Limits](#rate_limits)
</error>

### Data Format Errors

<error id="err-format" http_code="400">
- **Symptom**: "Invalid format" or "Bad request"
- **Cause**: {Common causes}
- **Immediate Fix**: {Steps}
- **Prevention**: {How to avoid}
- **N8N Tool**: Use "Set" node to transform data before this node
</error>

### Node-Specific Errors

<error id="err-custom-001" http_code="{code}">
**Error Code/Message**: "{specific error}"
- **Symptom**: {What user sees}
- **Cause**: {Why it happens}
- **Immediate Fix**: {Steps to resolve}
- **Prevention**: {How to avoid}
- **N8N Context**: {N8N-specific information}
</error>

## Diagnostic Steps

1. **Check N8N Execution Logs**
   - View execution history
   - Check input/output data
   - Review error messages
   - Inspect node configuration

2. **Test Node Isolation**
   - Run node with sample data
   - Verify credentials
   - Check service status
   - Test API directly (Postman/curl)

3. **Verify Configuration**
   - Node parameters
   - Credential settings
   - Workflow connections
   - Environment variables

4. **Review N8N Environment**
   - N8N version compatibility
   - Node version compatibility
   - Server resources (memory, CPU)
   - Network connectivity

5. **Check Service Status**
   - Service API status page
   - Recent service updates
   - Known issues
   - Maintenance windows
</troubleshooting>

<related_docs>
## Documentation Structure

- **Operations**: [operations.md](./operations.md) - All available operations
- **Examples**: [examples.md](./examples.md) - Real-world workflow examples

## Related Nodes

- **{Node 1}**: [{Link}](../Category/node1.md) - {Relationship/use case}
- **{Node 2}**: [{Link}](../Category/node2.md) - {Relationship/use case}
- **{Node 3}**: [{Link}](../Category/node3.md) - {Relationship/use case}

## External Resources

- **Official N8N Documentation**: {N8N docs URL}
- **Service API Documentation**: {Service API docs URL}
- **Community Discussions**: {Community forum links}
- **NPM Package**: {NPM URL if community node}
- **GitHub Repository**: {GitHub URL if open source}
- **Service Status Page**: {Status page URL}
</related_docs>

<metadata_summary>
## Document Information

- **Last Updated**: {YYYY-MM-DD}
- **Version**: 1.0
- **Completeness**: {X}% (Operations: {Y}/{Z})
- **Validation Status**: {Validated / Pending / Draft}
- **Next Review**: {YYYY-MM-DD}
- **N8N Version Tested**: {version}
- **Node Version**: {version}
</metadata_summary>
