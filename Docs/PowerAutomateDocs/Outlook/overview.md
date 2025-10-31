# Office 365 Outlook Connector Overview

---
type: connector-overview
connector_name: Office 365 Outlook
connector_type: standard
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [outlook, email, calendar, contacts, send, receive, meeting, event, exchange]
related_connectors: [Office 365 Users, Microsoft Teams, SharePoint]
api_limits:
  calls_per_minute: 5
  calls_per_hour: 300
  max_email_size_mb: 49
  max_send_batch_mb: 500
  max_concurrent_requests: 70
official_docs_url: https://learn.microsoft.com/en-us/connectors/office365/
---

<official_docs>
https://learn.microsoft.com/en-us/connectors/office365/
</official_docs>

<description>
Office 365 Outlook connector enables automation of email, calendar, and contact management within Microsoft 365 environments. Supports sending/receiving emails, calendar event management, contact operations, and advanced features like approval emails and flagging, with comprehensive integration across Power Automate, Logic Apps, and Power Apps.
</description>

<capabilities>
## Core Capabilities
- Send, reply, forward, delete, and move emails
- Read and manage inbox messages with filtering
- Create, update, and delete calendar events
- Manage contacts (create, update, delete, get)
- Flag emails and mark as read/unread
- Send approval emails and emails with options
- Access shared calendars and mailboxes

## Supported Operations
- **Email Management**: Send (V2), Get emails (V3), Reply (V3), Forward (V2), Delete (V2), Move (V2), Mark as read/unread (V3), Flag email (V2)
- **Calendar Operations**: Create event (V4), Update event (V4), Delete event (V2), Get calendar view (V3), Get events
- **Contact Operations**: Create/update/delete contacts (V2), Get contacts
- **Advanced**: Send approval email, Send email with options, Draft messages, Export email

## Integration Features
- Real-time triggers for new emails and calendar events
- Support for HTML and plain text email formatting
- Attachment handling for emails
- Shared calendar access based on permissions
- Importance and sensitivity flags for emails
</capabilities>

<api_limits>
## Rate Limits

**Connection-Level Throttling**
- **300 API calls per 60 seconds** per connection
- Throttling scope: per connection
- Retry-After header: yes

**Action-Specific Limits**
- Send email batch: **500 MB total** per 5 minutes
- Concurrent requests: **70 simultaneous requests** maximum
- Max email size: **49 MB** per email
- Get calendar events: **256 events** maximum returned

**Throttling Behavior**
- HTTP Status: 429 (Too Many Requests)
- Error message: "Rate limit exceeded"
- Automatic retry: yes

## Size Limits

**Email Operations**
- Max email size: **49 MB** including attachments
- Max send batch: **500 MB** per 5 minutes
- Max recipients: No explicit limit documented

**Calendar Operations**
- Max events returned: **256 events** per query
- Requires pagination for larger datasets

## Timeout Limits
- Graph API timeout: **30 seconds**
- Outlook REST API timeout: **60 seconds**
</api_limits>

<critical_limitations>
## Email Limitations

<limitation id="lim-001" severity="high">
**Item Attachments Not Supported**: Cannot handle item attachments (embedded emails, calendar items)

- **Impact**: Cannot process or send emails with embedded items
- **Scope**: All email operations
- **Workaround**: Extract item as file attachment or use different method
- **Affected Operations**: Send email, Get email, Forward email
</limitation>

<limitation id="lim-002" severity="medium">
**Encrypted Emails Unsupported**: Cannot process encrypted emails for certain operations

- **Impact**: Encrypted email content not accessible
- **Scope**: Read operations on encrypted messages
- **Workaround**: Decrypt emails manually or use alternative connector
- **Affected Operations**: Get email, Get emails
</limitation>

<limitation id="lim-003" severity="medium">
**256 Event Limit**: Calendar queries return maximum 256 events

- **Impact**: Missing events if calendar has more than 256 events in query range
- **Scope**: Get calendar view, Get events operations
- **Workaround**: Use date filtering to narrow results or implement pagination
- **Affected Operations**: Get calendar view of events, Get events
</limitation>

## Authentication Limitations

<limitation id="lim-004" severity="high">
**Service Principal Not Supported**: Connector does not support app-only authentication

