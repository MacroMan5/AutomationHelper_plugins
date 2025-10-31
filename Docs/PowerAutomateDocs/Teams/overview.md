# Microsoft Teams Connector Overview

---
type: connector-overview
connector_name: Microsoft Teams
connector_type: standard
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [teams, chat, channel, message, notification, collaboration, adaptive card, mention]
related_connectors: [Office 365 Outlook, SharePoint, Office 365 Users]
api_limits:
  calls_per_minute: 1.67
  calls_per_hour: 100
  trigger_poll_frequency_seconds: 600
  non_get_requests_per_5min: 25
  max_message_size_kb: 28
official_docs_url: https://learn.microsoft.com/en-us/connectors/teams/
---

<official_docs>
https://learn.microsoft.com/en-us/connectors/teams/
</official_docs>

<description>
Microsoft Teams connector enables automation of Teams messaging, channel management, and collaboration workflows within Microsoft 365. Supports posting messages and adaptive cards to channels/chats, creating channels and teams, managing memberships, and triggering flows based on Teams activity with real-time notifications.
</description>

<capabilities>
## Core Capabilities
- Post messages and adaptive cards to channels and chats
- Create and manage Teams channels
- Add and remove team members
- Detect new messages, mentions, and reactions
- Post interactive adaptive cards with user responses
- Create group chats with up to 20 participants
- Send notifications as Flow bot

## Supported Operations
- **Messaging**: Post message in chat/channel, Post adaptive card, Reply to message, Get message details
- **Channel Management**: Create channel, List channels, Get channel details
- **Team Management**: Add member to team, Remove member, List teams, Get team details
- **Chat Operations**: Create chat, Add user to chat, List chat messages
- **Interactive**: Post choice of options as Flow bot, Wait for adaptive card response

## Integration Features
- Polling triggers for new messages (3-minute intervals)
- Adaptive Cards for interactive content
- @mention detection in channels
- Message reactions monitoring
- Flow bot for choice prompts
- HTML formatting support in messages
</capabilities>

<api_limits>
## Rate Limits

**Connection-Level Throttling**
- **100 API calls per 60 seconds** per connection
- Throttling scope: per connection
- Retry-After header: yes

**Trigger-Specific Limits**
- Trigger polling frequency: **1 call per 600 seconds** (10 minutes)
- New message check: **Every 3 minutes**

**Action-Specific Limits**
- Non-GET requests (Flow bot): **25 calls per 300 seconds** (5 minutes)
- Non-GET requests (other): **300 calls per 300 seconds** (5 minutes)
- Message size: **~28 KB maximum** including HTML

**Throttling Behavior**
- HTTP Status: 429 (Too Many Requests)
- Error message: "Rate limit exceeded"
- Automatic retry: yes

## Size Limits

**Message Operations**
- Max message size: **~28 KB** including all HTML elements
- Max users per chat creation: **20 users**
- No explicit limit on channel message length (subject to 28KB total)

**Adaptive Card Size**
- Recommended: Keep cards under 28KB for reliability
- Large cards may fail or be truncated

## Timeout Limits
- Default timeout: **120 seconds**
- Long-running operations: Not applicable for messaging
</api_limits>

<critical_limitations>
## Channel & Messaging Limitations

<limitation id="lim-001" severity="critical">
**Cannot Post to Private Channels**: Connector doesn't support private channel messaging

- **Impact**: Cannot automate messages to private channels
- **Scope**: All channel messaging actions
- **Workaround**: Use standard channels or direct chats instead
- **Affected Operations**: Post message in channel, Post adaptive card in channel
</limitation>

<limitation id="lim-002" severity="high">
**Replies Don't Trigger Channel Message Events**: Reply messages don't fire "When a new channel message is added" trigger

- **Impact**: Flows only trigger on root messages, not replies
- **Scope**: Channel message triggers
- **Workaround**: Use Get message details periodically or monitor replies separately
- **Affected Operations**: When a new channel message is added trigger
</limitation>

<limitation id="lim-003" severity="medium">
**3-Minute Trigger Polling Delay**: Triggers check for new messages every 3 minutes

- **Impact**: Up to 3-minute delay in detecting new messages
- **Scope**: All message-based triggers
- **Workaround**: None - polling frequency is fixed
- **Affected Operations**: All triggers (new message, new chat message, @mention)
</limitation>

<limitation id="lim-004" severity="medium">
**20-User Chat Limit**: Can only create chats with maximum 20 participants

- **Impact**: Cannot automate large group chat creation
- **Scope**: Create chat action
- **Workaround**: Use Teams channels for larger groups
- **Affected Operations**: Create a chat
</limitation>

