# {CONNECTOR_NAME} Connector Overview

<!--
INSTRUCTIONS FOR CLAUDE CODE:
1. Replace all {PLACEHOLDERS} with actual values
2. Fill YAML frontmatter with accurate metadata
3. Extract keywords from Microsoft documentation
4. Assign severity levels: critical, high, medium, low
5. Create unique IDs: lim-001, lim-002, err-001, etc.
6. Remove unused sections (don't leave empty)
-->

---
type: connector-overview
connector_name: {CONNECTOR_NAME}
connector_type: standard|premium|custom
version: 1.0
last_updated: {YYYY-MM-DD}
keywords: [{keyword1}, {keyword2}, {keyword3}, {category}, {use-case}]
related_connectors: [{Connector1}, {Connector2}]
api_limits:
  calls_per_minute: {X}
  calls_per_hour: {Y}
  max_file_size_mb: {Z}
official_docs_url: {URL}
---

<official_docs>
{Microsoft Learn URL for this connector}
</official_docs>

<description>
{2-3 sentences describing connector purpose, primary use cases, and value proposition}
</description>

<capabilities>
## Core Capabilities
- {Capability 1 - be specific}
- {Capability 2 - be specific}
- {Capability 3 - be specific}
- {Capability 4 - be specific}

## Supported Operations
- {Operation category 1}: {brief description}
- {Operation category 2}: {brief description}
- {Operation category 3}: {brief description}

## Integration Features
- {Feature 1 - e.g., "Webhook support for real-time events"}
- {Feature 2 - e.g., "Batch operations for bulk processing"}
- {Feature 3 - e.g., "Delta queries for change tracking"}
</capabilities>

<api_limits>
## Rate Limits

**Connection-Level Throttling**
- **{X} API calls per {Y} seconds** per connection
- Throttling scope: {per user / per app / per tenant}
- Retry-After header: {yes/no}

**Action-Specific Limits**
- {Action name}: {X} calls per {Y} seconds
- {Action name}: {X} calls per {Y} seconds

**Throttling Behavior**
- HTTP Status: {429 / other}
- Error message: "{typical error message}"
- Automatic retry: {yes/no}

## Size Limits

**File Operations**
- Max file upload size: **{X}MB**
- Max file download size: **{Y}MB**
- Max attachment size: **{Z}MB**

**Data Operations**
- Max items per request: **{X}**
- Max batch size: **{Y} operations**
- Max request payload: **{Z}KB**

**List/Array Operations**
- Max items returned: **{X}** (pagination required beyond)
- Max filter complexity: {description}

## Timeout Limits
- Default timeout: **{X} seconds**
- Max timeout: **{Y} seconds**
- Long-running operations: {supported/not supported}
</api_limits>

<critical_limitations>
## {Category 1 - e.g., "Content Type Support"}

<limitation id="lim-001" severity="critical|high|medium|low">
**{Limitation Title}**: {Clear description of the limitation}

- **Impact**: {What operations/scenarios are affected}
- **Scope**: {When/where this applies}
- **Workaround**: {Solution or "None available"}
- **Affected Operations**: {List actions/triggers affected}

**Example Scenario**: {Concrete example of when user would hit this}
</limitation>

<limitation id="lim-002" severity="{level}">
**{Another Limitation}**: {Description}

- **Impact**: {Impact description}
- **Workaround**: {Workaround or "None"}
</limitation>

## {Category 2 - e.g., "Authentication & Permissions"}

<limitation id="lim-003" severity="{level}">
{Content following same structure}
</limitation>

## {Category 3 - e.g., "Performance & Scale"}

<limitation id="lim-004" severity="{level}">
{Content following same structure}
</limitation>
</critical_limitations>

<authentication>
## Supported Authentication Methods

### OAuth 2.0 (Recommended)
- Flow type: {Authorization Code / Client Credentials}
- Required scopes: {list}
- Token refresh: {automatic/manual}

### Service Principal
- Supported: {yes/no}
- Setup: {brief steps or link}
- Limitations: {if any}

### Legacy Authentication
- Status: {deprecated/supported/not available}
- Migration path: {if applicable}

## Required Permissions

### Delegated Permissions (User Context)
- **{Permission.Name}**: {Why needed and what it enables}
- **{Permission.Name}**: {Why needed and what it enables}

### Application Permissions (App-Only Context)
- **{Permission.Name}**: {Why needed and what it enables}
- **{Permission.Name}**: {Why needed and what it enables}

## Permission Troubleshooting
- Insufficient permissions error: {How to diagnose and fix}
- Conditional Access: {Impact and considerations}
</authentication>

<common_use_cases>
## 1. {Use Case Name}

**Description**: {What business problem this solves}

**Typical Flow**:
```
Trigger: {trigger name}
↓
Action 1: {action name} - {purpose}
↓
Action 2: {action name} - {purpose}
↓
Result: {outcome}
```

**Key Actions**: [{action1}](./actions.md#action-id), [{action2}](./actions.md#action-id)

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

### API Call Efficiency
1. **{Practice}**: {Explanation}
   - **Why**: {Benefit}
   - **How**: {Implementation}

2. **{Practice}**: {Explanation}
   - **Why**: {Benefit}
   - **How**: {Implementation}

### Throttling Management
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

### Batch Operations
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

## Reliability & Error Handling

### Retry Logic
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

### Idempotency
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

### Error Recovery
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

## Security Best Practices

### Authentication
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

### Data Protection
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

### Access Control
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

## Flow Design

### Trigger Selection
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

### Action Ordering
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}

### Variable Management
1. **{Practice}**: {Explanation}
2. **{Practice}**: {Explanation}
</best_practices>

<troubleshooting>
## Common Errors

### Throttling Errors (429)

<error id="err-429" http_code="429">
- **Symptom**: "Too Many Requests" or "Rate limit exceeded"
- **Cause**: Exceeded {X} calls per {Y} seconds limit
- **Immediate Fix**:
  1. Add delay between calls
  2. Implement exponential backoff
  3. Use batch operations
- **Prevention**:
  - Monitor API call count
  - Enable concurrency control limits
  - Cache frequently accessed data
- **Reference**: [API Limits](#api_limits)
</error>

### Authentication Errors (401)

<error id="err-401" http_code="401">
- **Symptom**: "Unauthorized" or "Access token is invalid"
- **Cause**: {Common causes}
- **Immediate Fix**: {Steps to resolve}
- **Prevention**: {How to avoid}
- **Reference**: [Authentication](#authentication)
</error>

### Permission Errors (403)

<error id="err-403" http_code="403">
- **Symptom**: "Forbidden" or "Insufficient permissions"
- **Cause**: {Common causes}
- **Immediate Fix**: {Steps to resolve}
- **Prevention**: {How to avoid}
- **Reference**: [Required Permissions](#authentication)
</error>

### Not Found Errors (404)

<error id="err-404" http_code="404">
- **Symptom**: "Resource not found" or "Item doesn't exist"
- **Cause**: {Common causes}
- **Immediate Fix**: {Steps to resolve}
- **Prevention**: {How to avoid}
</error>

### Timeout Errors

<error id="err-timeout" http_code="408">
- **Symptom**: "Request timeout" or "Operation timed out"
- **Cause**: {Common causes}
- **Immediate Fix**: {Steps to resolve}
- **Prevention**: {How to avoid}
- **Reference**: [Timeout Limits](#api_limits)
</error>

### Connector-Specific Errors

<error id="err-custom-001" http_code="{code}">
**Error Code/Message**: "{specific error}"
- **Symptom**: {What user sees}
- **Cause**: {Why it happens}
- **Immediate Fix**: {Steps to resolve}
- **Prevention**: {How to avoid}
</error>

## Diagnostic Steps

1. **Check Error Details**
   - Error code/message
   - Timestamp
   - Action that failed

2. **Verify Configuration**
   - Connection status
   - Permission levels
   - Parameter values

3. **Review Recent Changes**
   - Flow modifications
   - Permission changes
   - Service updates

4. **Test Incrementally**
   - Isolate failing action
   - Test with known-good data
   - Check service health
</troubleshooting>

<related_docs>
## Documentation Structure

- **Actions**: [actions.md](./actions.md) - All available actions
- **Triggers**: [triggers.md](./triggers.md) - All available triggers

## Related Connectors

- **{Connector 1}**: [{Link}](../Connector1/overview.md) - {Relationship/use case}
- **{Connector 2}**: [{Link}](../Connector2/overview.md) - {Relationship/use case}

## External Resources

- **Official Documentation**: {Microsoft Learn URL}
- **API Reference**: {API docs URL if different}
- **Known Issues**: {Link to known issues page}
- **Community Forum**: {Link to support forum}
- **Service Health**: {Link to status page}
</related_docs>

<metadata_summary>
## Document Information

- **Last Updated**: {YYYY-MM-DD}
- **Version**: 1.0
- **Completeness**: {X}% (Actions: {Y}/{Z}, Triggers: {A}/{B})
- **Validation Status**: {Validated / Pending / Draft}
- **Next Review**: {YYYY-MM-DD}
</metadata_summary>
