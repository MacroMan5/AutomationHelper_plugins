# Webhook Node Overview

---
type: node-overview
node_name: Webhook
node_type: core
category: trigger
auth_required: false
version: 1.0
last_updated: 2025-10-31
keywords: [webhook, trigger, http, receive, endpoint, api, integration, real-time]
related_nodes: [HTTP Request, Respond to Webhook, Wait]
rate_limits:
  service_rate_limit: none (receiver)
  n8n_limit: Depends on hosting (self-hosted vs cloud)
official_docs_url: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/
npm_package: n/a (built-in)
---

<official_docs>
https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/
https://docs.n8n.io/workflows/components/
</official_docs>

<description>
The Webhook node enables workflows to receive HTTP requests from external sources, acting as a trigger that starts workflow execution when called. It creates unique URLs that accept data from third-party services, forms, applications, or custom integrations, supporting multiple HTTP methods, authentication schemes, and response customization for building robust API endpoints and real-time integrations.
</description>

<capabilities>
## Core Capabilities
- Create unique webhook URLs for receiving HTTP requests
- Support all HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Production and test webhook modes
- Custom response configuration (status codes, headers, body)
- Real-time workflow triggering
- Multiple authentication methods

## Supported Operations
- **Receive POST Data**: Accept JSON, form-data, or raw body data
- **Receive GET Requests**: Handle query parameters and URL paths
- **File Uploads**: Receive binary files via multipart/form-data
- **Custom Responses**: Return data, status codes, and headers to caller
- **Authenticated Endpoints**: Secure webhooks with various auth methods
- **Path Parameters**: Dynamic URL paths with variables

## Integration Features
- **Production URLs**: Stable URLs for live integrations
- **Test URLs**: Temporary URLs for development and testing
- **Authentication**: Header Auth, Basic Auth, Query Auth, None
- **Response Modes**: First Entry Only, Last Entry Only, All Entries, No Response
- **Binary Data**: Automatic file upload handling
- **URL Parameters**: Access query strings and path variables
- **Request Headers**: Read incoming HTTP headers
- **IP Whitelisting**: Filter by source IP (requires reverse proxy)
</capabilities>

<rate_limits>
## Rate Limits

**N8N Platform Limits**
- **Self-hosted**: No built-in rate limiting (configure at web server level)
- **N8N Cloud**: Subject to plan limits (typically 1000-10000 executions/month)
- **Concurrent requests**: Depends on server resources
- **Timeout**: 120 seconds default per execution

**Recommended Rate Limiting**
- Use reverse proxy (nginx, Apache) for rate limiting
- Implement queue-based processing for high-volume webhooks
- Add authentication to prevent abuse
- Monitor execution counts

**Throttling Behavior**
- No automatic throttling by N8N
- Server may return 503 if overloaded
- Queue executions if concurrent limit reached
- N8N automatic retry: Not applicable (sender must retry)

## Size Limits

**Request Data**
- Max payload size: Typically 100MB (configurable in N8N settings)
- Max form-data file: Depends on server configuration
- Max URL length: 2048 characters (browser standard)
- Headers: 8KB total (typical web server limit)

**Response Data**
- Max response size: Limited by execution memory
- Timeout: 120 seconds default
- Binary data: Handled via `$binary` property

## Timeout Limits
- Default timeout: 120 seconds per execution
- Max timeout: Configurable in N8N settings (up to 3600s)
- Long-running workflows: Use async pattern with callbacks
- Immediate response: Use "Respond to Webhook" node for long processes
</rate_limits>

<critical_limitations>
## Webhook URL Limitations

<limitation id="lim-001" severity="high">
**Test Webhook URLs Change**: Test webhook URLs change when workflow is saved/restarted

- **Impact**: Test URLs not suitable for external integrations
- **Scope**: Test webhook mode only
- **Workaround**: Use Production webhook URLs for stable integrations
- **Affected Operations**: All test mode webhooks

**Example Scenario**: Form submits to test webhook; URL changes after workflow edit, breaking integration
</limitation>

<limitation id="lim-002" severity="medium">
**Production URL Requires Active Workflow**: Production webhooks only work when workflow is active

- **Impact**: Webhook returns 404 if workflow is inactive
- **Scope**: Production webhook mode
- **Workaround**: Ensure workflow is activated before sharing URLs
- **Affected Operations**: All production webhooks

**Example Scenario**: Deactivating workflow for maintenance breaks all incoming webhook calls
</limitation>

## Authentication Limitations

<limitation id="lim-003" severity="medium">
**No OAuth Support**: Webhook node doesn't support OAuth authentication

