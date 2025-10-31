# Microsoft Teams - Triggers

---
type: connector-triggers
connector_name: Microsoft Teams
trigger_count: 12
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [teams, message, channel, chat, mention, reaction, adaptive card, trigger, webhook, polling]
trigger_types: [webhook, polling, instant]
---

<trigger_summary>
**Total Triggers**: 12

**Types**:
- Polling: 8 triggers (3-10 minute intervals)
- Instant/Manual: 2 triggers (Power Automate only)
- Webhook: 2 triggers (message-based)

**Categories**:
- Message Triggers: 6 (new message, mentions, keywords, reactions)
- Member Triggers: 2 (member added/removed)
- Instant Triggers: 2 (selected message, compose box)
- Adaptive Card: 2 (response triggers)

**Polling Frequency**: 3-minute interval for channel messages; 5-minute for member changes
</trigger_summary>

---

## Message Triggers

### When a New Channel Message is Added

<trigger id="trigger-001" type="polling" frequency="3-minutes" latency="3-10-minutes">

<trigger_header>
**Type**: Polling
**Frequency**: 3-minute polling interval (10-minute actual interval)
**Latency**: 3-10 minutes
**Operation ID**: OnNewChannelMessage
**Status**: Current
</trigger_header>

<description>
Triggers when a new message is posted to a channel in a team. Only fires for root messages; replies do not trigger. Uses polling mechanism with 3-minute check interval.
</description>

<parameters>
#### Required Parameters

**Team** (`string`)
- **Description**: Select team to monitor
- **Format**: Dynamic dropdown of available teams

**Channel** (`string`)
- **Description**: Channel ID to monitor
- **Format**: Dynamic dropdown of channels in selected team
</parameters>

<outputs>
**Trigger Output**:
```json
{
  "messageId": "1234567890",
  "body": {
    "content": "Message content here",
    "contentType": "html"
  },
  "from": {
    "user": {
      "displayName": "John Doe",
      "id": "user-guid"
    }
  },
  "createdDateTime": "2025-10-31T14:30:00Z",
  "importance": "normal",
  "mentions": [],
  "reactions": []
}
```

**Key Fields**:
- **messageId**: Unique identifier for message
- **content**: Message text (HTML format)
- **from**: Sender information
- **createdDateTime**: Message timestamp
- **mentions**: Array of @mentioned users
- **reactions**: Array of reactions (likes, etc.)
</outputs>

<limitations>
<limitation id="lim-trigger-001" severity="high">
**Root Messages Only**: Only fires for new root messages, not replies
- Replies to existing messages don't trigger flow
- Workaround: Use separate monitoring for reply detection
</limitation>

<limitation id="lim-trigger-002" severity="medium">
**Polling Interval**: 3-minute polling (10-minute actual interval)
- Not real-time; expect 3-10 minute delay
- Recommendation: Set user expectations for latency
</limitation>

<limitation id="lim-trigger-003" severity="medium">
**Shared Channels**: For shared channels, team ID must reference host team
- Channel may appear in multiple teams
- Requirement: Use host team (team that owns channel)
</limitation>
</limitations>

<best_practices>
- **Specific Channels**: Monitor specific channels, not all channels
- **Filter Content**: Add conditions to filter relevant messages
- **Deduplication**: Check message ID to avoid duplicate processing
- **Error Handling**: Handle cases where message deleted before processing
</best_practices>

<example>
**Use Case**: Monitoring project channel for status updates, auto-creating tasks from messages with specific keywords
</example>

</trigger>

---

### When a New Chat Message is Added

<trigger id="trigger-002" type="webhook" frequency="real-time" latency="seconds">

<trigger_header>
**Type**: Webhook (Real-time)
**Frequency**: Instant notification
**Latency**: Seconds
**Operation ID**: OnNewChatMessage
**Status**: Current
</trigger_header>

<description>
Triggers when a new message is posted in any chat the user is part of. Uses webhook for real-time delivery. Supports only one user per flow.
</description>

<parameters>
No required configuration parameters (monitors all chats for authenticated user)
</parameters>

<outputs>
Similar to channel message output with chat-specific context
</outputs>

