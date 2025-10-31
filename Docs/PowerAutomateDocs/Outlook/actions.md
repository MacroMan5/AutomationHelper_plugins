# Office 365 Outlook - Actions

---
type: connector-actions
connector_name: Office 365 Outlook
action_count: 45
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [outlook, email, calendar, contacts, send email, create event, office 365, actions]
categories: [create, read, update, delete, utility]
---

<action_summary>
**Total Actions**: 45+ (current versions only)

**By Category**:
- Email Operations: 20 actions (send, reply, forward, get, delete, move, flag, etc.)
- Calendar Operations: 10 actions (create/update/delete events, find meeting times, respond to invites)
- Contact Operations: 6 actions (create/get/update/delete contacts, get folders)
- Utility Operations: 9 actions (categories, rooms, mail tips, HTTP requests, MCP servers)

**Complexity Distribution**:
- Low complexity: 25 actions
- Medium complexity: 15 actions
- High complexity: 5 actions

**Most Used Actions**:
1. Send an email (V2)
2. Get emails (V3)
3. Create event (V4)
4. Reply to email (V3)
5. Get email (V2)
</action_summary>

<action_categories>
## Categories Overview

### Email Operations
Comprehensive email management including sending, reading, replying, forwarding, deleting, moving, flagging, and organizing emails. Supports both personal and shared mailboxes with rich filtering and attachment handling.

### Calendar Operations
Full calendar management with event creation, modification, deletion, and querying. Includes Teams meeting support, recurring events, room/resource booking, and meeting time suggestions.

### Contact Operations
Contact management with CRUD operations, folder management, and photo updates. Supports multiple email addresses, phone numbers, and physical addresses per contact.

### Utility Operations
Advanced operations including category management, room discovery, automatic reply configuration, mail tips retrieval, and custom Graph API requests via HTTP action.
</action_categories>

---

## Email Operations

### Send an Email (V2)

<action id="action-001" category="create" complexity="low" throttle_impact="medium">

<action_header>
**Operation Type**: Create
**Complexity**: Low
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: SendEmailV2
</action_header>

<description>
Sends an email message from the authenticated user's mailbox. Supports To/CC/BCC recipients, attachments, importance levels, and rich HTML formatting. Most commonly used Outlook action for automated email notifications and workflows.
</description>

<parameters>
#### Required Parameters

**To** (`string`)
- **Description**: Primary recipient email addresses
- **Format**: Semicolon-separated email list
- **Example**: "user@contoso.com;sales@fabrikam.com"

**Subject** (`string`)
- **Description**: Email subject line
- **Example**: "Order Confirmation #12345"

**Body** (`string`)
- **Description**: Email message content
- **Format**: HTML or plain text
- **Example**: "<p>Your order has been confirmed.</p>"

#### Optional Parameters

**CC** (`string`)
- **Description**: CC recipient addresses
- **Format**: Semicolon-separated email list

**BCC** (`string`)
- **Description**: BCC recipient addresses
- **Format**: Semicolon-separated email list

**Attachments** (`array`)
- **Description**: File attachments to include
- **Format**: Array of attachment objects
- **Structure**: `{"Name": "file.pdf", "ContentBytes": "[base64]"}`
- **Limit**: Total email size max 49 MB

**From** (`string`)
- **Description**: Sender address (send-on-behalf)
- **Requirement**: Send-on-behalf permissions required
- **Example**: "noreply@contoso.com"

**Importance** (`string`)
- **Description**: Email priority level
- **Values**: "Low", "Normal", "High"
- **Default**: "Normal"

**Is HTML** (`boolean`)
- **Description**: Whether body contains HTML
- **Default**: true

**Sensitivity** (`string`)
- **Description**: Email sensitivity level
- **Values**: "Normal", "Personal", "Private", "Confidential"
- **Default**: "Normal"
</parameters>

<returns>
**Return Type**: None (action does not return message ID)

**Behavior**: Email sent immediately; no confirmation object returned
</returns>

<limitations>
<limitation id="lim-email-001" severity="high">
**No Message ID Returned**: Action does not return sent message ID
- Cannot reference sent message for follow-up operations
- Workaround: Save copy to Sent Items and query by timestamp/subject
</limitation>

