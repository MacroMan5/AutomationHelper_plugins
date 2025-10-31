# HTTP Connector

## Overview
**Triggers**: 3
**Actions**: 3

The HTTP connector enables integration with external web services and APIs through HTTP requests and webhooks.

## Actions

### HTTP
**Description**: Sends HTTP request to any web service
**Parameters**:
- Method (required): GET, POST, PUT, PATCH, DELETE, HEAD
- URI (required) - Full URL
- Headers (optional) - Key-value pairs
- Queries (optional) - URL parameters
- Body (optional) - Request payload
- Authentication (optional) - Auth configuration
- Cookie (optional)
- Retry Policy (optional)

**Returns**:
- Status code
- Headers
- Body

**Authentication Types**:
- None
- Basic
- Client Certificate
- Active Directory OAuth
- Raw (custom headers)
- Managed Identity

**Use Cases**:
- REST API calls
- External service integration
- Custom connectors alternative
- Webhook calls

**Examples**:

**GET Request**:
```
Method: GET
URI: https://api.example.com/users/123
Headers: {
  "Accept": "application/json"
}
```

**POST Request**:
```
Method: POST
URI: https://api.example.com/users
Headers: {
  "Content-Type": "application/json"
}
Body: {
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Best Practices**:
- Store sensitive data in Azure Key Vault
- Use managed identity when possible
- Implement retry logic for transient failures
- Parse response with Parse JSON
- Handle different status codes appropriately
- Set appropriate timeouts

---

### HTTP + Swagger
**Description**: HTTP action with OpenAPI (Swagger) definition
**Parameters**:
- Swagger Endpoint (required) - OpenAPI spec URL
- Operation (required) - Selected from spec
- Parameters - Dynamic based on spec

**Benefits**:
- Auto-generated parameters
- Type validation
- Documentation integration
- Easier than raw HTTP

**Use Cases**:
- Well-documented APIs
- OpenAPI/Swagger services
- Type-safe API calls

**Best Practices**:
- Verify Swagger spec is accessible
- Update when API changes
- Prefer over raw HTTP when available

---

### HTTP Webhook
**Description**: Subscribe and unsubscribe to webhook events
**Parameters**:
- Subscribe Method (required) - HTTP method for subscription
- Subscribe URI (required) - Webhook registration URL
- Subscribe Body (optional) - Registration payload
- Unsubscribe Method (optional)
- Unsubscribe URI (optional)

**Flow**:
1. Flow subscribes to webhook
2. Waits for webhook callback
3. Processes webhook data
4. Unsubscribes after flow completes

**Use Cases**:
- Event-driven automation
- Real-time notifications
- Async operation completion
- Third-party event processing

**Example**:
```
Subscribe:
  Method: POST
  URI: https://api.example.com/webhooks/subscribe
  Body: {
    "callbackUrl": "@{listCallbackUrl()}",
    "events": ["user.created"]
  }

Unsubscribe:
  Method: DELETE
  URI: https://api.example.com/webhooks/@{triggerBody()?['subscriptionId']}
```

**Best Practices**:
- Always implement unsubscribe
- Validate webhook payload
- Use authentication for callbacks
- Handle duplicate events

---

## Triggers

### When an HTTP request is received
**Description**: Creates a webhook URL to receive HTTP requests
**Parameters**:
- Request Body JSON Schema (optional) - For payload parsing
- Method (optional) - GET, POST, PUT, etc.

**Generates**: Unique HTTP POST URL

**Returns**:
- Request headers
- Request body
- Request parameters

**Use Cases**:
- External system integration
- Custom webhooks
- Third-party event reception
- API endpoints for flows

**Security Notes**:
- URL contains security token
- Regenerates on save
- No built-in authentication
- Consider Azure AD or API Management for security

**Example Schema**:
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "email": {"type": "string"},
    "id": {"type": "integer"}
  }
}
```