- **Impact**: Requires user context, cannot use application permissions
- **Scope**: All operations
- **Workaround**: Use user account with delegated permissions
- **Affected Operations**: All actions and triggers
</limitation>

<limitation id="lim-005" severity="medium">
**Non-Shareable Connections**: Connections cannot be shared between users

- **Impact**: Each user must create own connection when apps shared
- **Scope**: All connection types
- **Workaround**: Document connection setup for all users
- **Affected Operations**: All operations
</limitation>

## Calendar Limitations

<limitation id="lim-006" severity="medium">
**Shared Calendar Permissions**: Access limited by user's permissions to shared calendar

- **Impact**: Cannot perform operations beyond user's permission level
- **Scope**: Shared calendar operations
- **Workaround**: Ensure proper permissions granted to service account
- **Affected Operations**: All calendar operations on shared calendars
</limitation>
</critical_limitations>

<authentication>
## Supported Authentication Methods

### OAuth 2.0 (Only Method)
- Flow type: Authorization Code
- Required scopes: Mail.ReadWrite, Mail.Send, Calendars.ReadWrite, Contacts.ReadWrite
- Token refresh: Automatic
- Account type: Organizational accounts only (Azure AD)

### Connection Types
1. **Default**: All regions except Azure Government
2. **Office 365 Credentials (GCC)**: Government Cloud
3. **Office 365 Credentials (GCC High)**: High-security government environments

### Service Principal
- Supported: No
- Connector requires user context (delegated permissions)

## Required Permissions

### Delegated Permissions (User Context)
- **Mail.ReadWrite**: Read and write access to user mailbox
- **Mail.Send**: Send emails as user
- **Calendars.ReadWrite**: Manage user calendar events
- **Contacts.ReadWrite**: Manage user contacts
- **MailboxSettings.Read**: Read mailbox settings

### Application Permissions (App-Only Context)
- Not supported by connector
</authentication>

<common_use_cases>
## 1. Automated Email Notifications

**Description**: Send notification emails triggered by events in other systems

**Typical Flow**:
```
Trigger: When item created (SharePoint/Forms)
↓
Action 1: Get item/response details
↓
Action 2: Send email (Outlook) - Notify stakeholders
↓
Result: Automated notifications for business events
```

**Key Actions**: Send an email (V2)
**Best For**: Alerts, confirmations, status updates

---

## 2. Email-Triggered Workflows

**Description**: Process incoming emails to trigger business workflows

**Typical Flow**:
```
Trigger: When a new email arrives (V3)
↓
Action 1: Get email details - Extract subject/body/attachments
↓
Action 2: Condition - Check if meets criteria
↓
Action 3: Create SharePoint item or start approval
↓
Result: Email-driven automation
```

**Key Actions**: When a new email arrives, Get email, Create item
**Best For**: Request processing, ticketing systems, approvals

---

## 3. Calendar Event Management

**Description**: Automate meeting scheduling and calendar synchronization

**Typical Flow**:
```
Trigger: When item created (Registration list)
↓
Action 1: Create event (V4) - Schedule meeting
↓
Action 2: Send email - Confirmation to attendees
↓
Result: Automated event scheduling
```

**Key Actions**: Create event (V4), Update event (V4)
**Best For**: Meeting scheduling, event registration, resource booking

---

## 4. Email Approval Workflows

**Description**: Request and track approvals via email

**Typical Flow**:
```
Trigger: When item created (Request list)
↓
Action 1: Send approval email - Request approval
↓
Action 2: Wait for approval response
↓
Action 3: Update item - Record decision
↓
Result: Email-based approval process
```

**Key Actions**: Send approval email, Send email with options
**Best For**: Purchase approvals, time-off requests, document reviews

---

## 5. Email Archiving and Organization

**Description**: Automatically organize and move emails based on rules

**Typical Flow**:
```
Trigger: When a new email arrives (V3)
↓
Action 1: Condition - Check sender/subject criteria
↓
Action 2: Move email (V2) - Organize into folder
↓
Action 3: Flag email (optional) - Mark for follow-up
↓
Result: Automated email organization
```

**Key Actions**: Move email (V2), Flag email (V2), Mark as read (V3)
**Best For**: Email management, archiving, priority flagging
</common_use_cases>

<best_practices>
## Performance Optimization