## Adaptive Card Limitations

<limitation id="lim-005" severity="high">
**Workflows App Required for Actions**: Adaptive card actions require Workflows app enabled in Teams

- **Impact**: Cards with action buttons don't work if app not enabled
- **Scope**: Adaptive cards with Action.Submit buttons
- **Workaround**: Enable Workflows app in Teams admin center
- **Affected Operations**: Post adaptive card, When someone responds to adaptive card
</limitation>

<limitation id="lim-006" severity="medium">
**28KB Message Size Limit**: Messages including HTML cannot exceed ~28KB

- **Impact**: Large formatted messages or complex cards may fail
- **Scope**: All messaging actions
- **Workaround**: Simplify message content, split into multiple messages
- **Affected Operations**: Post message, Post adaptive card
</limitation>

## Connection Limitations

<limitation id="lim-007" severity="medium">
**Non-Shareable Connections**: Connections cannot be shared between users

- **Impact**: Each user must create own connection when apps shared
- **Scope**: All connection types
- **Workaround**: Document connection setup for all users
- **Affected Operations**: All operations
</limitation>

## Reaction Limitations

<limitation id="lim-008" severity="low">
**Emoji-Only Reaction Monitoring**: Can only monitor for emoji reactions

- **Impact**: Cannot detect custom reactions or other response types
- **Scope**: Message reaction triggers
- **Workaround**: Use standard emojis for automation triggers
- **Affected Operations**: When a reaction is added to a message
</limitation>
</critical_limitations>

<authentication>
## Supported Authentication Methods

### OAuth 2.0 (Only Method)
- Flow type: Authorization Code
- Required scopes: Group.ReadWrite.All, Chat.Create, Channel.Create, TeamMember.ReadWrite.All
- Token refresh: Automatic
- Account type: Organizational accounts only (Azure AD)

### Connection Types
1. **Default**: All regions except Government clouds
2. **Microsoft Teams Credentials (GCC)**: Government Cloud
3. **Microsoft Teams Credentials (GCC High)**: High-security government environments

### Service Principal
- Supported: Limited (some operations support app permissions)
- Note: Most operations require user context

## Required Permissions

### Delegated Permissions (User Context)
- **Group.ReadWrite.All**: Manage teams and channels
- **Chat.Create**: Create chats and send messages
- **Channel.Create**: Create channels in teams
- **TeamMember.ReadWrite.All**: Manage team memberships
- **ChannelMessage.Send**: Send messages to channels

### Application Permissions (App-Only Context)
- Limited support - most operations require user delegation
</authentication>

<common_use_cases>
## 1. Automated Notifications

**Description**: Send notifications to Teams channels for business events

**Typical Flow**:
```
Trigger: When item created (SharePoint/Forms)
↓
Action 1: Get item details
↓
Action 2: Post message in channel - Notify team
↓
Result: Real-time Teams notifications
```

**Key Actions**: Post message in a chat or channel
**Best For**: Alerts, status updates, event notifications

---

## 2. Interactive Approvals with Adaptive Cards

**Description**: Request approvals via interactive adaptive cards in Teams

**Typical Flow**:
```
Trigger: When item created (Request list)
↓
Action 1: Post adaptive card - Display approval request
↓
Action 2: When someone responds to adaptive card - Wait for response
↓
Action 3: Update item - Record decision
↓
Result: Teams-based approval workflow
```

**Key Actions**: Post adaptive card, When someone responds to adaptive card
**Best For**: Approvals, surveys, feedback collection

---

## 3. Channel Creation for Projects

**Description**: Automatically create Teams channels for new projects

**Typical Flow**:
```
Trigger: When item created (Projects list)
↓
Action 1: Create channel - New project channel
↓
Action 2: Add members - Project team members
↓
Action 3: Post message - Welcome and instructions
↓
Result: Automated project workspace setup
```

**Key Actions**: Create a channel, Add a member to a team, Post message
**Best For**: Project onboarding, workspace provisioning

---

## 4. Mention-Based Workflow Triggers

**Description**: Trigger workflows when @mentioned in Teams

**Typical Flow**:
```
Trigger: When I am mentioned in a channel message
↓
Action 1: Get message details - Extract context
↓
Action 2: Parse message - Identify request type
↓
Action 3: Perform action - Execute requested operation
↓
Action 4: Reply to message - Confirm completion
↓
Result: Conversational automation via @mentions
```

**Key Actions**: When mentioned trigger, Get message details, Reply to message
**Best For**: Bot-like interactions, help desk automation

---

## 5. Group Chat Creation for Events

**Description**: Create group chats for event participants

