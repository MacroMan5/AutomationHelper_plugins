# Office 365 Outlook - Triggers

---
type: connector-triggers
connector_name: Office 365 Outlook
trigger_count: 6
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [outlook, email, calendar, trigger, webhook, new email, event, flagged, shared mailbox]
trigger_types: [webhook, polling]
---

<trigger_summary>
**Total Triggers**: 6

**Types**:
- Webhook/Real-time: 6 triggers (email and calendar events)
- Polling: 0 triggers (all use webhook technology)
- Instant/Manual: 0 triggers

**Categories**:
- Email Triggers: 4 (new email, shared mailbox, mentioned, flagged)
- Calendar Triggers: 2 (event created, event modified/deleted)

**Recommendation**: All triggers use webhook technology for real-time notifications. Configure filters to reduce unnecessary flow executions.
</trigger_summary>

---

## Email Triggers

### When a New Email Arrives (V3)

<trigger id="trigger-001" type="webhook" frequency="real-time" latency="seconds">

<trigger_header>
**Type**: Webhook (Real-time)
**Frequency**: Instant notification
**Latency**: 1-10 seconds typical
**Operation ID**: OnNewEmailV3
**Status**: Current (V3 is latest)
</trigger_header>

<description>
Triggers when a new email is received in the mailbox. Supports advanced filtering by folder, sender, recipient, subject, and importance. Uses webhook for real-time delivery with minimal latency. Most commonly used Outlook trigger for email automation.
</description>

<parameters>
#### Optional Parameters

**Folder** (`string`)
- **Description**: Mail folder to monitor
- **Default**: Inbox
- **Format**: Folder path or folder ID
- **Example**: "Inbox/Orders", "Deleted Items"
- **Note**: Dynamic dropdown of available folders

**To** (`string`)
- **Description**: Filter by recipient email addresses
- **Format**: Semicolon-separated email list
- **Example**: "sales@contoso.com;orders@contoso.com"
- **Limitation**: Only one of To/CC should be populated

**CC** (`string`)
- **Description**: Filter by CC recipient addresses
- **Format**: Semicolon-separated email list
- **Limitation**: Only one of To/CC should be populated

**From** (`string`)
- **Description**: Filter by sender addresses
- **Format**: Semicolon-separated email list
- **Example**: "customer@fabrikam.com"

**Importance** (`string`)
- **Description**: Filter by email importance
- **Values**: "Any", "High", "Normal", "Low"
- **Default**: "Any"

**Include Attachments** (`boolean`)
- **Description**: Whether to include attachment content in trigger output
- **Default**: false
- **Note**: Setting true increases response size and may cause timeouts with large attachments

**Subject Filter** (`string`)
- **Description**: String to match in email subject
- **Format**: Case-insensitive substring match
- **Example**: "Invoice", "Order Confirmation"
</parameters>

<outputs>
**Trigger Output Structure**:
```json
{
  "Id": "AAMkAGVmMDEz...",
  "Subject": "New Order #12345",
  "From": "customer@contoso.com",
  "ToRecipients": "sales@fabrikam.com",
  "CcRecipients": "",
  "Body": "Email body content...",
  "BodyPreview": "First 255 characters...",
  "Importance": "Normal",
  "HasAttachments": true,
  "DateTimeReceived": "2025-10-31T14:30:00Z",
  "IsRead": false,
  "Attachments": []
}
```

**Key Fields**:
- **Id**: Unique message identifier for subsequent operations
- **From**: Sender email address
- **Subject**: Email subject line
- **Body**: Full HTML email body
- **DateTimeReceived**: ISO 8601 timestamp
- **HasAttachments**: Boolean indicating attachments present
- **Attachments**: Array of attachment metadata (if Include Attachments = true)
</outputs>

<limitations>
<limitation id="lim-trig-001" severity="high">
**Large Emails Skipped**: Emails with total size > 50 MB or Exchange Admin limit are skipped
- No error notification when skipped
- Recommendation: Check size limits; use separate large file handling
</limitation>