<limitation id="lim-email-002" severity="high">
**Total Size Limit**: 49 MB maximum per email including attachments
- Inline images count toward limit after base64 encoding
- Recommendation: Use file links for large files instead of attachments
</limitation>

<limitation id="lim-email-003" severity="medium">
**Send Rate Limit**: 500 MB per 5 minutes across all send operations
- Shared limit across all email send actions
- Recommendation: Implement delays for bulk email scenarios
</limitation>

<limitation id="lim-email-004" severity="medium">
**Inline Image Limit**: 1 MB maximum per inline image after base64 encoding
- Base64 encoding increases size by ~33%
- Recommendation: Optimize images before encoding
</limitation>
</limitations>

<best_practices>
- **HTML Validation**: Test HTML in Outlook before using in flows
- **Attachment Size**: Keep total email size under 10 MB for reliability
- **Recipient Validation**: Validate email addresses before sending
- **Error Handling**: Wrap in try-catch scope for graceful failure
- **Rate Limiting**: Add delays for bulk sending (minimum 1 second between sends)
- **Dynamic Content**: Use expressions for personalized email content
</best_practices>

<example>
```json
{
  "To": "customer@contoso.com",
  "Subject": "Order Confirmation - ORD-2025-12345",
  "Body": "<html><body><h2>Thank you for your order!</h2><p>Order ID: ORD-2025-12345</p><p>Total: $2,500.00</p><p>Estimated delivery: 3-5 business days</p></body></html>",
  "CC": "sales@fabrikam.com",
  "Importance": "Normal",
  "IsHTML": true,
  "Attachments": [
    {
      "Name": "OrderReceipt.pdf",
      "ContentBytes": "[base64-encoded-pdf-content]"
    }
  ]
}
```

**Use Case**: Automated order confirmation emails with receipt attachment
</example>

</action>

---

### Get Emails (V3)

<action id="action-002" category="read" complexity="medium" throttle_impact="high">

<action_header>
**Operation Type**: Read
**Complexity**: Medium
**Throttling Impact**: High
**Premium**: No
**Operation ID**: GetEmailsV3
</action_header>

<description>
Retrieves emails from a specified folder with advanced filtering capabilities. Supports filtering by sender, recipient, importance, subject, and custom search queries. Returns array of email objects with full metadata.
</description>

<parameters>
#### Optional Parameters

**Folder** (`string`)
- **Description**: Mail folder to retrieve from
- **Default**: "Inbox"
- **Format**: Folder path or ID

**To** (`string`)
- **Description**: Filter by recipient addresses
- **Limitation**: First 250 items only; use Search Query for more

**From** (`string`)
- **Description**: Filter by sender addresses
- **Limitation**: First 250 items only

**CC** (`string`)
- **Description**: Filter by CC recipients
- **Limitation**: First 250 items only

**Importance** (`string`)
- **Description**: Filter by importance
- **Values**: "Any", "Low", "Normal", "High"

**Subject Filter** (`string`)
- **Description**: Substring match in subject

**Search Query** (`string`)
- **Description**: Advanced search query (KQL syntax)
- **Example**: "from:user@contoso.com AND hasattachments:true"
- **Recommendation**: Use for complex filters to avoid 250-item limitation

**Top** (`integer`)
- **Description**: Maximum emails to return
- **Default**: All matching
- **Maximum**: 1000
- **Example**: 50, 100

**Include Attachments** (`boolean`)
- **Description**: Include attachment content
- **Default**: false
- **Warning**: May cause timeout with large attachments

**Mail box Address** (`string`)
- **Description**: Shared mailbox address
- **Requirement**: Full Access permissions
</parameters>

<returns>
**Return Type**: `Array` of email objects

**Structure**:
```json
{
  "value": [
    {
      "Id": "AAMkAGVmMDEz...",
      "Subject": "Order #12345",
      "From": "customer@contoso.com",
      "ToRecipients": "sales@fabrikam.com",
      "Body": "Email body...",
      "DateTimeReceived": "2025-10-31T10:30:00Z",
      "HasAttachments": true,
      "IsRead": false,
      "Importance": "Normal"
    }
  ]
}
```

