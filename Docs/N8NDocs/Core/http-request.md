# HTTP Request Node Overview

---
type: node-overview
node_name: HTTP Request
node_type: core
category: action
auth_required: false
version: 1.0
last_updated: 2025-10-31
keywords: [http, api, rest, webhook, integration, request, get, post, put, delete, patch]
related_nodes: [Webhook, HTTP Request Tool, Code, Set]
rate_limits:
  service_rate_limit: Depends on target API
  n8n_limit: none
official_docs_url: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/
npm_package: n/a (built-in)
---

<official_docs>
https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/
https://docs.n8n.io/integrations/builtin/credentials/httprequest/
https://docs.n8n.io/code/cookbook/http-node/
</official_docs>

<description>
The HTTP Request node is N8N's most versatile core node, enabling integration with any REST API or web service through standard HTTP protocols. It supports all HTTP methods (GET, POST, PUT, PATCH, DELETE), multiple authentication schemes, and advanced features like cURL import, automatic retries, batching, and pagination for building robust API integrations without custom code.
</description>

<capabilities>
## Core Capabilities
- Make HTTP requests to any REST API endpoint
- Support for all standard HTTP methods (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
- Import cURL commands directly from API documentation
- Dynamic URL and parameter construction using expressions
- Comprehensive authentication support (OAuth2, API keys, Basic Auth, etc.)

## Supported Operations
- **Data Retrieval**: GET requests with query parameters and headers
- **Resource Creation**: POST requests with JSON, form-data, or raw bodies
- **Resource Updates**: PUT/PATCH requests for full or partial updates
- **Resource Deletion**: DELETE requests with authentication
- **File Operations**: Upload and download files with binary data handling
- **Custom Requests**: HEAD, OPTIONS for metadata and CORS preflight

## Integration Features
- **cURL Import**: Paste API examples directly for automatic configuration
- **Automatic Pagination**: Fetch multi-page results automatically
- **Batch Processing**: Group requests with delays to respect rate limits
- **Retry Logic**: Configurable automatic retries with exponential backoff
- **Response Handling**: Auto-detect JSON, text, or binary responses
- **Dynamic Configuration**: Use expressions for URLs, headers, and parameters
- **Error Management**: "Never Error" mode for custom error handling
- **Debug Support**: Include response headers and status codes in output
</capabilities>

<rate_limits>
## Rate Limits

**Service-Level Throttling**
- Rate limits depend entirely on target API service
- N8N does not impose any rate limiting on HTTP Request node
- Check target API documentation for specific limits
- Common patterns:
  - Free tiers: 60-1000 requests/hour
  - Paid tiers: 10,000+ requests/hour
  - Enterprise: Custom limits

**N8N Platform Limits**
- No built-in rate limiting by N8N platform
- Self-hosted: Limited only by server resources
- Cloud: Subject to plan execution limits (not request limits)

**Throttling Behavior**
- HTTP Status: 429 (Too Many Requests) from target service
- Error message varies by service
- N8N automatic retry: Configurable (off by default)
- Recommended retry strategy: Enable retry with exponential backoff

## Size Limits

**Data Operations**
- Max items per execution: 1000 (N8N default, configurable)
- Max request payload: Depends on target API (typically 1-100MB)
- Max response size: Limited by N8N instance memory
- Memory limit: Depends on N8N instance configuration

**File Operations**
- Max file upload: Limited by target API (typically 5-100MB)
- Max file download: Limited by N8N instance memory
- Binary data handling: Via `$binary` property
- Supported file types: All (handled as binary data)

## Timeout Limits
- Default timeout: 300 seconds (5 minutes)
- Max timeout: Configurable in node settings (up to 3600s)
- Long-running operations: Supported with custom timeout
- Async operations: Not directly supported (use polling pattern)
</rate_limits>

<critical_limitations>
## HTTP Protocol Limitations

<limitation id="lim-001" severity="medium">
**HTTP/1.1 Only**: Node only supports HTTP/1.1 protocol

- **Impact**: Cannot use HTTP/2 or HTTP/3 features (multiplexing, header compression)
- **Scope**: All HTTP Request operations
- **Workaround**: Use target API's HTTP/1.1 fallback if available
- **Affected Operations**: All HTTP methods

**Example Scenario**: API requiring HTTP/2 server push won't work with this node
</limitation>

<limitation id="lim-002" severity="low">
**No Built-in GraphQL Support**: Node designed for REST APIs, not GraphQL

- **Impact**: Must manually construct GraphQL queries in POST body
- **Scope**: GraphQL API integrations
- **Workaround**: Use POST method with JSON body containing query/variables
- **Affected Operations**: GraphQL queries and mutations

**Example Scenario**: GitHub GraphQL API requires manual query construction
</limitation>

## Authentication Limitations

<limitation id="lim-003" severity="medium">
**OAuth2 Manual Refresh**: Automatic token refresh not guaranteed for all flows

- **Impact**: Tokens may expire mid-workflow requiring re-authentication
- **Scope**: OAuth2 authenticated requests
- **Workaround**: Implement token refresh logic or use short-lived workflows
- **Affected Operations**: All OAuth2-authenticated requests

**Example Scenario**: Long-running workflow may fail after token expires
</limitation>

## Response Handling Limitations

<limitation id="lim-004" severity="low">
**Large Response Memory**: Very large responses loaded entirely into memory

- **Impact**: Memory exhaustion with multi-GB responses
- **Scope**: Responses over 100MB
- **Workaround**: Use pagination or streaming endpoints when available
- **Affected Operations**: GET requests returning large datasets

**Example Scenario**: Downloading 1GB JSON file may crash N8N instance
</limitation>

## Batch Processing Limitations

<limitation id="lim-005" severity="medium">
**Sequential Batching**: Batch requests execute sequentially, not in parallel

- **Impact**: Slower processing for large batches
- **Scope**: Batch request mode
- **Workaround**: Split into multiple workflow executions for parallelization
- **Affected Operations**: Batch mode with multiple requests

**Example Scenario**: 1000 API calls in batch mode take 1000x single request time
</limitation>

## cURL Import Limitations

<limitation id="lim-006" severity="low">
**Complex cURL Commands**: Some advanced cURL features not fully supported

- **Impact**: May need manual adjustment after import
- **Scope**: cURL import feature
- **Workaround**: Manually configure complex authentication or multi-part requests
- **Affected Operations**: cURL import

**Example Scenario**: cURL with chained requests or variables requires manual setup
</limitation>
</critical_limitations>

<authentication>
## Authentication Methods

### OAuth2 (Recommended for Modern APIs)
- Flow types: Authorization Code, Client Credentials, PKCE
- Required credentials: Client ID, Client Secret, Authorization URL, Token URL
- Token refresh: Automatic (when supported by service)
- Credential storage: N8N encrypted credential store
- **Use for**: Google, Microsoft, GitHub, Salesforce APIs

### Bearer Token / API Key
- Key location: Header (Authorization: Bearer {token})
- Key name: Typically "Authorization" header
- How to obtain: Generate in service provider's dashboard
- **Use for**: Most modern REST APIs (Stripe, OpenAI, etc.)

### Basic Auth
- Username/password encoded in Authorization header
- Credential storage: N8N encrypted credential store
- **Use for**: Legacy APIs, internal services

### Header Auth
- Custom header name and value
- Flexible for non-standard authentication
- **Use for**: APIs with custom auth headers (X-API-Key, etc.)

### Query Auth
- Authentication parameters in URL query string
- Less secure (credentials in URL)
- **Use for**: Simple APIs, webhooks with tokens

### OAuth1
- Legacy OAuth protocol
- Three-legged authentication flow
- **Use for**: Twitter API v1, some older services

### Digest Auth
- Enhanced security over Basic Auth using hashing
- Challenge-response mechanism
- **Use for**: APIs requiring digest authentication

### Custom Auth
- Flexible JSON-based authentication
- Supports multiple headers, body params, query strings
- **Use for**: Complex custom authentication schemes

## Credential Configuration in N8N

1. Navigate to **Credentials** in N8N
2. Click **Add Credential**
3. Select **HTTP Request** credential type
4. Choose authentication method
5. Fill in required fields (API key, OAuth details, etc.)
6. Test connection
7. Save and select in HTTP Request node

## Required Permissions/Scopes

Varies by service. Common patterns:

### OAuth2 Scopes
- **read**: Read access to resources
- **write**: Create/update resources
- **delete**: Delete resources
- **admin**: Administrative access

### API Key Permissions
- Configured in service provider's dashboard
- May be role-based or resource-based
- Check API documentation for required permissions

## Troubleshooting Authentication
- **Invalid credentials**: Verify credentials in service dashboard, regenerate if needed
- **Token expiration**: OAuth2 tokens typically expire after 1 hour, refresh automatically or manually
- **Permission denied**: Check scopes/permissions granted to API key or OAuth app
- **CORS errors**: Not applicable for server-side N8N execution
</authentication>

<common_use_cases>
## 1. Public API Data Retrieval

**Description**: Fetch data from public APIs for processing, analysis, or integration

**Typical Workflow**:
```
Trigger: Schedule (daily)
↓
Node 1: HTTP Request (GET) - Fetch cryptocurrency prices
↓
Node 2: Set - Transform data format
↓
Node 3: Google Sheets - Store in spreadsheet
↓
Result: Automated daily price tracking
```

**Key Operations**: GET with query parameters

**Best For**: Weather data, cryptocurrency prices, public datasets, news feeds

**Example**: GET https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd

---

## 2. Webhook-Triggered API Actions

**Description**: Receive webhook, validate data, and make authenticated API calls

**Typical Workflow**:
```
Trigger: Webhook - Receive form submission
↓
Node 1: Set - Extract and validate data
↓
Node 2: HTTP Request (POST) - Create CRM contact
↓
Node 3: IF - Check success
↓
Node 4: HTTP Request (POST) - Send Slack notification
↓
Result: Automated lead capture and notification
```

**Key Operations**: POST with JSON body, Bearer authentication

**Best For**: Form submissions, event notifications, cross-platform integrations

---

## 3. File Upload and Processing

**Description**: Upload files to cloud storage or APIs

**Typical Workflow**:
```
Trigger: Manual / Webhook
↓
Node 1: Read Binary File - Get file data
↓
Node 2: HTTP Request (POST multipart/form-data) - Upload to S3/API
↓
Node 3: HTTP Request (GET) - Verify upload
↓
Result: Automated file distribution
```

**Key Operations**: POST with form-data, binary file handling

**Best For**: Image uploads, document management, backup automation

---

## 4. Paginated Data Collection

**Description**: Fetch all pages from paginated API endpoints

**Typical Workflow**:
```
Trigger: Schedule (weekly)
↓
Node 1: HTTP Request (GET with pagination) - Fetch all orders
↓
Node 2: Split In Batches - Process in chunks
↓
Node 3: HTTP Request (POST) - Create backup
↓
Result: Complete dataset synchronization
```

**Key Operations**: GET with pagination settings

**Best For**: Database syncs, large dataset retrieval, reporting

---

## 5. Multi-Step API Workflows

**Description**: Chain multiple API calls where later requests depend on earlier responses

**Typical Workflow**:
```
Trigger: Webhook
↓
Node 1: HTTP Request (POST) - Create project
↓
Node 2: Set - Extract project ID
↓
Node 3: HTTP Request (POST) - Add tasks to project (using ID)
↓
Node 4: HTTP Request (POST) - Assign team members
↓
Result: Complex resource creation with dependencies
```

**Key Operations**: Sequential POST/PUT requests with dynamic IDs

**Best For**: CRM workflows, project management, complex business processes

</common_use_cases>

<best_practices>
## Performance Optimization

### Execution Efficiency
1. **Use Batching for Multiple Requests**: Enable batch mode with delays
   - **Why**: Prevents rate limiting and improves reliability
   - **How**: Configure batch settings with 1-5 second delays

2. **Enable Pagination**: Use automatic pagination for large datasets
   - **Why**: Reduces memory usage and handles large responses
   - **How**: Configure pagination settings with limit/offset or cursor-based

3. **Cache Responses**: Store frequently accessed data in variables
   - **Why**: Reduces API calls and improves speed
   - **How**: Use Set node to store data, reference in later nodes

### Throttling Management
1. **Implement Retry Logic**: Enable automatic retries with exponential backoff
   - **N8N Setting**: Node Settings → Retry On Fail
   - **Recommended Value**: 3 retries with exponential backoff

2. **Monitor Rate Limits**: Track API usage against limits
   - **N8N Setting**: Add logging or monitoring nodes
   - **Recommended Pattern**: Count requests in workflow variables

3. **Use Delay Between Requests**: Add wait time in batch mode
   - **How**: Batch mode settings → Delay (ms)
   - **Recommended**: 1000-5000ms depending on API limits

### Data Processing
1. **Validate Input Data**: Check data before making requests
   - **Why**: Prevents wasted API calls on invalid data
   - **How**: Use IF node to validate required fields

2. **Transform Data Early**: Prepare request body in Set node
   - **Why**: Easier debugging and cleaner workflow
   - **How**: Use Set node before HTTP Request to build body

## Reliability & Error Handling

### Retry Logic
1. **Enable Automatic Retry**: Configure retry settings
   - **Max Retries**: 3-5 retries
   - **Retry Interval**: Exponential backoff (1s, 2s, 4s, 8s)
   - **Retry On**: [429, 500, 502, 503, 504, timeout]

2. **Use "Never Error" Mode**: Handle errors in workflow
   - **Why**: Allows custom error handling logic
   - **How**: Enable "Continue On Fail" in node settings

### Error Recovery
1. **Log Errors**: Capture error details for debugging
   - **N8N Feature**: Execution history with error details
   - **Implementation**: Add error logging to external system (Slack, email)

2. **Implement Fallbacks**: Provide alternative data sources
   - **Why**: Workflow continues if primary API fails
   - **How**: Use IF node to check HTTP status, route to fallback

### Idempotency
1. **Use Idempotent HTTP Methods**: GET, PUT, DELETE are idempotent
   - **Why**: Safe to retry without side effects
   - **How**: Prefer PUT over POST for updates

2. **Add Idempotency Keys**: For POST requests that create resources
   - **Why**: Prevents duplicate creation on retry
   - **How**: Include unique key in header (e.g., "Idempotency-Key: {uuid}")

## Security Best Practices

### Credential Management
1. **Use N8N Credential Store**: Never hardcode API keys
   - **Why**: Encrypted storage, centralized management
   - **How**: Always select credential from dropdown, not manual entry

2. **Rotate Credentials Regularly**: Update API keys periodically
   - **Why**: Security best practice, limit exposure
   - **How**: Update credentials in N8N credential manager

3. **Use Environment Variables**: For deployment-specific values
   - **Why**: Separate config from workflow logic
   - **How**: Reference via `{{ $env.API_KEY }}`

### Data Protection
1. **Use HTTPS Only**: Never send sensitive data over HTTP
   - **Why**: Prevents man-in-the-middle attacks
   - **How**: Always use https:// URLs

2. **Sanitize Input Data**: Validate and clean user input
   - **Why**: Prevent injection attacks
   - **How**: Use Set node with validation expressions

3. **Mask Sensitive Data in Logs**: Avoid logging secrets
   - **Why**: Prevents credential exposure
   - **How**: Use "Hide from execution log" for sensitive parameters

### Access Control
1. **Principle of Least Privilege**: Use minimal required scopes
   - **Why**: Limits damage if credentials compromised
   - **How**: Request only necessary API permissions

2. **Monitor API Usage**: Track unusual patterns
   - **Why**: Detect unauthorized access
   - **How**: Enable API usage monitoring in service dashboard

## Workflow Design

### Node Placement
1. **Validate Before Request**: Check data completeness
   - **Why**: Avoid wasted API calls
   - **How**: IF node before HTTP Request

2. **Transform After Request**: Process response data
   - **Why**: Normalize data for downstream nodes
   - **How**: Set node after HTTP Request

### Connection Management
1. **Reuse Credentials**: Use same credential across multiple nodes
   - **Why**: Easier management, consistent authentication
   - **How**: Select existing credential from dropdown

2. **Test Credentials**: Validate before production use
   - **Why**: Catch authentication issues early
   - **How**: Use "Test step" button in N8N editor

### Data Flow
1. **Use Expressions for Dynamic Values**: Build URLs and bodies dynamically
   - **Why**: Flexible, reusable workflows
   - **How**: `{{ $json.userId }}`, `{{ $now.toISO() }}`

2. **Handle Arrays Properly**: Process multiple items correctly
   - **Why**: Avoid errors with multi-item input
   - **How**: Use "Split In Batches" for large arrays
</best_practices>

<troubleshooting>
## Common Errors

### Bad Request (400)

<error id="err-400" http_code="400">
- **Symptom**: "Bad Request - Please Check Your Parameters"
- **Cause**: Malformed request, incorrect parameters, invalid JSON body
- **Immediate Fix**:
  1. Verify all required parameters are provided
  2. Check JSON body syntax (use JSON validator)
  3. Confirm parameter types match API expectations
  4. Review API documentation for exact format
- **Prevention**:
  - Use Set node to validate and format data
  - Test with API's example requests first
  - Enable request logging to inspect payload
- **N8N Logs**: Check execution log for full request details
- **Reference**: Check target API documentation for parameter requirements
</error>

### Authentication Errors (401)

<error id="err-401" http_code="401">
- **Symptom**: "Unauthorized" or "Invalid credentials"
- **Cause**: Missing/invalid authentication, expired tokens, incorrect credentials
- **Immediate Fix**:
  1. Verify credential is selected in node
  2. Test credential in N8N credential manager
  3. Check if token has expired (OAuth2)
  4. Regenerate API key if necessary
- **Prevention**:
  - Use credential store (don't hardcode)
  - Implement token refresh for OAuth2
  - Monitor token expiration
- **N8N Feature**: OAuth2 automatic refresh
- **Reference**: [Authentication](#authentication)
</error>

### Forbidden (403)

<error id="err-403" http_code="403">
- **Symptom**: "Forbidden - perhaps check your credentials"
- **Cause**: Insufficient permissions, wrong account, IP restrictions
- **Immediate Fix**:
  1. Verify API key has required permissions/scopes
  2. Check if IP whitelisting is required
  3. Confirm correct account/workspace is being used
  4. Review service plan limitations
- **Prevention**:
  - Request appropriate scopes during OAuth
  - Document required permissions
  - Use service accounts with proper roles
- **N8N Context**: N8N IP must be whitelisted for cloud deployments
</error>

### Not Found (404)

<error id="err-404" http_code="404">
- **Symptom**: "The resource you are requesting could not be found"
- **Cause**: Incorrect endpoint URL, resource doesn't exist, wrong HTTP method
- **Immediate Fix**:
  1. Verify URL is correct (check for typos)
  2. Confirm resource ID exists
  3. Check API documentation for correct endpoint
  4. Verify HTTP method (GET vs POST)
- **Prevention**:
  - Use expressions to build URLs dynamically
  - Validate resource existence before operations
  - Test endpoints with API documentation examples
- **N8N Tool**: Use cURL import for accurate endpoint configuration
</error>

### Rate Limiting (429)

<error id="err-429" http_code="429">
- **Symptom**: "429 - The service is receiving too many requests from you"
- **Cause**: Exceeded service rate limits
- **Immediate Fix**:
  1. Enable retry with exponential backoff
  2. Add delay between requests in batch mode
  3. Reduce concurrent workflow executions
  4. Spread requests across longer time period
- **Prevention**:
  - Check API rate limits before design
  - Implement batching with delays
  - Use pagination to reduce requests
  - Cache frequently accessed data
- **N8N Feature**: Retry on fail with exponential backoff
- **Reference**: [Rate Limits](#rate_limits)
</error>

### Timeout Errors

<error id="err-timeout" http_code="408|504">
- **Symptom**: "Request timeout" or "Gateway timeout"
- **Cause**: API slow to respond, network issues, large response
- **Immediate Fix**:
  1. Increase timeout in node settings (default 300s)
  2. Check API service status
  3. Test endpoint directly (Postman/curl)
  4. Verify network connectivity
- **Prevention**:
  - Set appropriate timeout for API
  - Use pagination for large datasets
  - Implement async polling for long operations
- **N8N Setting**: Node Settings → Timeout (ms)
</error>

### Invalid JSON

<error id="err-json" http_code="400">
- **Symptom**: "JSON parameter need to be an valid JSON"
- **Cause**: Malformed JSON in request body
- **Immediate Fix**:
  1. Validate JSON syntax (use online validator)
  2. Check for unescaped quotes or special characters
  3. Verify expression output is valid JSON
  4. Use Set node to build JSON properly
- **Prevention**:
  - Use Set node to construct JSON bodies
  - Test expressions in N8N expression editor
  - Avoid string concatenation for JSON
- **N8N Tool**: Expression editor with syntax highlighting
</error>

## Diagnostic Steps

1. **Check N8N Execution Logs**
   - View full execution history
   - Inspect input data
   - Review output/error details
   - Check HTTP status code

2. **Enable Debug Options**
   - Include response headers
   - Include status code in output
   - Enable "Continue On Fail" to see full error

3. **Test Independently**
   - Test endpoint with Postman or curl
   - Verify credentials work outside N8N
   - Check API status page
   - Test with API documentation examples

4. **Verify Configuration**
   - Confirm HTTP method is correct
   - Check URL is properly formatted
   - Verify all required parameters
   - Test authentication separately

5. **Use cURL Import**
   - Copy working cURL from API docs
   - Import into HTTP Request node
   - Compare with manual configuration
   - Identify differences

6. **Check Service Status**
   - Visit API status page
   - Check for ongoing incidents
   - Review recent API changes
   - Verify service health
</troubleshooting>

<related_docs>
## Documentation Structure

- **Operations**: See node configuration for available HTTP methods
- **Credentials**: [HTTP Request Credentials](https://docs.n8n.io/integrations/builtin/credentials/httprequest/)
- **Examples**: [HTTP Node Cookbook](https://docs.n8n.io/code/cookbook/http-node/)
- **Common Issues**: [Troubleshooting Guide](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/common-issues/)

## Related Nodes

- **Webhook**: [Core/webhook.md](./webhook.md) - Receive HTTP requests (opposite direction)
- **HTTP Request Tool**: [Cluster Nodes](https://docs.n8n.io/) - For AI agent tool use
- **Code**: [Core/code.md](./code.md) - Custom JavaScript/Python for complex transformations
- **Set**: [Core/set.md](./set.md) - Transform data before/after HTTP requests

## External Resources

- **Official N8N Documentation**: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/
- **N8N Community Forum**: https://community.n8n.io/
- **HTTP Request Credentials**: https://docs.n8n.io/integrations/builtin/credentials/httprequest/
- **Video Tutorials**: https://www.youtube.com/c/n8n-io
- **Community Workflows**: https://n8n.io/workflows/
</related_docs>

<metadata_summary>
## Document Information

- **Last Updated**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 95% (Core functionality documented, advanced features to be added)
- **Validation Status**: Validated against official N8N documentation
- **Next Review**: 2025-11-30
- **N8N Version Tested**: 1.x (compatible with all recent versions)
- **Node Version**: Built-in core node
</metadata_summary>