- **Impact**: Cannot validate OAuth tokens directly
- **Scope**: Authentication methods
- **Workaround**: Use Code node to validate tokens or use Basic Auth/Header Auth
- **Affected Operations**: Authenticated webhooks

**Example Scenario**: Third-party service sending OAuth bearer tokens requires custom validation
</limitation>

<limitation id="lim-004" severity="low">
**Basic Auth Cleartext**: Basic Auth credentials transmitted in Base64 (not encrypted)

- **Impact**: Credentials visible if not using HTTPS
- **Scope**: Basic Auth method
- **Workaround**: Always use HTTPS, prefer Header Auth with API keys
- **Affected Operations**: Basic Auth webhooks

**Example Scenario**: HTTP webhook with Basic Auth exposes credentials in network traffic
</limitation>

## Request Handling Limitations

<limitation id="lim-005" severity="medium">
**No Request Queuing**: Concurrent requests execute in parallel (may overwhelm resources)

- **Impact**: High-volume webhooks can crash N8N instance
- **Scope**: All webhook requests
- **Workaround**: Implement rate limiting at reverse proxy, use queue system
- **Affected Operations**: High-traffic webhooks

**Example Scenario**: 1000 simultaneous webhook calls exhaust server memory
</limitation>

<limitation id="lim-006" severity="low">
**Single Workflow Trigger**: Each webhook URL triggers only one workflow

- **Impact**: Cannot fan-out to multiple workflows from single URL
- **Scope**: Webhook URL routing
- **Workaround**: Use "Execute Workflow" node to call sub-workflows
- **Affected Operations**: All webhooks

**Example Scenario**: Same event needs to trigger multiple workflows requires duplication or sub-workflow pattern
</limitation>

## Response Limitations

<limitation id="lim-007" severity="medium">
**120-Second Timeout**: Webhook must respond within 120 seconds (default)

- **Impact**: Long-running workflows timeout before completion
- **Scope**: All webhook executions
- **Workaround**: Use "Respond to Webhook" node to send immediate response, then continue processing
- **Affected Operations**: Long-running workflows

**Example Scenario**: Workflow processing 10,000 records times out before sender receives response
</limitation>
</critical_limitations>

<authentication>
## Authentication Methods

### None (No Authentication)
- No authentication required
- **Security**: Vulnerable to abuse and spam
- **Use for**: Internal testing, low-security use cases
- **Not recommended for**: Production, public endpoints

### Header Auth
- Custom header name and expected value
- **Example**: `X-API-Key: your-secret-key-here`
- **Security**: Good if using HTTPS and strong keys
- **Use for**: API integrations, service-to-service communication
- **Best practice**: Use UUID or cryptographically random keys

### Basic Auth
- Username and password in Authorization header
- Encoded as Base64: `Authorization: Basic base64(username:password)`
- **Security**: Moderate (credentials in Base64, use HTTPS)
- **Use for**: Simple authentication, internal services
- **Limitation**: Credentials transmitted with every request

### Query Auth
- Authentication parameter in URL query string
- **Example**: `?api_key=your-secret-key`
- **Security**: Lower (visible in logs, browser history)
- **Use for**: Simple webhooks, when headers not available
- **Not recommended for**: Sensitive data, production APIs

## Credential Configuration in N8N

**Production Webhook URLs** (Stable):
```
https://your-n8n-instance.com/webhook/unique-path-here
https://your-n8n-instance.com/webhook-test/unique-path-here (test)
```

**Header Auth Setup**:
1. Enable authentication in webhook node
2. Select "Header Auth"
3. Set header name (e.g., "X-API-Key")
4. Set expected value (generate strong random key)
5. Share key securely with webhook sender

**Basic Auth Setup**:
1. Enable authentication
2. Select "Basic Auth"
3. Set username and password
4. Sender must use Authorization header with Basic credentials

## Security Best Practices

1. **Always Use HTTPS**: Encrypt data in transit
2. **Strong Authentication**: Use Header Auth with random keys (not "password123")
3. **Key Rotation**: Change authentication keys periodically
4. **Rate Limiting**: Implement at reverse proxy level
5. **Validate Input**: Check data format and values in workflow
6. **Log Monitoring**: Track unusual request patterns
7. **IP Whitelisting**: Restrict to known source IPs (if possible)
8. **CORS Configuration**: Control cross-origin requests
</authentication>

<common_use_cases>
## 1. Form Submission Processing

**Description**: Receive form submissions from websites and process data