<limitation id="lim-trig-002" severity="high">
**Dynamic Delivery Emails**: May trigger twice for emails with attachments using Dynamic Delivery
- Expected behavior with certain mail flow rules
- Recommendation: Implement deduplication logic using message ID
</limitation>

<limitation id="lim-trig-003" severity="medium">
**To/CC Filter Limitation**: Only one field should be populated at a time
- Using both may cause unexpected behavior
- Recommendation: Use separate flows or advanced filtering
</limitation>

<limitation id="lim-trig-004" severity="medium">
**Protected Emails**: May skip protected/encrypted emails
- Output won't contain actual message body
- Recommendation: Check HasAttachments and Body fields for empty values
</limitation>

<limitation id="lim-trig-005" severity="low">
**Attachment Timeout**: Large attachment inclusion may cause timeout
- Especially with multiple large attachments
- Recommendation: Set Include Attachments = false; retrieve separately with Get Attachment action
</limitation>
</limitations>

<best_practices>
- **Folder Filtering**: Always specify folder to reduce unnecessary triggers
- **Attachments**: Set Include Attachments = false unless specifically needed
- **Deduplication**: Implement logic to handle potential duplicate triggers
- **Subject Filters**: Use specific subject patterns to minimize false triggers
- **Concurrency**: Limit concurrency for high-volume email processing
</best_practices>

<example>
```json
{
  "Folder": "Inbox/Orders",
  "From": "orders@customer.com",
  "SubjectFilter": "New Order",
  "Importance": "Any",
  "IncludeAttachments": false
}
```

**Use Case**: Automated order processing from customer email submissions
</example>

</trigger>

---

### When a New Email Arrives in a Shared Mailbox (V2)

<trigger id="trigger-002" type="webhook" frequency="real-time" latency="seconds">

<trigger_header>
**Type**: Webhook (Real-time)
**Frequency**: Instant notification
**Latency**: 1-10 seconds typical
**Operation ID**: OnNewEmailSharedMailboxV2
**Status**: Current
</trigger_header>

<description>
Triggers when new email arrives in a shared mailbox. Requires full access permissions to shared mailbox. Supports same filtering options as standard new email trigger with additional mailbox address specification.
</description>

<parameters>
#### Required Parameters

**Original Mailbox Address** (`string`)
- **Description**: Email address of shared mailbox to monitor
- **Format**: Full email address
- **Example**: "sales@contoso.com", "support@fabrikam.com"
- **Requirement**: User must have Full Access permissions

#### Optional Parameters
Same filtering options as "When a new email arrives (V3)":
- Folder, To, From, CC, Importance, Include Attachments, Subject Filter
</parameters>

<outputs>
Same output structure as "When a new email arrives (V3)"
</outputs>

<limitations>
<limitation id="lim-trig-006" severity="critical">
**Full Access Required**: Won't work unless user has full access to shared mailbox
- Send-As permissions are NOT sufficient
- Recommendation: Grant Full Access in Exchange Admin Center
</limitation>

<limitation id="lim-trig-007" severity="high">
**Intermittent Triggering**: Flow may trigger for both older emails and latest emails moved to another folder
- Known issue with shared mailbox webhook subscriptions
- Recommendation: Implement timestamp filtering to ignore old emails
</limitation>

<limitation id="lim-trig-008" severity="medium">
**Permission Replication Delay**: Permissions may take up to 2 hours to replicate
- After granting access, wait 2 hours before testing
- Recommendation: Plan ahead when setting up new shared mailbox flows
</limitation>
</limitations>

<best_practices>
- **Permissions Verification**: Verify Full Access before deploying flow
- **Age Filtering**: Add condition to filter emails older than X minutes
- **Group vs Shared**: Do NOT use Microsoft 365 Group addresses; shared mailboxes only
- **User-to-User Sharing**: For user-to-user shared mailboxes, Full Access required
</best_practices>

<example>
```json
{
  "OriginalMailboxAddress": "support@contoso.com",
  "Folder": "Inbox",
  "SubjectFilter": "Support Request",
  "IncludeAttachments": false
}
```

**Use Case**: Automated support ticket creation from shared support mailbox
</example>

</trigger>

---

### When a New Email Mentioning Me Arrives (V3)