<limitations>
<limitation id="lim-trigger-004" severity="high">
**Single User Only**: Supports only one user per flow
- Cannot monitor multiple users' chats in single flow
- Requirement: Separate flows for each user
</limitation>

<limitation id="lim-trigger-005" severity="medium">
**All Chats Monitored**: Monitors ALL chats user is part of
- No filtering by specific chat
- Recommendation: Add conditions to filter relevant chats
</limitation>
</limitations>

<best_practices>
- **Chat Filtering**: Filter by chat name or participants
- **Personal vs Group**: Differentiate between 1:1 and group chats
- **Content Filtering**: Use subject/content conditions
</best_practices>

<example>
**Use Case**: Auto-responding to customer inquiries in dedicated support chats
</example>

</trigger>

---

### When a New Message is Added to a Chat or Channel

<trigger id="trigger-003" type="webhook" frequency="real-time" latency="seconds">

<trigger_header>
**Type**: Webhook (Real-time)
**Frequency**: Instant notification
**Latency**: Seconds
**Operation ID**: OnNewMessageInChatOrChannel
**Status**: Current
</trigger_header>

<description>
Triggers when new message posted in specified chat or channel. Does not trigger if message is edited. Flexible trigger supporting both chats and channels.
</description>

<parameters>
#### Required Parameters

**Message Type** (`string`)
- **Description**: Type of message source
- **Values**: Channel message, Chat message

**Request Body** (`dynamic`)
- **Description**: Dynamic webhook request body
- **Format**: Configuration based on message type
</parameters>

<limitations>
<limitation id="lim-trigger-006" severity="medium">
**No Edit Triggers**: Does not trigger when message edited
- Only new message creation triggers flow
- Workaround: Use polling with timestamp tracking for edit detection
</limitation>
</limitations>

</trigger>

---

### When I'm @Mentioned

<trigger id="trigger-004" type="webhook" frequency="real-time" latency="seconds">

<trigger_header>
**Type**: Webhook (Real-time)
**Frequency**: Instant notification
**Latency**: Seconds
**Operation ID**: OnIMentioned
**Status**: Current
</trigger_header>

<description>
Triggers when current user is @mentioned in a specified chat or channel. Real-time notification for personal mentions requiring attention or response.
</description>

<parameters>
#### Required Parameters

**Message Type** (`string`)
- **Values**: Channel message, Chat message

**Request Body** (`dynamic`)
- **Description**: Configuration for mention monitoring
</parameters>

<best_practices>
- **Priority Notifications**: Send immediate alerts for @mentions
- **Response Tracking**: Auto-track items requiring response
- **Escalation**: Route urgent mentions to appropriate channels
</best_practices>

<example>
**Use Case**: Send mobile notification when @mentioned in important project channel
</example>

</trigger>

---

### When I am Mentioned in a Channel Message

<trigger id="trigger-005" type="polling" frequency="3-minutes" latency="3-10-minutes">

<trigger_header>
**Type**: Polling
**Frequency**: 3-minute polling interval
**Latency**: 3-10 minutes
**Operation ID**: OnIMentionedInChannelMessage
**Status**: Current
</trigger_header>

<description>
Triggers when current user @mentioned in channel within a team. Polling-based variant with team/channel specificity.
</description>

<parameters>
#### Required Parameters

**Team** (`string`)
- **Description**: Team to monitor

**Channel** (`string`)
- **Description**: Channel to monitor for mentions
</parameters>

<best_practices>
- **Specific Monitoring**: Use for specific channel mention tracking
- **Polling Delay**: Account for 3-10 minute latency
- **Webhook Alternative**: Consider webhook-based mention trigger for real-time
</best_practices>

</trigger>

---

### When Keywords Are Mentioned

<trigger id="trigger-006" type="webhook" frequency="real-time" latency="seconds">

<trigger_header>
**Type**: Webhook (Real-time)
**Frequency**: Instant notification
**Latency**: Seconds
**Operation ID**: OnKeywordsMentioned
**Status**: Current
</trigger_header>

<description>
Triggers when specific keyword mentioned in chat or channel. Does not trigger if message edited. Useful for monitoring specific topics or alerts.
</description>

<parameters>
#### Required Parameters

**Message Type** (`string`)
- **Values**: Channel message, Chat message