**Typical Workflow**:
```
Trigger: Webhook (POST)
↓
Node 1: Set - Validate and clean form data
↓
Node 2: IF - Check for spam/invalid data
↓
Node 3: HTTP Request - Create CRM record
↓
Node 4: Send Email - Confirmation to submitter
↓
Result: Automated form processing with validation
```

**Configuration**:
- Method: POST
- Authentication: Header Auth (prevent spam)
- Response Mode: Return success message

**Best For**: Contact forms, registration forms, survey submissions

---

## 2. Third-Party Service Notifications

**Description**: Receive notifications from services (GitHub, Stripe, etc.)

**Typical Workflow**:
```
Trigger: Webhook (POST)
↓
Node 1: Code - Parse webhook payload
↓
Node 2: Switch - Route based on event type
↓
Node 3a: Slack - Notify team (payment received)
Node 3b: Database - Log event (new user)
↓
Result: Real-time event processing and notifications
```

**Configuration**:
- Method: POST
- Authentication: Query Auth or Header Auth (service-specific)
- Response Mode: Return 200 OK

**Best For**: Payment notifications, GitHub webhooks, service integrations

---

## 3. Mobile App Backend

**Description**: Create API endpoints for mobile or web applications

**Typical Workflow**:
```
Trigger: Webhook (POST /api/users)
↓
Node 1: IF - Validate authentication token
↓
Node 2: Code - Process business logic
↓
Node 3: Database - Query/update data
↓
Node 4: Respond to Webhook - Return JSON response
↓
Result: Custom API endpoint with authentication
```

**Configuration**:
- Method: POST, GET, PUT, DELETE
- Authentication: Header Auth (bearer token)
- Response Mode: Custom JSON response
- Path: Dynamic path with parameters

**Best For**: Mobile apps, SPAs, microservices

---

## 4. File Upload Processing

**Description**: Receive file uploads and process/store them

**Typical Workflow**:
```
Trigger: Webhook (POST multipart/form-data)
↓
Node 1: Code - Extract file from $binary
↓
Node 2: HTTP Request - Upload to S3/storage
↓
Node 3: Database - Save file metadata
↓
Node 4: Respond to Webhook - Return file URL
↓
Result: File upload API with storage integration
```

**Configuration**:
- Method: POST
- Content-Type: multipart/form-data
- Authentication: Header Auth
- Binary data: Enabled

**Best For**: Image uploads, document processing, attachment handling

---

## 5. Chatbot Webhooks

**Description**: Receive messages from chat platforms (Slack, Discord, etc.)

**Typical Workflow**:
```
Trigger: Webhook (POST from chat platform)
↓
Node 1: Code - Parse message and extract command
↓
Node 2: Switch - Route based on command
↓
Node 3: HTTP Request - Process command (API call)
↓
Node 4: Respond to Webhook - Send reply to chat
↓
Result: Interactive chatbot with commands
```

**Configuration**:
- Method: POST
- Authentication: Per platform (Slack: signature, Discord: token)
- Response Mode: Return message to chat
- Timeout: Fast response required

**Best For**: Slack bots, Discord bots, Teams integrations

</common_use_cases>

<best_practices>
## Performance Optimization

### Request Handling
1. **Use Respond to Webhook for Long Processes**: Send immediate response, continue processing
   - **Why**: Prevents timeout errors
   - **How**: Add "Respond to Webhook" node early, workflow continues after

2. **Implement Queueing**: For high-volume webhooks, use queue system
   - **Why**: Prevents server overload
   - **How**: Store requests in database, process with scheduled workflow

3. **Validate Early**: Check data format at workflow start
   - **Why**: Fail fast, save resources
   - **How**: Use IF node immediately after webhook trigger

### Throttling Management
1. **Configure Rate Limiting**: At reverse proxy level (nginx, Apache)
   - **Recommended**: 10-100 requests/minute per IP
   - **Implementation**: nginx limit_req_zone directive

2. **Monitor Execution Counts**: Track webhook usage
   - **Why**: Detect abuse, plan capacity
   - **How**: Log executions to database or monitoring service

### Response Optimization
1. **Return Minimal Data**: Only return necessary information
   - **Why**: Faster response, less bandwidth
   - **How**: Use Set node to build response with only required fields

2. **Cache Static Data**: Store frequently used data in variables
   - **Why**: Reduce database queries
   - **How**: Use workflow variables or external cache (Redis)

## Reliability & Error Handling

### Retry Logic
1. **Sender Must Retry**: Webhook doesn't retry failed requests
   - **Why**: Webhook is passive receiver
   - **How**: Implement retry in sending application (exponential backoff)