**Dynamic Content**: Loop through `value` array; access `item()?['Property']`
</returns>

<limitations>
<limitation id="lim-email-005" severity="high">
**To/From/CC Limitation**: Filtering performed on first 250 items only
- Use Search Query field for comprehensive filtering
- Example: `from:user@contoso.com` instead of From parameter
</limitation>

<limitation id="lim-email-006" severity="medium">
**Maximum Results**: Returns max 1000 emails per call
- Implement pagination for larger result sets
- Use date filters to limit scope
</limitation>
</limitations>

<best_practices>
- **Search Query**: Use for advanced filtering beyond 250 items
- **Pagination**: Request only needed number of emails
- **Attachments**: Set false unless required; retrieve separately
- **Folder Selection**: Specify folder to reduce scope
- **Caching**: Cache results if re-querying frequently
</best_practices>

<example>
```json
{
  "Folder": "Inbox/Orders",
  "SearchQuery": "from:orders@customer.com AND received>=2025-10-01",
  "Top": 100,
  "IncludeAttachments": false
}
```

**Use Case**: Retrieving recent order emails for batch processing
</example>

</action>

---

### Reply to Email (V3)

<action id="action-003" category="create" complexity="low" throttle_impact="medium">

<action_header>
**Operation Type**: Create
**Complexity**: Low
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: ReplyToV3
</action_header>

<description>
Replies to an existing email message, maintaining conversation thread. Automatically includes original message and recipients. Supports HTML content and shared mailbox replies.
</description>

<parameters>
#### Required Parameters

**Message ID** (`string`)
- **Description**: ID of email to reply to
- **Source**: From trigger output or Get Email action
- **Example**: "AAMkAGVmMDEz..."

**Comment** (`string`)
- **Description**: Reply message content
- **Format**: HTML or plain text
- **Example**: "<p>Thank you for your inquiry...</p>"

#### Optional Parameters

**Mailbox Address** (`string`)
- **Description**: Shared mailbox address (if replying from shared mailbox)
- **Requirement**: Full Access permissions
</parameters>

<returns>
**Return Type**: None
</returns>

<limitations>
<limitation id="lim-email-007" severity="high">
**Encrypted Emails Not Supported**: Cannot reply to encrypted emails
- Action fails silently
- Recommendation: Check email properties before replying
</limitation>

<limitation id="lim-email-008" severity="low">
**UTC Conversion**: Original email datetime converted to UTC in reply
- May cause confusion with timezone display
- Expected behavior; no workaround needed
</limitation>
</limitations>

<best_practices>
- **Personalization**: Include original sender name in reply
- **Thread Preservation**: Reply maintains conversation threading
- **Error Handling**: Check if message ID valid before replying
- **Shared Mailbox**: Specify mailbox address for shared mailbox replies
</best_practices>

<example>
```json
{
  "MessageID": "AAMkAGVmMDEz...",
  "Comment": "<p>Thank you for your order! Your order #12345 has been confirmed and will ship within 2 business days.</p><p>Best regards,<br/>Sales Team</p>"
}
```

**Use Case**: Automated reply to customer inquiries
</example>

</action>

---

### Forward an Email (V2)

<action id="action-004" category="create" complexity="low" throttle_impact="medium">

<action_header>
**Operation Type**: Create
**Complexity**: Low
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: ForwardEmailV2
</action_header>

<description>
Forwards an existing email to specified recipients with optional additional comment. Maintains original attachments and message content.
</description>

<parameters>
#### Required Parameters

**Message ID** (`string`)
- **Description**: ID of email to forward

**To Recipients** (`string`)
- **Description**: Forward recipient addresses
- **Format**: Semicolon-separated list
- **Example**: "manager@contoso.com;archive@contoso.com"

#### Optional Parameters

**Comment** (`string`)
- **Description**: Additional message to include
- **Format**: HTML or plain text

**Mailbox Address** (`string`)
- **Description**: Shared mailbox address
</parameters>