<trigger id="trigger-003" type="webhook" frequency="real-time" latency="seconds">

<trigger_header>
**Type**: Webhook (Real-time)
**Frequency**: Instant notification
**Latency**: 1-10 seconds typical
**Operation ID**: OnNewEmailMentionedV3
**Status**: Current
</trigger_header>

<description>
Triggers when an email arrives where the current user is @mentioned in the message body. Requires email to use Outlook's @mention feature. Supports same filtering options as standard email trigger.
</description>

<parameters>
#### Optional Parameters
Same as "When a new email arrives (V3)":
- Folder, To, From, CC, Importance, Include Attachments, Subject Filter
</parameters>

<outputs>
Same output structure as "When a new email arrives (V3)" with additional mention context
</outputs>

<best_practices>
- **Mention Validation**: Verify @mention format in condition before processing
- **Priority Routing**: Use for important email routing requiring personal attention
- **Notification**: Send immediate notification for @mentioned emails
</best_practices>

<example>
**Use Case**: Send Teams notification when mentioned in important email thread
</example>

</trigger>

---

### When an Email is Flagged (V4)

<trigger id="trigger-004" type="webhook" frequency="real-time" latency="seconds">

<trigger_header>
**Type**: Webhook (Real-time)
**Frequency**: Instant notification
**Latency**: 1-10 seconds typical
**Operation ID**: OnEmailFlaggedV4
**Status**: Current
</trigger_header>

<description>
Triggers when an email is flagged for follow-up or when a flagged email is received. Also triggers when already-flagged email is modified in any way. Useful for task creation and follow-up automation.
</description>

<parameters>
#### Optional Parameters
Similar filtering to standard email trigger
</parameters>

<outputs>
Same structure as new email trigger with flag status information
</outputs>

<limitations>
<limitation id="lim-trig-009" severity="medium">
**Multiple Triggers Per Email**: Triggers on flag action, receiving flagged email, AND modifying flagged email
- May cause duplicate flow runs for same email
- Recommendation: Implement deduplication using message ID and timestamp
</limitation>
</limitations>

<best_practices>
- **Task Creation**: Auto-create tasks in planner/to-do when email flagged
- **Deduplication**: Track processed message IDs to avoid duplicate processing
- **Flag Status**: Check flag status in flow logic
</best_practices>

<example>
**Use Case**: Create Planner task when email flagged for follow-up
</example>

</trigger>

---

## Calendar Triggers

### When a New Event is Created (V3)

<trigger id="trigger-005" type="webhook" frequency="real-time" latency="seconds">

<trigger_header>
**Type**: Webhook (Real-time)
**Frequency**: Instant notification
**Latency**: 1-10 seconds typical
**Operation ID**: OnNewEventV3
**Status**: Current
</trigger_header>

<description>
Triggers when a new calendar event is created in the user's calendar. Monitors event creation including meeting invitations accepted. Uses webhook for real-time notification.
</description>

<parameters>
#### Optional Parameters

**Calendar ID** (`string`)
- **Description**: Specific calendar to monitor
- **Default**: Primary calendar
- **Format**: Calendar ID or name
</parameters>

<outputs>
**Trigger Output Structure**:
```json
{
  "Id": "AAMkAGVmMDEz...",
  "Subject": "Team Meeting",
  "Start": {
    "DateTime": "2025-11-01T10:00:00",
    "TimeZone": "Pacific Standard Time"
  },
  "End": {
    "DateTime": "2025-11-01T11:00:00",
    "TimeZone": "Pacific Standard Time"
  },
  "Location": "Conference Room A",
  "Organizer": {
    "EmailAddress": {
      "Name": "John Doe",
      "Address": "john@contoso.com"
    }
  },
  "Attendees": [],
  "IsAllDay": false,
  "IsCancelled": false,
  "Importance": "Normal"
}
```

**Key Fields**:
- **Id**: Event identifier for subsequent operations
- **Subject**: Event title
- **Start/End**: Event date/time with timezone
- **Organizer**: Event creator information
- **Attendees**: List of invited attendees
</outputs>