**Keywords to Search For** (`string`)
- **Description**: Comma-separated list of keywords
- **Format**: "keyword1,keyword2,keyword3"
- **Important**: Only single-word keywords supported

**Request Body** (`dynamic`)
- **Description**: Configuration for keyword monitoring
</parameters>

<limitations>
<limitation id="lim-trigger-007" severity="high">
**Single-Word Keywords Only**: Phrases longer than one word won't trigger
- "urgent" works, "urgent request" doesn't
- Workaround: Use multiple single-word keywords; filter in flow
</limitation>

<limitation id="lim-trigger-008" severity="medium">
**No Edit Triggers**: Doesn't trigger when message edited to add keyword
- Only triggers on new message creation
</limitation>
</limitations>

<best_practices>
- **Multiple Keywords**: Use comma-separated keywords for variations
- **Case Sensitivity**: Verify keyword matching behavior
- **Content Filtering**: Add flow conditions for phrase matching
- **Alert Categories**: Group keywords by topic/priority
</best_practices>

<example>
```json
{
  "MessageType": "Channel message",
  "KeywordsToSearchFor": "urgent,critical,emergency,blocked"
}
```

**Use Case**: Monitoring project channels for urgent issues requiring immediate attention
</example>

</trigger>

---

### When Someone Reacted to a Message in Chat

<trigger id="trigger-007" type="webhook" frequency="real-time" latency="seconds">

<trigger_header>
**Type**: Webhook (Real-time)
**Frequency**: Instant notification
**Latency**: Seconds
**Operation ID**: OnMessageReaction
**Status**: Current
</trigger_header>

<description>
Triggers when someone reacts to a message in chat or channel. Configurable to track specific emoji and trigger frequency (every reaction or first only).
</description>

<parameters>
#### Required Parameters

**Emoji to Track** (`string`)
- **Description**: Specific emoji to monitor
- **Example**: "👍", "❤️", "😊"

**Trigger Frequency** (`string`)
- **Description**: When to trigger
- **Values**: "Every reaction", "First reaction only"

**Who Can Trigger** (`string`)
- **Description**: User scope for triggering
- **Values**: "Anyone", "Specific users"

**Message Type** (`string`)
- **Values**: Channel message, Chat message

**Request Body** (`dynamic`)
- **Description**: Reaction monitoring configuration
</parameters>

<best_practices>
- **Voting Mechanisms**: Use reactions for simple approval/voting
- **Sentiment Tracking**: Monitor reaction patterns
- **First Reaction**: Use "First only" to avoid duplicate processing
- **Specific Users**: Limit to relevant users (e.g., managers for approvals)
</best_practices>

<example>
**Use Case**: Using thumbs-up reactions as approval mechanism for quick decisions
</example>

</trigger>

---

## Member Triggers

### When a New Team Member is Added

<trigger id="trigger-008" type="polling" frequency="5-minutes" latency="5-15-minutes">

<trigger_header>
**Type**: Polling
**Frequency**: 5-minute polling interval
**Latency**: 5-15 minutes
**Operation ID**: OnNewTeamMember
**Status**: Current
</trigger_header>

<description>
Triggers when member added to team. Uses polling mechanism with 5-minute interval. May fire multiple times for same event.
</description>

<parameters>
#### Required Parameters

**Team** (`string`)
- **Description**: Team to monitor for new members
</parameters>

<outputs>
**Trigger Output**:
```json
{
  "UserId": "user-guid-here"
}
```

**Key Field**:
- **UserId**: Unique identifier of added user
</outputs>

<limitations>
<limitation id="lim-trigger-009" severity="medium">
**Multiple Triggers**: May fire multiple times for same member addition event
- Expected behavior with polling
- Recommendation: Implement deduplication logic
</limitation>

<limitation id="lim-trigger-010" severity="medium">
**Unified Groups with Hidden Members**: Doesn't work on unified groups with hidden member settings
- Requirement: Standard teams with visible members
</limitation>

<limitation id="lim-trigger-011" severity="low">
**Polling Delay**: 5-15 minute latency for new member detection
- Not suitable for immediate onboarding workflows
</limitation>
</limitations>