<best_practices>
- **Approval Workflows**: Forward for manager approval
- **Escalation**: Automatic escalation forwarding
- **Archival**: Forward to archival systems
</best_practices>

<example>
**Use Case**: Forward high-priority emails to manager for review
</example>

</action>

---

### Delete Email (V2)

<action id="action-005" category="delete" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Delete
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: DeleteEmailV2
</action_header>

<description>
Deletes an email message by ID. Moves email to Deleted Items folder (soft delete). Can be used with shared mailboxes.
</description>

<parameters>
#### Required Parameters

**Message ID** (`string`)
- **Description**: ID of email to delete

#### Optional Parameters

**Mailbox Address** (`string`)
- **Description**: Shared mailbox address
</parameters>

<best_practices>
- **Confirmation**: Implement approval before deleting important emails
- **Logging**: Log deleted message details for audit
- **Archive First**: Consider moving to archive folder instead
- **Condition**: Use conditions to ensure correct email deleted
</best_practices>

<example>
**Use Case**: Auto-delete spam or processed emails
</example>

</action>

---

### Move Email (V2)

<action id="action-006" category="update" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Update
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: MoveEmailV2
</action_header>

<description>
Moves an email to a specified folder within the same mailbox. Useful for organizing and categorizing emails automatically.
</description>

<parameters>
#### Required Parameters

**Message ID** (`string`)
- **Description**: ID of email to move

**Folder Path** (`string`)
- **Description**: Destination folder path
- **Format**: Folder path or folder ID
- **Example**: "Inbox/Processed", "Archive/2025"
- **Note**: Must be within same mailbox

#### Optional Parameters

**Mailbox Address** (`string`)
- **Description**: Shared mailbox address
</parameters>

<best_practices>
- **Organization**: Auto-organize by subject, sender, or content
- **Workflow**: Move after processing completion
- **Archive**: Move old emails to archive folders
- **Folder Creation**: Ensure destination folder exists
</best_practices>

<example>
```json
{
  "MessageID": "AAMkAGVmMDEz...",
  "FolderPath": "Inbox/Orders/Processed"
}
```

**Use Case**: Moving processed order emails to archive folder
</example>

</action>

---

### Get Email (V2)

<action id="action-007" category="read" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Read
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: GetEmailV2
</action_header>

<description>
Retrieves a specific email by ID with full metadata and optional attachment content. Use after trigger or Get Emails to fetch complete email details.
</description>

<parameters>
#### Required Parameters

**Message ID** (`string`)
- **Description**: ID of email to retrieve

#### Optional Parameters

**Include Attachments** (`boolean`)
- **Description**: Include attachment content
- **Default**: false

**Mailbox Address** (`string`)
- **Description**: Shared mailbox address

**Extract Sensitivity Label** (`boolean`)
- **Description**: Extract sensitivity label metadata
- **Default**: false
</parameters>

<returns>
Complete email object with all fields and optional attachment bytes
</returns>

<best_practices>
- **Trigger Follow-up**: Use after trigger to get full email details
- **Attachments**: Only include when needed
- **Shared Mailbox**: Specify address for shared mailbox access
</best_practices>

</action>

---

## Calendar Operations

### Create Event (V4)

<action id="action-011" category="create" complexity="medium" throttle_impact="medium">

<action_header>
**Operation Type**: Create
**Complexity**: Medium
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: CreateEventV4
</action_header>

<description>
Creates a new calendar event with comprehensive options including attendees, recurrence, reminders, and Teams meeting integration. Supports all-day events, time zones, and importance levels.
</description>

<parameters>
#### Required Parameters

**Calendar ID** (`string`)
- **Description**: Target calendar identifier
- **Default**: Primary calendar
- **Format**: Calendar ID or name

**Subject** (`string`)
- **Description**: Event title
- **Example**: "Team Standup Meeting"

**Start Time** (`datetime`)
- **Description**: Event start date/time
- **Format**: "date-no-tz" (2025-10-31T10:00:00)
- **Note**: Timezone specified separately

**End Time** (`datetime`)
- **Description**: Event end date/time
- **Format**: "date-no-tz" (2025-10-31T11:00:00)