<limitations>
<limitation id="lim-trig-010" severity="medium">
**Accepted Invitations Trigger Twice**: When accepting meeting invitation, trigger fires again
- First: When invitation received
- Second: When user accepts invitation
- Recommendation: Check event status or implement deduplication
</limitation>
</limitations>

<best_practices>
- **Meeting Automation**: Auto-prepare meeting rooms/resources
- **Notification**: Send reminders or prepare materials
- **Integration**: Create related items in project management systems
</best_practices>

<example>
**Use Case**: Automatically book conference room resources when team meeting created
</example>

</trigger>

---

### When an Event is Added, Updated or Deleted (V3)

<trigger id="trigger-006" type="webhook" frequency="real-time" latency="seconds">

<trigger_header>
**Type**: Webhook (Real-time)
**Frequency**: Instant notification
**Latency**: 1-10 seconds typical
**Operation ID**: OnCalendarEventChangedV3
**Status**: Current
</trigger_header>

<description>
Triggers when any calendar event is created, modified, or deleted. Provides comprehensive calendar monitoring for all event changes. Includes change type in output for conditional processing.
</description>

<parameters>
#### Optional Parameters

**Calendar ID** (`string`)
- **Description**: Specific calendar to monitor
- **Default**: Primary calendar
</parameters>

<outputs>
Same as event created trigger with additional fields:
- **ChangeType**: "Created", "Updated", or "Deleted"
- **iCalUId**: Universal identifier for recurring events
</outputs>

<limitations>
<limitation id="lim-trig-011" severity="medium">
**Recurring Event Behavior**: Triggers on each occurrence of recurring event
- Single recurring event definition causes multiple triggers
- Recommendation: Use iCalUId to identify recurring event series
</limitation>

<limitation id="lim-trig-012" severity="medium">
**Outside Interval Triggers**: Events outside monitoring window may trigger with "Deleted" value
- Internal process cleanup triggers
- Recommendation: Filter by DateTimeReceived in flow logic
</limitation>

<limitation id="lim-trig-013" severity="low">
**Unnecessary Updates**: Trigger provides updates due to internal processes
- Not all triggers represent user-initiated changes
- Recommendation: Check LastModifiedDateTime changes
</limitation>
</limitations>

<best_practices>
- **Change Type Routing**: Use switch control on ChangeType for different logic paths
- **Recurring Events**: Handle recurring events specially using iCalUId
- **Deleted Events**: Implement cleanup logic for deleted events
- **Update Filtering**: Filter out non-meaningful updates
</best_practices>

<example>
**Use Case**: Sync calendar events to external system with create/update/delete handling
</example>

</trigger>

---

## General Trigger Limitations

<limitation id="lim-general-001" severity="high">
**API Rate Limit**: 300 calls per 60 seconds per connection
- Shared across all triggers and actions
- Recommendation: Monitor usage; implement throttling for high-volume scenarios
</limitation>

<limitation id="lim-general-002" severity="medium">
**Webhook Reliability**: Occasional missed webhook notifications (rare)
- Webhook infrastructure may experience transient failures
- Recommendation: Implement periodic reconciliation job for critical workflows
</limitation>

<limitation id="lim-general-003" severity="low">
**Shared Calendar IDs**: Each user has unique ID for shared calendars
- Calendar ID differs per user even for same shared calendar
- Recommendation: Use owner's connection for shared calendar flows
</limitation>

---

## Trigger Selection Guide

| Use Case | Recommended Trigger | Notes |
|----------|-------------------|-------|
| Process incoming emails | When a new email arrives (V3) | Use folder and subject filters |
| Monitor support mailbox | When a new email arrives in shared mailbox | Requires Full Access |
| Priority email notifications | When mentioned in email | @mention required |
| Follow-up automation | When email flagged | Creates tasks automatically |
| Meeting preparation | When event created | Auto-prepare resources |
| Calendar sync | When event added/updated/deleted | Comprehensive monitoring |

---

**Last Updated**: 2025-10-31
**Documentation Version**: 1.0
**Connector Version**: Current (as of 2025-10-31)
**Official Reference**: https://learn.microsoft.com/en-us/connectors/office365/