**Typical Flow**:
```
Trigger: When item created (Event registration)
↓
Action 1: Get attendees - List participants
↓
Action 2: Create chat - Group chat with attendees
↓
Action 3: Post message - Event details and instructions
↓
Result: Automated event communication setup
```

**Key Actions**: Create a chat, Post message in chat
**Best For**: Event coordination, team assembly, project kickoffs
</common_use_cases>

<best_practices>
## Performance Optimization

### API Call Efficiency
1. **Batch Notifications**: Send single message with multiple @mentions instead of multiple messages
2. **Cache Team/Channel IDs**: Store IDs in variables to avoid repeated lookups
3. **Use Adaptive Cards Wisely**: Cards consume more API calls than simple messages

### Throttling Management
1. **Add Delays**: Insert 2-3 second delays between Teams operations in loops
2. **Limit Flow Bot Usage**: Flow bot has stricter limits (25 calls per 5 minutes)
3. **Monitor Non-GET Requests**: Track action calls to stay under limits

## Reliability & Error Handling

### Retry Logic
1. **Retry on 429**: Implement exponential backoff for throttling
2. **Handle Network Failures**: Configure automatic retry for transient errors

### Message Validation
1. **Check Message Size**: Validate content under 28KB before sending
2. **Test Adaptive Cards**: Validate card JSON before deploying

## Security Best Practices

### Message Security
1. **Sanitize User Input**: Validate/sanitize data before including in messages
2. **Avoid Sensitive Data**: Don't post sensitive info to public channels
3. **Use Private Chats**: For confidential communications use 1:1 or group chats

### Permission Management
1. **Limit Bot Permissions**: Grant minimum necessary permissions
2. **Use Service Accounts**: Dedicated accounts for automated messaging

## Flow Design

### Messaging Best Practices
1. **Format with Markdown**: Use markdown for readable messages
2. **Include Context**: Always provide relevant context in notifications
3. **Test Card Rendering**: Verify adaptive cards display correctly

### Adaptive Card Design
1. **Keep Cards Simple**: Avoid overly complex cards (28KB limit)
2. **Provide Clear Actions**: Label buttons clearly for user understanding
3. **Handle Timeouts**: Implement fallback for cards without responses

### Channel Management
1. **Use Standard Channels**: Avoid private channels (not supported)
2. **Verify Team Membership**: Check user is team member before operations
3. **Handle Channel Limits**: Teams has limits on channels per team
</best_practices>

<troubleshooting>
## Common Errors

### Throttling Errors (429)
<error id="err-429" http_code="429">
- **Symptom**: "Rate limit exceeded" or "Too many requests"
- **Cause**: Exceeded 100 calls per 60 seconds or Flow bot limit (25 per 5 minutes)
- **Fix**: Add delays, reduce frequency, use standard actions instead of Flow bot
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
- **Cause**: User lacks required Teams permissions (e.g., not team member)
- **Fix**: Add user to team, grant necessary permissions
</error>

### Private Channel Errors
<error id="err-private-channel" http_code="400">
- **Symptom**: "Cannot post to private channel" or operation fails
- **Cause**: Attempting to post to private channel (not supported)
- **Fix**: Use standard channel or direct chat instead
- **Reference**: [Limitation lim-001](#lim-001)
</error>

### Message Size Errors
<error id="err-size" http_code="413">
- **Symptom**: "Message too large" or content truncated
- **Cause**: Message exceeds ~28KB limit
- **Fix**: Simplify message, remove excess HTML, split into multiple messages
- **Reference**: [Limitation lim-006](#lim-006)
</error>

### Adaptive Card Errors
<error id="err-card" http_code="400">
- **Symptom**: "Invalid adaptive card" or card doesn't render
- **Cause**: Invalid card JSON, Workflows app not enabled, or card too large
- **Fix**: Validate JSON, enable Workflows app, reduce card complexity
- **Reference**: [Limitation lim-005](#lim-005)
</error>
</troubleshooting>

<related_docs>
## Documentation Structure

- **Actions**: [actions.md](./actions.md) - All available actions (to be created)
- **Triggers**: [triggers.md](./triggers.md) - Available triggers (to be created)

## Related Connectors

- **Office 365 Outlook**: Send emails alongside Teams notifications
- **SharePoint**: Integrate Teams notifications with SharePoint workflows
- **Office 365 Users**: Lookup user info for @mentions and chat creation
- **Planner**: Manage tasks mentioned in Teams messages

## External Resources

- **Official Documentation**: https://learn.microsoft.com/en-us/connectors/teams/
- **Adaptive Cards Designer**: https://adaptivecards.io/designer/
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