### API Call Efficiency
1. **Batch Email Sends**: Use single Send email action with multiple recipients instead of loops
2. **Filter at Source**: Use filtering in Get emails to reduce data transfer
3. **Cache Email Data**: Store frequently accessed email info in variables

### Throttling Management
1. **Add Delays**: Insert 1-2 second delays between email operations in loops
2. **Limit Concurrency**: Set concurrency control to 10-20 for email-triggered flows
3. **Monitor Send Volume**: Track email sends to stay under 500MB per 5 minutes

## Reliability & Error Handling

### Retry Logic
1. **Retry on 429**: Implement exponential backoff for throttling errors
2. **Handle Network Failures**: Configure automatic retry for transient errors

### Email Validation
1. **Validate Addresses**: Check email format before sending
2. **Handle Bounces**: Implement error handling for invalid recipients

## Security Best Practices

### Email Security
1. **Sanitize Content**: Validate/sanitize user input before including in emails
2. **Use Service Accounts**: Dedicated accounts for automated emails
3. **Limit Permissions**: Grant minimum necessary mailbox permissions

### Sensitive Data
1. **Encrypt Attachments**: Use encryption for sensitive file attachments
2. **Avoid Hardcoded Credentials**: Use secure storage for sensitive data
3. **Log Email Operations**: Track automated email sends for audit

## Flow Design

### Email Composition
1. **Use HTML Formatting**: Leverage HTML for professional email layouts
2. **Include Unsubscribe**: Add unsubscribe options for bulk notifications
3. **Test Email Templates**: Validate formatting across email clients

### Calendar Management
1. **Handle Time Zones**: Always specify time zones for calendar events
2. **Check Availability**: Verify attendee availability before scheduling
3. **Include Meeting Details**: Comprehensive event descriptions and locations
</best_practices>

<troubleshooting>
## Common Errors

### Throttling Errors (429)
<error id="err-429" http_code="429">
- **Symptom**: "Rate limit exceeded" or "Too many requests"
- **Cause**: Exceeded 300 calls per 60 seconds
- **Fix**: Add delays, reduce concurrency, implement retry logic
- **Reference**: [API Limits](#api_limits)
</error>

### Authentication Errors (401)
<error id="err-401" http_code="401">
- **Symptom**: "Unauthorized" or "Invalid token"
- **Cause**: Token expired or invalid connection
- **Fix**: Re-authenticate connection, verify permissions
</error>

### Permission Errors (403)
<error id="err-403" http_code="403">
- **Symptom**: "Forbidden" or "Insufficient permissions"
- **Cause**: User lacks required mailbox permissions
- **Fix**: Grant necessary permissions (Mail.Send, Calendars.ReadWrite, etc.)
</error>

### Email Size Errors
<error id="err-size" http_code="413">
- **Symptom**: "Request entity too large" or "Email exceeds size limit"
- **Cause**: Email size exceeds 49MB limit
- **Fix**: Reduce attachment sizes, use file links instead of attachments
- **Reference**: [Size Limits](#api_limits)
</error>

### Timeout Errors
<error id="err-timeout" http_code="504">
- **Symptom**: "Gateway timeout" or operation takes longer than expected
- **Cause**: Exceeded Graph API 30-second timeout
- **Fix**: Simplify operations, reduce data volume, retry after delay
</error>
</troubleshooting>

<related_docs>
## Documentation Structure

- **Actions**: [actions.md](./actions.md) - All available actions (to be created)
- **Triggers**: [triggers.md](./triggers.md) - Available triggers (to be created)

## Related Connectors

- **Office 365 Users**: User profile and manager lookups
- **Microsoft Teams**: Post notifications to Teams channels
- **SharePoint**: Create items from emails, attach files
- **OneDrive**: Store email attachments

## External Resources

- **Official Documentation**: https://learn.microsoft.com/en-us/connectors/office365/
- **Community Forum**: https://powerusers.microsoft.com/
- **Service Health**: https://admin.microsoft.com/Adminportal/Home#/servicehealth
</related_docs>

<metadata_summary>
## Document Information

- **Last Updated**: 2025-10-31
- **Fetch Date**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 40% (Overview complete, Actions: 0%, Triggers: 0%)
- **Validation Status**: Validated against Microsoft Learn documentation
- **Next Review**: 2025-11-30
- **Source**: Microsoft Learn official documentation
</metadata_summary>
