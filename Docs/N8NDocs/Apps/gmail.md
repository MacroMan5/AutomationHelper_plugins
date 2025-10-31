---
type: node-overview
node_name: Gmail
node_type: app
category: both
auth_required: true
version: 1.0
last_updated: 2025-10-31
keywords: [email, gmail, send, search, message, inbox, attachment, label, thread, automation, communication]
related_nodes: [Google Drive, HTTP Request, Set]
rate_limits:
  service_rate_limit: 250 requests per second per user (varies by operation)
  n8n_limit: none (N8N doesn't impose limits)
official_docs_url: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/
npm_package: n8n-nodes-base
---

<official_docs>
https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/
https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/message-operations/
https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/draft-operations/
https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/label-operations/
https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/thread-operations/
</official_docs>

<description>
The Gmail node provides comprehensive email automation capabilities for N8N workflows. It enables sending emails, searching messages, managing labels, handling drafts, and organizing threads without leaving N8N. Perfect for email notifications, automated responses, inbox automation, and email-based workflow triggers.
</description>

<capabilities>
## Core Capabilities
- **Send Messages**: Compose and send emails with attachments
- **Search Messages**: Find emails by subject, sender, date, and content
- **Read Messages**: Retrieve full message content and metadata
- **Delete Messages**: Remove unwanted emails
- **Manage Labels**: Create, apply, and remove email labels/tags
- **Draft Management**: Create, update, and send drafts
- **Thread Organization**: Manage email conversations and threads
- **Modify Messages**: Change message properties (mark as read, star, etc.)

## Supported Operations
- **Send**: Compose and send email messages
- **Get**: Retrieve specific message details
- **Search**: Find messages by query criteria
- **Delete**: Remove messages from mailbox
- **Create Draft**: Create email draft
- **Update Draft**: Modify draft content
- **Send Draft**: Send previously created draft
- **Add Label**: Apply labels to messages
- **Create Label**: Create new label/category
- **Remove Label**: Remove label from messages
- **Trash/Restore**: Move messages to/from trash
- **Mark As Read/Unread**: Change message read status

## Integration Features
- **OAuth2 Authentication**: Secure credential-based access
- **Attachment Support**: Send files as attachments
- **HTML Email Support**: Send formatted emails
- **Reply-To Configuration**: Set custom reply addresses
- **CC/BCC Support**: Send to multiple recipients
- **Search Filters**: Advanced Gmail search syntax
- **Batch Operations**: Process multiple emails
- **Thread Management**: Handle email conversations
</capabilities>

<rate_limits>
## Rate Limits

**Service-Level Throttling**
- **250 requests per second** per user (varies by operation)
- **Send operations**: 100 emails per day for new users (5,000+ with verified account)
- Throttling scope: Per user account
- Retry-After header: Yes
- N8N built-in retry: Yes

**Operation-Specific Limits**
- **Send Email**: 100-5,000 per day depending on account age/reputation
- **Search/Get**: Standard rate limit (250 req/sec)
- **Modify/Delete**: Standard rate limit applies
- **Label Operations**: Standard rate limit applies

**N8N Platform Limits**
- No built-in rate limiting by N8N platform
- Self-hosted: Limited by server resources
- Cloud: Respects Gmail API quotas

**Throttling Behavior**
- HTTP Status: 429 (Too Many Requests) or 403 (Quota exceeded)
- Error message: "Rate limit exceeded" or "Daily limit exceeded"
- N8N automatic retry: Yes (configurable)
- Recommended retry strategy: Exponential backoff with longer delays

## Size Limits

**Email Operations**
- Max email size: **25MB** (including attachments)
- Max attachment size: **25MB per attachment**
- Max total attachments per email: **Unlimited in count**, but subject to total email size
- Max recipients per email: **500** (combined To, CC, BCC)
- Max subject line length: **998 characters**
- Max email body length: **No explicit limit**, but practical limit around 25MB

**Storage Operations**
- Max labels per account: **250**
- Max labels per message: **250**
- Max trash retention: **30 days** before permanent deletion

## Timeout Limits
- Default timeout: **300 seconds** (N8N default)
- Max timeout: **600 seconds** (configurable)
- Send operation timeout: **60 seconds** (Google API limit)
- Search operations: **May take longer for large mailboxes**
</rate_limits>

<critical_limitations>
## Send Limitations

<limitation id="lim-001" severity="critical">
**Send Rate Quota**: New accounts have strict daily sending limits

- **Impact**: Workflows that send bulk emails fail after daily quota
- **Scope**: Send Message operations
- **Workaround**: Verify account, request higher quota from Google, or spread sends over time
- **Affected Operations**: Send Message

**Example Scenario**: New account limited to 100 sends/day; bulk notification workflow fails after 100 emails
</limitation>

<limitation id="lim-002" severity="high">
**Attachment Size Limitations**: Large files cannot be attached

- **Impact**: Cannot send files >25MB or emails >25MB total
- **Scope**: Send Message with attachments
- **Workaround**: Use Google Drive link sharing instead of attachment, compress files
- **Affected Operations**: Send Message with attachments

**Example Scenario**: Attempting to send 50MB video file as attachment fails
</limitation>

<limitation id="lim-003" severity="high">
**Recipient Count Limits**: Cannot send to too many recipients

- **Impact**: Mass emails to >500 recipients must be split
- **Scope**: Send Message operations
- **Workaround**: Split into multiple sends using Split In Batches node
- **Affected Operations**: Send Message

**Example Scenario**: Attempting to CC 1000 people fails
</limitation>

## Search & Retrieval

<limitation id="lim-004" severity="high">
**Search Latency**: Newly received emails may not appear in search immediately

- **Impact**: Workflows searching for just-received emails may not find them
- **Scope**: Search Message operations
- **Workaround**: Add delay before search, or use direct message ID if known
- **Affected Operations**: Search, Get Message

**Example Scenario**: Email received 5 seconds ago not yet searchable
</limitation>

<limitation id="lim-005" severity="medium">
**Search Result Pagination**: Cannot get full history in single operation

- **Impact**: Large result sets must be paginated
- **Scope**: Search operations returning >100 results
- **Workaround**: Implement pagination logic or date range filtering
- **Affected Operations**: Search

**Example Scenario**: Searching for all emails from 2024 returns 1000+ results, need pagination
</limitation>

## Authentication & Credentials

<limitation id="lim-006" severity="critical">
**OAuth2 Token Expiration**: OAuth tokens expire and require refresh

- **Impact**: Long-running workflows may encounter token errors
- **Scope**: All OAuth2-authenticated operations
- **Workaround**: N8N automatically refreshes tokens if refresh token available
- **Affected Operations**: All operations

**Example Scenario**: Scheduled workflow running for 8+ hours encounters expired token
</limitation>

<limitation id="lim-007" severity="high">
**No Service Account Direct Send**: Service accounts cannot send emails directly

- **Impact**: Automated sending requires user OAuth2 or domain admin
- **Scope**: Service account authentication with Send operations
- **Workaround**: Use OAuth2 with personal account, or implement admin API
- **Affected Operations**: Send Message

**Example Scenario**: Service account workflow cannot send notification emails
</limitation>

## Data Limitations

<limitation id="lim-008" severity="medium">
**Deleted Email Recovery**: Emails in trash deleted after 30 days permanently

- **Impact**: No way to recover permanently deleted emails
- **Scope**: Deleted message operations
- **Workaround**: Archive instead of delete, or implement backup before delete
- **Affected Operations**: Delete Message

**Example Scenario**: Workflow deletes email, but it's permanently removed after 30 days
</limitation>

<limitation id="lim-009" severity="low">
**Special Character Encoding**: Some special characters may be encoded in subject/body

- **Impact**: Email display or searching may be affected
- **Scope**: Send/Search operations with special characters
- **Workaround**: Use UTF-8 encoding, test with Set node
- **Affected Operations**: Send, Search

**Example Scenario**: Emoji in subject line displays as encoding
</limitation>
</critical_limitations>

<authentication>
## Authentication Methods

### OAuth2 (Recommended)
- Flow type: Authorization Code
- Required credentials: Google account with Gmail access
- Token refresh: Automatic (N8N manages refresh tokens)
- Credential storage: N8N encrypted credential store

**Scopes Required**:
- `https://www.googleapis.com/auth/gmail.send` (Send emails only)
- `https://www.googleapis.com/auth/gmail.modify` (Full Gmail access - recommended)
- `https://www.googleapis.com/auth/gmail.readonly` (Read-only access)

### Service Account (Limited Use)
- Authentication type: Private key
- Use case: Automated access only (cannot send as user)
- Limitations: Domain admin required to send on behalf of users
- Credential storage: N8N encrypted credential store

## Credential Configuration in N8N

1. Navigate to **Credentials** in N8N
2. Click **Add Credential**
3. Select **Gmail**
4. Choose authentication method:
   - **OAuth2**: Click "Connect my account" and follow Google OAuth flow
   - Grant access when prompted (select appropriate scopes)
5. N8N stores token securely
6. Credential status shows "Connected"
7. Save credential

## Required Permissions/Scopes

### Gmail Permissions
- **Send Emails** (`gmail.send` scope): Send on behalf of user
- **Modify Gmail** (`gmail.modify` scope): Read, compose, send, delete emails; manage labels
- **Read Gmail** (`gmail.readonly` scope): Read-only access (for read/search only)

## Troubleshooting Authentication
- **"Invalid credentials" or "Unauthorized"**:
  - Check Gmail account is accessible
  - Verify Google account allows less secure apps (if needed)
  - Re-authenticate credential

- **"Token expiration"**:
  - N8N handles automatically; if persists, update credential
  - Check Google account hasn't revoked app access

- **"Permission denied" on Send**:
  - Verify credential has `gmail.send` scope
  - Account must not have restrictions on automated sending
  - Check Google account sending settings
</authentication>

<common_use_cases>
## 1. Automated Email Notifications

**Description**: Send automated emails when specific events occur in your workflow

**Typical Workflow**:
```
Trigger: Webhook (Customer action)
↓
Node 1: Set - Prepare email content
↓
Node 2: Gmail - Send notification email
↓
Node 3: Log - Record notification sent
↓
Result: Customer receives automated notification
```

**Key Operations**: [Send](#)

**Best For**: Alert notifications, confirmation emails, order updates

---

## 2. Email-Based Form Processing

**Description**: Receive emails, extract data, and process submissions

**Typical Workflow**:
```
Trigger: Gmail - Search for new emails
↓
Node 1: Gmail - Get message details
↓
Node 2: Code - Parse email content and attachments
↓
Node 3: HTTP Request - Submit data to system
↓
Node 4: Gmail - Add processed label
↓
Result: Email data extracted and processed
```

**Key Operations**: [Search](#), [Get](#), [Add Label](#)

**Best For**: Email form processing, customer inquiries, support tickets

---

## 3. Inbox Automation and Organization

**Description**: Automatically organize, label, and archive emails

**Typical Workflow**:
```
Trigger: Schedule (Daily)
↓
Node 1: Gmail - Search for unread emails
↓
Node 2: IF - Check sender or subject
↓
Node 3: Gmail - Add appropriate label
↓
Node 4: Gmail - Archive if processed
↓
Result: Inbox automatically organized
```

**Key Operations**: [Search](#), [Add Label](#)

**Best For**: Inbox management, email organization, spam filtering

---

## 4. Email Reply Automation

**Description**: Monitor inbox and automatically reply to specific emails

**Typical Workflow**:
```
Trigger: Gmail - Search for unanswered emails
↓
Node 1: IF - Check if reply needed
↓
Node 2: Gmail - Send reply
↓
Node 3: Gmail - Mark as answered/label
↓
Result: Emails automatically replied
```

**Key Operations**: [Search](#), [Send](#), [Add Label](#)

**Best For**: FAQ handling, order confirmations, auto-responders

---

## 5. Data Collection via Email Attachments

**Description**: Monitor for emails with attachments and process the files

**Typical Workflow**:
```
Trigger: Gmail - Search for emails with attachments
↓
Node 1: Gmail - Get message with attachment
↓
Node 2: Google Drive - Upload attachment
↓
Node 3: Code - Process file
↓
Node 4: Gmail - Send confirmation
↓
Result: Files collected and processed
```

**Key Operations**: [Search](#), [Get](#), [Send](#)

**Best For**: File collection, data import, document processing
</common_use_cases>

<best_practices>
## Performance Optimization

### Execution Efficiency
1. **Use Targeted Searches**: Narrow search scope with date ranges and filters
   - **Why**: Reduces result set and processing time
   - **How**: Use Gmail search syntax (from:, to:, subject:, before:, after:)

2. **Batch Email Processing**: Process multiple emails efficiently
   - **Why**: Reduces API calls and workflow overhead
   - **How**: Use Split In Batches node to handle multiple search results

3. **Implement Smart Filtering**: Filter at query level, not post-retrieval
   - **Why**: Reduces data transfer
   - **How**: Use Gmail search operators instead of retrieving all emails

### Throttling Management
1. **Enable Automatic Retry**: Configure in node settings
   - **N8N Setting**: Node settings → Retry settings
   - **Recommended Value**: 3-5 retries with exponential backoff (longer delays for send)

2. **Respect Send Quota**: Distribute sends over time
   - **How**: Implement delays between batch sends
   - **Strategy**: For bulk sends, space across multiple days if possible

### Data Processing
1. **Pre-format Email Content**: Use Set node before sending
   - **Why**: Ensures HTML/text formatting is correct
   - **How**: Build email body using Set node expressions

2. **Validate Recipients**: Check email format before sending
   - **Why**: Prevent send failures
   - **How**: Use code or IF node to validate email addresses

## Reliability & Error Handling

### Retry Logic
1. **Enable Automatic Retry**: Configure retry for send operations
   - **Max Retries**: 5 (for send operations; longer delays recommended)
   - **Retry Interval**: 5000ms for send, 2000ms for others (exponential)
   - **Retry On**: [429, 500, 502, 503, 504, "quota"]

2. **Use Error Workflow**: Create dedicated error handling
   - **Why**: Capture send failures and notify
   - **How**: Set up "Error Workflow" in N8N settings

### Error Recovery
1. **Log Failed Sends**: Track what emails failed to send
   - **Why**: Manual retry or investigation
   - **How**: Use Set node to log failed emails with reasons

2. **Implement Fallback Notifications**: Alert on send failures
   - **Why**: Ensure critical notifications aren't silently lost
   - **How**: Use Error Trigger to send notification of failure

### Idempotency
1. **Use Email References**: Track sent emails to prevent duplicates
   - **Why**: Prevent sending same email twice
   - **How**: Record message-id or use labels to mark sent

## Security Best Practices

### Credential Management
1. **Use N8N Credential Store**: Never hardcode credentials or email addresses
   - **Why**: Encrypted storage, centralized management
   - **How**: Always use credential selector in node settings

2. **Limit Credential Scope**: Use minimal required scopes
   - **Why**: Reduces damage if credentials compromised
   - **How**: Use `gmail.send` for send-only, `gmail.readonly` for read-only

### Data Protection
1. **Don't Send Sensitive Data**: Avoid PII, passwords, API keys in emails
   - **Why**: Email is transmitted in plain text (unless TLS enabled)
   - **How**: Use secure links instead of embedding sensitive info

2. **Sanitize Email Content**: Clean user-provided data before sending
   - **Why**: Prevent injection attacks or inappropriate content
   - **How**: Use Code node to sanitize email body/subject

### Access Control
1. **Use Service Account for Non-Personal Emails**: For transactional emails
   - **Why**: Separates system emails from user emails
   - **How**: Create service account and configure for system notifications

2. **Implement Audit Logging**: Track who/what sent emails
   - **Why**: Compliance and security monitoring
   - **How**: Log send operations with timestamp and recipient

## Workflow Design

### Node Placement
1. **Validate Email Addresses First**: Check recipient before sending
   - **Why**: Prevents send failures
   - **How**: Use IF node to validate email format

2. **Set Proper Headers**: Configure reply-to and from addresses
   - **Why**: Ensures responses go to correct address
   - **How**: Use node settings to configure headers

### Connection Management
1. **Reuse Credentials**: Use same Gmail credential across nodes
   - **Why**: Easier management, consistent account
   - **How**: Select existing credential from dropdown

2. **Test Sending**: Always test email workflow
   - **Why**: Verify formatting and delivery
   - **How**: Send test email to yourself first

### Data Flow
1. **Build Email Body Systematically**: Use Set node to structure email
   - **Why**: Cleaner, more readable emails
   - **How**: Concatenate subject, body, HTML using Set node
</best_practices>

<troubleshooting>
## Common Errors

### Authentication Errors

<error id="err-401" http_code="401">
- **Symptom**: "Unauthorized" or "Invalid credentials"
- **Cause**: OAuth token expired, credential revoked, or invalid
- **Immediate Fix**:
  1. Check N8N credential status
  2. Delete and recreate credential
  3. Re-authenticate with Google account
  4. Verify Gmail account access in Google settings
- **Prevention**:
  - Keep credentials up to date
  - Don't revoke app access in Google settings
  - Check that account isn't restricted
- **N8N Logs**: Check execution logs for "invalid_grant" errors
- **Reference**: [Authentication](#authentication)
</error>

### Send Quota Errors

<error id="err-quota" http_code="403">
- **Symptom**: "Daily limit exceeded" or "Quota exceeded"
- **Cause**: Exceeded daily sending limit
- **Immediate Fix**:
  1. Stop sending temporarily (quota resets at midnight)
  2. For new accounts: Verify account and request higher quota
  3. Reduce send frequency or batch size
  4. Wait 24 hours for quota reset
- **Prevention**:
  - Verify account with Google to increase quota
  - Spread sends over time
  - Monitor send count
  - Request higher quota from Google Cloud Console
- **N8N Feature**: Can check remaining quota before sending
- **Reference**: [Rate Limits](#rate_limits)
</error>

### Rate Limiting Errors

<error id="err-429" http_code="429">
- **Symptom**: "Too Many Requests"
- **Cause**: Exceeded Gmail API rate limits (250 req/sec)
- **Immediate Fix**:
  1. Enable automatic retry with exponential backoff
  2. Add "Wait" node with 2-5 second delays
  3. Reduce concurrent workflow executions
  4. Batch operations
- **Prevention**:
  - Space out operations with delays
  - Use batch processing for multiple emails
  - Monitor API quotas
- **N8N Feature**: Built-in retry with configurable backoff
- **Reference**: [Rate Limits](#rate_limits)
</error>

### Email Format Errors

<error id="err-format" http_code="400">
- **Symptom**: "Invalid format" or "Bad request"
- **Cause**: Invalid email addresses, malformed recipients, or content issues
- **Immediate Fix**:
  1. Validate email addresses before sending (use regex check)
  2. Check recipient list format (should be array or comma-separated)
  3. Verify email body isn't malformed
  4. Check attachment paths exist
- **Prevention**:
  - Validate email format with IF node
  - Use Set node to normalize recipient data
  - Test with sample emails
- **N8N Tool**: Use "Set" node to validate and format data
</error>

### Recipient/Size Errors

<error id="err-size" http_code="413">
- **Symptom**: "Message too large" or "Too many recipients"
- **Cause**: Email >25MB or >500 recipients
- **Immediate Fix**:
  1. Check attachment sizes (each <25MB)
  2. Check total email size <25MB
  3. Split recipients into multiple sends if >500
  4. Compress attachments
- **Prevention**:
  - Validate attachments before sending
  - Check recipient count
  - Implement size checking in Set node
- **N8N Context**: Use Split In Batches for bulk recipients
</error>

## Diagnostic Steps

1. **Check N8N Execution Logs**
   - View execution history
   - Check input/output data
   - Review error messages
   - Inspect node configuration

2. **Test Node Isolation**
   - Send test email to yourself
   - Verify credential in N8N
   - Check Gmail account settings
   - Test with simple recipient

3. **Verify Configuration**
   - Email address format
   - Recipient list format
   - Email body structure
   - Attachment paths

4. **Review N8N Environment**
   - N8N version and Gmail node version
   - Credential scopes
   - Send quota status
   - API quota status

5. **Check Gmail Settings**
   - Account verification status
   - Less secure apps setting (if applicable)
   - Sending restrictions
   - API quotas in Google Cloud Console
</troubleshooting>

<related_docs>
## Documentation Structure

- **Operations**: See [gmail-operations.md](#) for detailed operation reference
- **Examples**: Check N8N workflow templates for Gmail patterns

## Related Nodes

- **Google Drive**: [../google-drive.md](#) - For attachment file management
- **HTTP Request**: [../Core/http-request.md](#) - For direct Gmail API calls
- **Set**: [../Core/set.md](#) - Email body formatting and data preparation
- **IF**: [../Core/if.md](#) - Conditional sending logic

## External Resources

- **Official N8N Documentation**: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/
- **Gmail API Documentation**: https://developers.google.com/gmail/api
- **Gmail Search Syntax**: https://support.google.com/mail/answer/7190
- **Gmail Send Limits**: https://support.google.com/a/answer/6350159
- **Community Discussions**: https://community.n8n.io/
- **N8N Workflows**: https://n8n.io/workflows/ (search "Gmail")
- **Service Status**: https://www.google.com/appsstatus
</related_docs>

<metadata_summary>
## Document Information

- **Last Updated**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 85% (Core operations documented, advanced features pending)
- **Validation Status**: Validated against official N8N documentation
- **Next Review**: 2025-11-30
- **N8N Version Tested**: Latest (self-hosted and cloud)
- **Node Version**: Latest n8n-nodes-base
</metadata_summary>