<best_practices>
- **Onboarding**: Send welcome messages to new members
- **Provisioning**: Trigger access provisioning workflows
- **Deduplication**: Track processed user IDs to avoid duplicates
- **User Info**: Use Office 365 Users connector to get member details
</best_practices>

<example>
**Use Case**: Automated onboarding - send welcome message and training materials to new team members
</example>

</trigger>

---

### When a New Team Member is Removed

<trigger id="trigger-011" type="polling" frequency="5-minutes" latency="5-15-minutes">

<trigger_header>
**Type**: Polling
**Frequency**: 5-minute polling interval
**Latency**: 5-15 minutes
**Operation ID**: OnTeamMemberRemoved
**Status**: Current
</trigger_header>

<description>
Triggers when member removed from team. Polling-based with 5-minute interval. May fire multiple times.
</description>

<parameters>
#### Required Parameters

**Team** (`string`)
- **Description**: Team to monitor for member removal
</parameters>

<outputs>
```json
{
  "UserId": "user-guid-here"
}
```
</outputs>

<limitations>
Same limitations as member added trigger
</limitations>

<best_practices>
- **Deprovisioning**: Trigger access removal workflows
- **Archival**: Archive user's team content
- **Notifications**: Notify team of member departure
- **Deduplication**: Track processed removals
</best_practices>

<example>
**Use Case**: Automated offboarding - revoke access and transfer ownership when member removed
</example>

</trigger>

---

## Adaptive Card & Instant Triggers

### When Someone Responds to an Adaptive Card

<trigger id="trigger-009" type="webhook" frequency="real-time" latency="immediate">

<trigger_header>
**Type**: Webhook (Real-time)
**Frequency**: Immediate
**Latency**: Immediate
**Operation ID**: OnAdaptiveCardResponse
**Status**: Current
**Availability**: Default environment only
</trigger_header>

<description>
Handles responses for adaptive card posted in Teams. Captures user input from adaptive card actions (buttons, input fields). Requires Workflows app.
</description>

<parameters>
No configuration required (dynamic based on adaptive card schema)
</parameters>

<outputs>
Dynamic output based on adaptive card input fields
</outputs>

<limitations>
<limitation id="lim-trigger-012" severity="critical">
**Default Environment Only**: Works only in default Power Automate environment
- Not supported in non-default environments
- Requirement: Flow must be in default environment
</limitation>

<limitation id="lim-trigger-013" severity="high">
**Guest/External Users Not Supported**: Doesn't work for guest or external users
- Internal organization users only
- Limitation: Multi-tenant scenarios not supported
</limitation>

<limitation id="lim-trigger-014" severity="high">
**Sovereign Clouds Not Supported**: Unsupported in GCC, GCCH, DoD environments
- Commercial cloud only
- Requirement: Commercial Microsoft 365 tenant
</limitation>

<limitation id="lim-trigger-015" severity="medium">
**Workflows App Required**: Requires Microsoft Power Automate Actions app (Workflows)
- Must be installed in Teams
- Automatic installation in most cases
</limitation>
</limitations>

<best_practices>
- **Approval Workflows**: Use for approval/rejection with adaptive cards
- **Form Collection**: Collect structured input via adaptive cards
- **Cannot Combine**: Cannot use with "Post adaptive card and wait for response" action in same flow
- **Validation**: Validate user inputs before processing
</best_practices>

<example>
**Use Case**: Collecting feedback via adaptive card form when team meeting ends
</example>

</trigger>

---

### For a Selected Message (V2)

<trigger id="trigger-010" type="instant" frequency="manual" latency="immediate">

<trigger_header>
**Type**: Instant (Manual)
**Frequency**: User-initiated
**Latency**: Immediate
**Operation ID**: OnSelectedMessage
**Status**: Current
**Availability**: Power Automate only (default environment)
</trigger_header>

<description>
Starts flow for a selected message in Microsoft Teams. User right-clicks message and selects flow from context menu. Provides message content and context as trigger output.
</description>

<parameters>
#### Configuration Parameters

**operationId** (`string`, required)
- Auto-configured operation identifier

**host, parameters, schema** (required)
- Auto-configured based on flow setup
</parameters>

<outputs>
Dynamic object containing selected message content and metadata
</outputs>