**Best Practices**:
- Define schema for dynamic content
- Validate incoming payload
- Implement security checks
- Return Response action
- Log received data for debugging

---

### When an HTTP webhook request is received
**Description**: Long-running webhook trigger
**Parameters**:
- JSON Schema (optional)

**Use Cases**:
- Long-running async operations
- Event subscriptions
- Real-time notifications

---

### HTTP request trigger (authenticated)
**Description**: Authenticated HTTP endpoint
**Parameters**:
- Authentication type
- Schema

**Use Cases**:
- Secure API endpoints
- Authenticated webhooks

---

## Response Action

### Response (from Request connector)
**Description**: Returns HTTP response to webhook caller
**Parameters**:
- Status Code (required) - e.g., 200, 400, 500
- Headers (optional)
- Body (optional)

**Use Cases**:
- Acknowledge receipt
- Return processing result
- Error responses
- Sync request-response patterns

**Example**:
```
Status Code: 200
Headers: {
  "Content-Type": "application/json"
}
Body: {
  "status": "success",
  "id": "12345",
  "message": "Request processed"
}
```

**Best Practices**:
- Return response early in flow
- Use appropriate status codes
- Include correlation ID
- Provide meaningful error messages

---

## Common HTTP Patterns

### Pattern 1: REST API Call
```
HTTP (GET) → Parse JSON → Process data
```

### Pattern 2: Authenticated API
```
Compose (build auth header) → HTTP (with headers) → Parse JSON
```

### Pattern 3: Retry Logic
```
Do until (success OR max retries)
  → HTTP action
  → Condition (check status code)
  → Delay (if retry needed)
```

### Pattern 4: Webhook Receiver
```
When HTTP request received → Parse JSON → Validate → Process → Response
```

### Pattern 5: Paginated API
```
Initialize page variable → Do until (no more pages)
  → HTTP GET (with page parameter)
  → Parse JSON
  → Process items
  → Increment page
```

## HTTP Status Code Handling

### Success (2xx)
- 200 OK - Request successful
- 201 Created - Resource created
- 202 Accepted - Async processing started
- 204 No Content - Success with no response body

### Client Errors (4xx)
- 400 Bad Request - Invalid request
- 401 Unauthorized - Authentication required
- 403 Forbidden - Insufficient permissions
- 404 Not Found - Resource doesn't exist
- 429 Too Many Requests - Rate limited

### Server Errors (5xx)
- 500 Internal Server Error - Server error
- 502 Bad Gateway - Upstream error
- 503 Service Unavailable - Temporary unavailable
- 504 Gateway Timeout - Timeout

## Best Practices

### Security
1. Never hardcode credentials
2. Use Azure Key Vault for secrets
3. Implement authentication on webhooks
4. Validate webhook payloads
5. Use managed identity when possible
6. Limit webhook URL exposure

### Reliability
1. Implement retry logic with exponential backoff
2. Handle all expected status codes
3. Set appropriate timeouts
4. Log requests and responses
5. Use idempotency keys for POST requests
6. Handle rate limiting (429 responses)

### Performance
1. Use async patterns when possible
2. Implement pagination for large datasets
3. Cache responses when appropriate
4. Use webhooks instead of polling
5. Minimize payload size

### Error Handling
1. Parse error responses
2. Log error details
3. Return meaningful error messages
4. Implement circuit breaker for failing APIs
5. Alert on critical failures

### Debugging
1. Log request and response bodies
2. Use correlation IDs
3. Test with Postman/curl first
4. Check firewall/network policies
5. Verify SSL/TLS certificates
6. Monitor API quotas

## Common Pitfalls

1. **Hardcoded secrets** - Use secure storage
2. **No retry logic** - Implement for transient failures
3. **Ignoring status codes** - Handle all responses
4. **No timeout** - Set appropriate limits
5. **Unsecured webhooks** - Add authentication
6. **Not parsing responses** - Use Parse JSON
7. **Missing error handling** - Wrap in Scope with error path