2. **Return Appropriate Status Codes**: Help sender understand results
   - **Why**: Enables smart retry logic
   - **How**: Return 200 (success), 400 (bad request), 500 (server error)

### Error Recovery
1. **Use Try-Catch Pattern**: Wrap workflow in scope
   - **Why**: Catch errors, return meaningful responses
   - **How**: Use IF "Continue On Fail", check for errors

2. **Log Failed Requests**: Store for later reprocessing
   - **Why**: No data loss, audit trail
   - **How**: Write to database or file before processing

### Idempotency
1. **Use Idempotency Keys**: For create/update operations
   - **Why**: Safe to retry without duplicates
   - **How**: Extract unique ID from request, check if already processed

2. **Return Same Result for Duplicate Requests**: Cache results by request ID
   - **Why**: Prevents duplicate processing
   - **How**: Check database for existing result before processing

## Security Best Practices

### Endpoint Security
1. **Always Enable Authentication**: Never use "None" in production
   - **Why**: Prevent unauthorized access and abuse
   - **How**: Use Header Auth with strong random keys

2. **Use HTTPS Only**: Encrypt all webhook traffic
   - **Why**: Protect sensitive data and credentials
   - **How**: Configure SSL/TLS on N8N server

3. **Validate Webhook Signatures**: For third-party services
   - **Why**: Verify sender identity
   - **How**: Use Code node to validate HMAC signatures (Stripe, GitHub, etc.)

### Input Validation
1. **Sanitize All Input**: Clean and validate incoming data
   - **Why**: Prevent injection attacks
   - **How**: Use Set node to clean strings, validate formats

2. **Check Content-Type**: Verify request format
   - **Why**: Prevent malformed data processing
   - **How**: Access via `$json.headers['content-type']`

3. **Limit Payload Size**: Reject oversized requests
   - **Why**: Prevent DoS attacks
   - **How**: Configure max payload in N8N settings

### Monitoring & Logging
1. **Log All Webhook Calls**: Track requests for audit
   - **Why**: Security monitoring, debugging
   - **How**: Write to database with timestamp, IP, payload hash

2. **Alert on Anomalies**: Detect unusual patterns
   - **Why**: Early detection of attacks or issues
   - **How**: Monitor request rates, failed authentications

3. **Rotate Authentication Keys**: Change periodically
   - **Why**: Limit exposure if compromised
   - **How**: Implement key rotation schedule (quarterly)

## Workflow Design

### URL Structure
1. **Use Descriptive Paths**: Make URLs self-documenting
   - **Why**: Easier management and debugging
   - **How**: Use paths like /webhook/form-submissions, /webhook/payment-events

2. **Version Your APIs**: Include version in path
   - **Why**: Support breaking changes
   - **How**: /webhook/v1/users, /webhook/v2/users

3. **Use Production Webhooks**: For stable integrations
   - **Why**: URLs don't change
   - **How**: Enable "Production" mode in webhook node

### Response Design
1. **Return Consistent Format**: Use standard response structure
   - **Why**: Easier for clients to parse
   - **How**: Always return `{"success": true/false, "data": {}, "error": ""}`

2. **Include Request ID**: Return unique identifier
   - **Why**: Tracking and debugging
   - **How**: Generate UUID, return in response

3. **Set Appropriate Headers**: Content-Type, Cache-Control, etc.
   - **Why**: Proper HTTP semantics
   - **How**: Use "Respond to Webhook" node options

### Error Handling
1. **Return Detailed Errors in Development**: Help debug issues
   - **Why**: Faster development iteration
   - **How**: Include error messages and stack traces

2. **Return Generic Errors in Production**: Don't leak internal details
   - **Why**: Security
   - **How**: Return "Internal server error" without specifics
</best_practices>

<troubleshooting>
## Common Errors

### 404 Not Found

<error id="err-404" http_code="404">
- **Symptom**: "Webhook not found" or 404 error when calling URL
- **Cause**: Workflow is inactive, wrong URL, or webhook deleted
- **Immediate Fix**:
  1. Verify workflow is activated (toggle in N8N)
  2. Check webhook URL is correct
  3. Test with test webhook first
  4. Verify N8N instance is running
- **Prevention**:
  - Always activate workflow before sharing URLs
  - Use production webhooks for stability
  - Document webhook URLs
  - Monitor workflow active state
- **N8N Context**: Production webhooks only work when workflow active
</error>

### 401 Unauthorized

<error id="err-401" http_code="401">
- **Symptom**: "Unauthorized" or authentication failed
- **Cause**: Missing or incorrect authentication credentials
- **Immediate Fix**:
  1. Verify authentication is configured correctly
  2. Check header name matches (case-sensitive)
  3. Verify authentication value is correct
  4. Test with curl or Postman first