**Time Zone** (`string`)
- **Description**: Event timezone
- **Format**: Windows timezone name
- **Example**: "Pacific Standard Time", "Eastern Standard Time"
- **Requirement**: Must have Exchange Online Mailbox

#### Optional Parameters

**Attendees** (`array`)
- **Description**: Meeting attendees with type
- **Format**: Array of attendee objects
- **Types**: Required, Optional, Resource
- **Example**: `[{"EmailAddress": "user@contoso.com", "Type": "Required"}]`

**Body** (`string`)
- **Description**: Event description/agenda
- **Format**: HTML or plain text

**Location** (`string`)
- **Description**: Event location
- **Example**: "Conference Room A", "https://teams.microsoft.com/..."

**Importance** (`string`)
- **Description**: Event importance
- **Values**: "low", "normal", "high"

**Is All Day Event** (`boolean`)
- **Description**: All-day event flag
- **Default**: false

**Recurrence Pattern** (`string`)
- **Description**: Recurrence pattern type
- **Values**: "daily", "weekly", "monthly", "yearly"

**Selected Days of Week** (`string`)
- **Description**: Days for weekly recurrence
- **Format**: Comma-separated
- **Example**: "Monday,Wednesday,Friday"

**Reminder** (`integer`)
- **Description**: Minutes before event for reminder
- **Example**: 15, 30, 60

**Sensitivity** (`string`)
- **Description**: Event sensitivity
- **Values**: "normal", "personal", "private", "confidential"

**Show As** (`string`)
- **Description**: Availability status during event
- **Values**: "free", "tentative", "busy", "oof", "workingElsewhere"
</parameters>

<returns>
**Return Type**: Event object with ID and all properties
</returns>

<limitations>
<limitation id="lim-cal-001" severity="medium">
**Recurring Events - Multiple Days**: If event repeats several times per week, must specify days or only one day saves after update
- Workaround: Always specify Selected Days of Week for weekly recurrence
</limitation>

<limitation id="lim-cal-002" severity="medium">
**Timezone Requirement**: Time zone selection requires Exchange Online Mailbox
- Fails without Exchange license
- Workaround: Ensure user has appropriate license
</limitation>
</limitations>

<best_practices>
- **Teams Meetings**: Use "Create Teams Meeting" action for Teams integration
- **Timezone**: Always specify timezone explicitly
- **Attendees**: Use Required/Optional types appropriately
- **Reminders**: Set reasonable reminder times (15-60 minutes)
- **Recurrence**: For weekly recurring, always specify days
</best_practices>

<example>
```json
{
  "CalendarID": "Primary",
  "Subject": "Weekly Team Sync",
  "StartTime": "2025-11-04T14:00:00",
  "EndTime": "2025-11-04T15:00:00",
  "TimeZone": "Pacific Standard Time",
  "Attendees": [
    {
      "EmailAddress": "team@contoso.com",
      "Type": "Required"
    }
  ],
  "Location": "Conference Room B",
  "Body": "<p>Weekly team sync to review progress and blockers.</p>",
  "Recurrence": "weekly",
  "SelectedDaysOfWeek": "Monday",
  "Reminder": 15,
  "Importance": "normal"
}
```

**Use Case**: Creating recurring team meeting from workflow
</example>

</action>

---

### Update Event (V4)

<action id="action-012" category="update" complexity="medium" throttle_impact="medium">

<action_header>
**Operation Type**: Update
**Complexity**: Medium
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: UpdateEventV4
</action_header>

<description>
Updates an existing calendar event. Warning: All omitted fields reset to default values. If organizer, all attendees receive meeting updates.
</description>

<parameters>
Same parameters as Create Event plus:

**Event ID** (`string`, required)
- **Description**: ID of event to update
</parameters>

<limitations>
<limitation id="lim-cal-003" severity="critical">
**Omitted Fields Reset**: All event fields not provided in update reset to default values
- Must include ALL fields, even unchanged ones
- Recommendation: Get event first, modify needed fields, then update with all fields
</limitation>