<limitations>
<limitation id="lim-trigger-016" severity="critical">
**Power Automate Only**: Not available in Power Apps
- Instant cloud flows only
</limitation>

<limitation id="lim-trigger-017" severity="high">
**Default Environment Only**: Works only in default environment
</limitation>

<limitation id="lim-trigger-018" severity="high">
**Workflows App Required**: Requires Power Automate Actions app in Teams
</limitation>

<limitation id="lim-trigger-019" severity="high">
**Guest/External Users Not Supported**: Internal users only
</limitation>

<limitation id="lim-trigger-020" severity="high">
**Sovereign Clouds Not Supported**: GCC, GCCH, DoD unsupported
</limitation>
</limitations>

<best_practices>
- **Message Actions**: Create actions like "Save to OneNote", "Create Task", "Translate"
- **User Experience**: Clear flow names so users understand action
- **Confirmation**: Provide feedback after flow execution
- **Error Handling**: Graceful failure with user notification
</best_practices>

<example>
**Use Case**: "Create Planner Task from Message" - user selects message, flow creates task with message content
</example>

</trigger>

---

### From the Compose Box (V2)

<trigger id="trigger-012" type="instant" frequency="manual" latency="immediate">

<trigger_header>
**Type**: Instant (Manual)
**Frequency**: User-initiated
**Latency**: Immediate
**Operation ID**: FromComposeBox
**Status**: Current
**Availability**: Power Automate only
</trigger_header>

<description>
Starts flow from compose message box in Teams. User types message, then selects flow before sending. Enables message preprocessing or dynamic message generation.
</description>

<parameters>
Auto-configured parameters for compose box integration
</parameters>

<outputs>
Message content and compose context
</outputs>

<limitations>
Same as "For a selected message" (default environment, Power Automate only, Workflows app required, no guest/external users, sovereign clouds not supported)
</limitations>

<best_practices>
- **Message Enhancement**: Add formatting, lookup data, translate
- **Templates**: Generate message from templates
- **Validation**: Check message content before sending
- **Integration**: Pull data from other systems into message
</best_practices>

<example>
**Use Case**: "Send Status Update" - user starts typing, flow fetches latest project status, generates formatted message
</example>

</trigger>

---

## General Trigger Limitations

<limitation id="lim-general-001" severity="high">
**API Rate Limit**: 100 calls per 60 seconds per connection
- Shared across all triggers and actions
- Recommendation: Monitor usage; implement throttling
</limitation>

<limitation id="lim-general-002" severity="high">
**Non-GET Throttling**: 25 non-GET calls per 300 seconds for List chats/Feed notifications
- Tighter limit for specific operations
- Recommendation: Avoid frequent polling
</limitation>

<limitation id="lim-general-003" severity="medium">
**Polling Frequency**: Minimum 1 call per 600 seconds (10 minutes) for triggers
- Cannot poll more frequently
- Actual interval may be longer (3-10 minutes typical)
</limitation>

<limitation id="lim-general-004" severity="low">
**Subscription Required**: Must have enabled Microsoft 365 Teams subscription
- Teams license required for all triggers
</limitation>

---

## Trigger Selection Guide

| Use Case | Recommended Trigger | Latency | Notes |
|----------|-------------------|---------|-------|
| Monitor channel messages | When new channel message | 3-10 min | Root messages only |
| Real-time chat monitoring | When new chat message | Seconds | All user chats |
| @Mention notifications | When I'm @mentioned | Seconds | Real-time alerts |
| Keyword monitoring | When keywords mentioned | Seconds | Single words only |
| Approval via reactions | When someone reacted | Seconds | Track specific emoji |
| Team onboarding | When member added | 5-15 min | Polling delay |
| Team offboarding | When member removed | 5-15 min | Polling delay |
| Adaptive card forms | When adaptive card response | Immediate | Default env only |
| Message actions | For selected message | Immediate | Manual trigger |
| Compose enhancement | From compose box | Immediate | Manual trigger |

---

**Last Updated**: 2025-10-31
**Documentation Version**: 1.0
**Connector Version**: Current (as of 2025-10-31)
**Official Reference**: https://learn.microsoft.com/en-us/connectors/teams/