- **Prevention**:
  - Document authentication requirements
  - Use strong, unique keys
  - Test authentication before sharing
- **N8N Tool**: Test webhook in N8N editor
</error>

### 413 Payload Too Large

<error id="err-413" http_code="413">
- **Symptom**: "Payload too large" or request entity too large
- **Cause**: Request body exceeds N8N or server limits
- **Immediate Fix**:
  1. Increase max payload size in N8N settings
  2. Configure web server (nginx) to allow larger bodies
  3. Reduce payload size if possible
  4. Use multipart upload for large files
- **Prevention**:
  - Set appropriate limits for use case
  - Validate file sizes before upload
  - Use chunked uploads for large files
- **N8N Setting**: Configure in environment variables
</error>

### 504 Gateway Timeout

<error id="err-504" http_code="504">
- **Symptom**: "Gateway timeout" or request timeout
- **Cause**: Workflow execution exceeds timeout (120s default)
- **Immediate Fix**:
  1. Use "Respond to Webhook" node to reply immediately
  2. Move long processing after response
  3. Increase timeout in N8N settings
  4. Optimize workflow performance
- **Prevention**:
  - Always respond within 30 seconds
  - Use async processing for long tasks
  - Implement queue-based processing
- **N8N Pattern**: Respond → Continue processing
</error>

### Webhook URL Changes

<error id="err-custom-001" http_code="N/A">
**Error**: Test webhook URL changed after saving
- **Symptom**: Previously working test URL returns 404
- **Cause**: Test URLs regenerate on workflow save
- **Immediate Fix**:
  1. Copy new test URL from N8N editor
  2. Update sender with new URL
  3. Switch to production webhook for stable URLs
- **Prevention**:
  - Use production webhooks for integrations
  - Only use test webhooks during development
  - Document that test URLs are temporary
- **N8N Behavior**: Expected behavior, use production mode
</error>

### Binary Data Not Received

<error id="err-custom-002" http_code="N/A">
**Error**: File uploads not appearing in workflow
- **Symptom**: No `$binary` data in webhook trigger output
- **Cause**: Incorrect Content-Type, missing binary data handling
- **Immediate Fix**:
  1. Verify Content-Type is multipart/form-data
  2. Check file field name in form
  3. Ensure binary data option enabled
  4. Test with curl: `curl -F "file=@test.pdf" URL`
- **Prevention**:
  - Enable binary data in webhook settings
  - Document expected field names
  - Test file uploads before production
- **N8N Access**: Files available via `$binary.data`
</error>

## Diagnostic Steps

1. **Test with cURL**
   - Create sample request
   - Test authentication
   - Verify response
   - Check status codes

```bash
# Basic test
curl -X POST https://your-n8n.com/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# With authentication
curl -X POST https://your-n8n.com/webhook/test \
  -H "X-API-Key: your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

2. **Check N8N Execution Log**
   - View workflow execution history
   - Inspect input data
   - Review error messages
   - Check execution duration

3. **Verify Workflow State**
   - Confirm workflow is active
   - Check webhook configuration
   - Test in N8N editor first
   - Verify URL is correct

4. **Test Authentication**
   - Verify header name/value
   - Check case sensitivity
   - Test with Postman
   - Review sender configuration

5. **Monitor Server Logs**
   - Check N8N logs for errors
   - Review web server logs (nginx)
   - Check system resources (memory, CPU)
   - Verify no firewall blocks
</troubleshooting>

<related_docs>
## Documentation Structure

- **Response Handling**: Use "Respond to Webhook" node for custom responses
- **Best Practices**: Workflow design patterns and security guidance

## Related Nodes

- **[HTTP Request](./http-request.md)** - Make outbound API calls (opposite direction)
- **Respond to Webhook** - Send custom responses in webhook workflows
- **Wait** - Pause workflow for async operations
- **[Code](./code.md)** - Validate webhook signatures, parse data

## External Resources

- **Official N8N Webhook Docs**: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/
- **N8N Community**: https://community.n8n.io/
- **Webhook Security Guide**: https://docs.n8n.io/security/
- **Workflow Examples**: https://n8n.io/workflows?search=webhook
</related_docs>

<metadata_summary>
## Document Information

- **Last Updated**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 95% (Core functionality documented)
- **Validation Status**: Validated against N8N patterns
- **Next Review**: 2025-11-30
- **N8N Version**: Compatible with all recent versions
</metadata_summary>