<limitation id="lim-cal-004" severity="high">
**Attendee Notifications**: All attendees receive update if you're organizer
- Cannot suppress notification
- Recommendation: Inform users about automated updates
</limitation>
</limitations>

<best_practices>
- **Get Before Update**: Always retrieve event first to preserve all fields
- **Field Preservation**: Include all fields in update, even unchanged
- **Attendee Communication**: Consider notification impact
- **Validation**: Verify event ID before updating
</best_practices>

</action>

---

### Get Events (V4) & Get Calendar View of Events (V3)

<action id="action-013" category="read" complexity="medium" throttle_impact="medium">

**Get Events (V4)**:
- Lists events from calendar with OData filtering
- Returns series definitions for recurring events (not instances)

**Get Calendar View of Events (V3)**:
- Lists all events including recurring instances within date range
- Maximum 256 events returned
- Recommended for displaying calendar views

<parameters>
**Required**: Calendar ID, Start Time, End Time (for Calendar View)
**Optional**: Filter Query, Order By, Top, Skip
</parameters>

<best_practices>
- **Date Ranges**: Use Calendar View for specific date range queries
- **Recurring Events**: Calendar View expands recurring events to instances
- **Pagination**: Use Top/Skip for large result sets
- **Filters**: Apply OData filters for targeted queries
</best_practices>

</action>

---

### Create Teams Meeting

<action id="action-014" category="create" complexity="medium" throttle_impact="medium">

<action_header>
**Operation Type**: Create
**Complexity**: Medium
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: CreateTeamsMeeting
</action_header>

<description>
Creates a meeting with Teams meeting link at bottom of invite. Enables online participation via Microsoft Teams. All parameters same as Create Event with automatic Teams link generation.
</description>

<parameters>
Same as Create Event (V4)
</parameters>

<returns>
Event object with Teams meeting link in Location or Body
</returns>

<best_practices>
- **Hybrid Meetings**: Use for meetings with remote participants
- **Link Access**: Teams link automatically included in invite
- **Permissions**: Requires Teams license for organizer
- **Recording**: Teams meeting enables cloud recording options
</best_practices>

<example>
**Use Case**: Creating client meeting with Teams link for remote participation
</example>

</action>

---

## Contact Operations Summary

### Create Contact (V2)
Creates new contact with name, emails, phones, addresses. Returns contact ID.

### Get Contact (V2)
Retrieves specific contact by ID from specified folder.

### Get Contacts (V2)
Lists contacts with OData filtering and pagination.

### Update Contact (V2)
Modifies existing contact information. Include all fields to preserve data.

### Delete Contact (V2)
Removes contact from folder by ID.

### Get Contact Folders (V2)
Lists available contact folders with IDs.

### Update Contact Photo
Updates profile photo for contact (max 4 MB).

---

## Utility Operations Summary

### Get Outlook Category Names
Retrieves list of available Outlook categories for email organization.

### Assign Outlook Category
Applies category to single or multiple emails for organization.

### Get Rooms (V2) & Get Room Lists (V2)
Lists meeting rooms and room lists in tenant. Room limit: 100 per query.

### Get Mail Tips for Mailbox (V2)
Retrieves auto-reply status and mailbox information. Not available in GccHigh/Mooncake.

### Set Up Automatic Replies (V2)
Configures out-of-office auto-reply messages with schedule.

### Send an HTTP Request
Constructs custom Microsoft Graph API requests to Outlook endpoints. Supported segments: /me, /users, messages, mailFolders, events, calendar.

### Export Email (V2)
Exports email content in EML format for archival or transfer.

### Draft an Email Message
Creates draft email without sending. Can send later with Send Draft action.

---

## MCP Servers (Model Context Protocol)

The connector provides three MCP servers for advanced integration:

### Email Management MCP Server
Manages email operations via JSONRPC format.

### Contact Management MCP Server
Handles contact CRUD operations via JSONRPC.

### Meeting Management MCP Server
Manages events, calendars, and meetings via JSONRPC.

---

## Common Error Codes

<error id="err-403" http_code="403">
**Error**: 403 Forbidden
**Causes**:
- Insufficient permissions
- Shared mailbox without Full Access
- Protected/encrypted content
- Send-on-behalf without permissions

**Solutions**:
- Grant appropriate permissions (Full Access for shared mailboxes)
- Verify user has rights to perform operation
- Check for protected content
</error>

<error id="err-404" http_code="404">
**Error**: 404 Not Found
**Causes**:
- Message/Event ID invalid or deleted
- Folder doesn't exist
- Calendar not found

**Solutions**:
- Verify ID is current and valid
- Check folder path spelling
- Ensure resource hasn't been deleted
</error>

<error id="err-429" http_code="429">
**Error**: 429 Too Many Requests
**Causes**:
- Exceeded 300 API calls per 60 seconds
- Too many concurrent operations

**Solutions**:
- Add delays between operations (2+ seconds)
- Implement exponential backoff
- Limit concurrency on triggers
- Use multiple connections for high volume
</error>

<error id="err-504" http_code="504">
**Error**: 504 Gateway Timeout
**Causes**:
- Operation exceeded 30-60 second timeout
- Large attachment processing
- Complex query execution

**Solutions**:
- Reduce operation complexity
- Process attachments separately
- Simplify queries
- Action automatically retries up to 4 times
</error>

---

## General Limitations

<limitation id="lim-general-001" severity="critical">
**API Rate Limit**: 300 calls per 60 seconds per connection
- Shared across all actions and triggers
- Recommendation: Add 2+ second delays; monitor usage
</limitation>

<limitation id="lim-general-002" severity="high">
**Content Limits**:
- Max email size: 49 MB
- Total send action limit: 500 MB per 5 minutes
- All actions limit: 2000 MB per 5 minutes
- Inline images: 1 MB max after base64 encoding
</limitation>

<limitation id="lim-general-003" severity="high">
**Concurrent Operations**:
- Maximum concurrent megabyte transfer: 300 MB
- Maximum concurrent requests: 70
- Recommendation: Limit parallel operations
</limitation>

<limitation id="lim-general-004" severity="high">
**Attachment Issues**:
- Item attachments (email/calendar) not supported
- Digitally signed emails may have incorrect attachment content
- Workaround: Use HTTP action with Microsoft Entra ID connector
</limitation>

<limitation id="lim-general-005" severity="medium">
**Shared Mailbox Constraints**:
- Group address cannot be used as shared mailbox
- Permissions replicate within ~2 hours after grant
- User-to-user shared requires Full Access permissions
</limitation>

<limitation id="lim-general-006" severity="medium">
**Service Limitations**:
- REST API disabled for on-premise dedicated mail servers
- Service Principal authentication not supported
- Some operations unavailable in Sovereign clouds
</limitation>

<limitation id="lim-general-007" severity="medium">
**Calendar Limitations**:
- Each user has unique calendar ID for shared calendars
- Shared connections may return 404 errors
- Workaround: Use owner's connection for shared calendar flows
</limitation>

---

## Performance Best Practices

### Throttling Management
1. **Delays**: Add minimum 2-second delays between operations
2. **Batching**: Group operations when possible
3. **Concurrency**: Limit to 10-20 parallel operations
4. **Monitoring**: Track API usage patterns

### Email Operations
1. **Attachments**: Avoid including unless necessary
2. **Bulk Sends**: Implement queueing with delays
3. **Search Optimization**: Use Search Query for complex filters
4. **Folder Organization**: Organize emails to reduce query scope

### Calendar Operations
1. **Date Ranges**: Limit query ranges to needed timeframe
2. **Recurring Events**: Use Get Events for series, Calendar View for instances
3. **Room Booking**: Cache room lists for reuse

### Error Handling
1. **Retry Logic**: Implement exponential backoff for 429/504 errors
2. **Validation**: Validate IDs and addresses before operations
3. **Graceful Degradation**: Handle failures without breaking flow
4. **Logging**: Log all operations for debugging

---

**Last Updated**: 2025-10-31
**Documentation Version**: 1.0
**Connector Version**: Current (as of 2025-10-31)
**Official Reference**: https://learn.microsoft.com/en-us/connectors/office365/
