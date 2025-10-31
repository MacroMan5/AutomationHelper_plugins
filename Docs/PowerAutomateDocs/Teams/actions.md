# Microsoft Teams - Actions

---
type: connector-actions
connector_name: Microsoft Teams
action_count: 40
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [teams, message, channel, chat, adaptive card, post message, create channel, members, actions]
categories: [create, read, update, delete, utility]
---

<action_summary>
**Total Actions**: 40+ (25 current + 15+ deprecated)

**By Category**:
- Messaging: 15 actions (post, reply, get messages, post cards, adaptive cards)
- Team/Channel Management: 8 actions (create, list, get details)
- Member Management: 4 actions (add/remove members, list members)
- Tags: 4 actions (create, list, manage team tags)
- Utility: 9 actions (HTTP requests, @mention tokens, feed notifications)
- Deprecated: 15+ actions (replaced by newer versions)

**Complexity Distribution**:
- Low complexity: 18 actions
- Medium complexity: 15 actions
- High complexity: 7 actions

**Most Used Actions**:
1. Post message in a chat or channel
2. Post card in a chat or channel
3. Post adaptive card and wait for response
4. Create a channel
5. List messages
</action_summary>

<action_categories>
## Categories Overview

### Messaging Operations
Post messages, adaptive cards, and replies to channels and chats. Includes waiting for responses, retrieving messages, and managing message interactions.

### Team/Channel Management
Create and manage teams, channels, and chats. List and get details for organizational structures.

### Member Management
Add, remove, and list team members. Manage team membership and access.

### Tags
Create, list, and manage team tags for organizing and @mentioning groups of users.

### Utility Operations
Advanced operations including HTTP requests, @mention token generation, and feed notifications.
</action_categories>

---

## Messaging Operations

### Post Message in a Chat or Channel

<action id="action-001" category="create" complexity="medium" throttle_impact="medium">

<action_header>
**Operation Type**: Create
**Complexity**: Medium
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: PostMessageInChatOrChannel
</action_header>

<description>
Posts a message to a chat or channel. Can post as Flow bot or as authenticated user. Supports HTML formatting, @mentions, and rich content. Requires Workflows app installed in Teams. Most commonly used messaging action.
</description>

<parameters>
#### Required Parameters

**Post as** (`string`)
- **Description**: Identity to post message as
- **Values**: "Flow bot", "User"
- **Note**: User option posts as authenticated user

**Post in** (`string`)
- **Description**: Destination type
- **Values**: "Channel", "Chat", "Group chat"

**Post Message Request** (`dynamic`)
- **Description**: Dynamic request body with message details
- **Format**: Varies based on Post as and Post in selections
- **Key Fields**:
  - Team ID (for channels)
  - Channel ID (for channels)
  - Chat ID (for chats)
  - Message body (HTML supported)
  - Recipient (for Flow bot chats)

#### Message Body Fields (in dynamic request)

**Message** (`string`)
- **Description**: Message content
- **Format**: HTML or plain text
- **Example**: `<p>New order #12345 has been received!</p>`
- **@Mentions**: Use `Get an @mention token` action to create mention tokens

**Subject** (`string`, optional)
- **Description**: Message subject line
- **Usage**: Rarely used; most messages don't have subjects
</parameters>

<returns>
**Return Type**: ConversationResponse object

**Structure**:
```json
{
  "messageId": "1234567890",
  "messageLink": "https://teams.microsoft.com/l/message/...",
  "eTag": "version-identifier"
}
```

**Key Fields**:
- **messageId**: Unique identifier for posted message
- **messageLink**: Direct link to message in Teams
- **eTag**: Version identifier for message updates
</returns>

<limitations>
<limitation id="lim-action-001" severity="critical">
**Workflows App Required**: Requires Microsoft Power Automate Actions (Workflows) app installed
- Automatically installed for most tenants
- Manual installation needed if missing
</limitation>

<limitation id="lim-action-002" severity="high">
**Message Size Limit**: ~28 KB maximum message size
- Includes HTML formatting and content
- Recommendation: Keep messages concise; use attachments for large content
</limitation>

<limitation id="lim-action-003" severity="medium">
**Private Channels Not Supported**: Cannot post to private channels currently
- Standard and shared channels only
- Workaround: None available; use regular channels
</limitation>

<limitation id="lim-action-004" severity="medium">
**@Mention Limit**: Maximum 20 users and 20 tags per message
- Total combined limit
- Recommendation: Batch notifications if exceeding limit
</limitation>
</limitations>

<best_practices>
- **Post as User**: Use "User" for personalized messages from specific person
- **Post as Flow Bot**: Use "Flow bot" for automated notifications/alerts
- **HTML Formatting**: Use HTML for rich formatting (bold, lists, links)
- **@Mentions**: Use @mention tokens for user notifications
- **Error Handling**: Wrap in try-scope for failure handling
- **Size Management**: Keep messages under 20 KB for reliability
</best_practices>

<example>
**Scenario**: Post order notification to sales channel

```json
{
  "PostAs": "Flow bot",
  "PostIn": "Channel",
  "PostMessageRequest": {
    "teamId": "team-guid",
    "channelId": "channel-guid",
    "message": {
      "subject": "",
      "body": {
        "content": "<p><strong>New Order Received</strong></p><p>Order ID: ORD-2025-12345<br/>Customer: Contoso Inc<br/>Amount: $2,500.00</p><p>@[mention-token] - Please review and process.</p>"
      }
    }
  }
}
```

**Use Case**: Automated order notifications to sales team channel
</example>

</action>

---

### Post Card in a Chat or Channel

<action id="action-002" category="create" complexity="medium" throttle_impact="medium">

<action_header>
**Operation Type**: Create
**Complexity**: Medium
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: PostCardInChatOrChannel
</action_header>

<description>
Posts an adaptive card to chat or channel. Adaptive cards provide rich, interactive UI with buttons, input fields, images, and structured layouts. Use for forms, approvals, status updates, and interactive notifications.
</description>

<parameters>
#### Required Parameters

**Post as** (`string`)
- **Values**: "Flow bot", "User"

**Post in** (`string`)
- **Values**: "Channel", "Chat", "Group chat"

**Post Card Request** (`dynamic`)
- **Description**: Dynamic request body
- **Key Fields**:
  - Destination IDs (team/channel/chat)
  - Adaptive card JSON
  - Update message (optional)

**Adaptive Card JSON** (in request)
- **Format**: JSON adaptive card schema
- **Version**: 1.2 or compatible
- **Example**: `{"type": "AdaptiveCard", "body": [...], "actions": [...]}`
- **Designer**: Use Adaptive Card Designer for creation
</parameters>

<returns>
**Return Type**: ConversationResponse with card ID and link
</returns>

<limitations>
<limitation id="lim-action-005" severity="high">
**Workflows App Required**: Same as post message
</limitation>

<limitation id="lim-action-006" severity="high">
**Size Limit**: ~28 KB including card JSON
</limitation>

<limitation id="lim-action-007" severity="medium">
**Card Version**: Must use compatible adaptive card schema version
- Test cards in designer before deployment
- Unsupported features may cause rendering issues
</limitation>
</limitations>

<best_practices>
- **Adaptive Card Designer**: Use https://adaptivecards.io/designer/ to design cards
- **Testing**: Test cards in Teams before production deployment
- **Action Handling**: For interactive cards, use separate flow to handle responses
- **Versioning**: Use adaptive card version 1.2 for broad compatibility
- **Visual Hierarchy**: Use headings, spacing, and containers for clear layout
</best_practices>

<example>
**Adaptive Card JSON** for approval request:
```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.2",
  "body": [
    {
      "type": "TextBlock",
      "text": "Approval Request",
      "weight": "bolder",
      "size": "large"
    },
    {
      "type": "TextBlock",
      "text": "Purchase Order: PO-2025-456",
      "wrap": true
    },
    {
      "type": "TextBlock",
      "text": "Amount: $5,000",
      "wrap": true
    }
  ],
  "actions": [
    {
      "type": "Action.Submit",
      "title": "Approve",
      "data": {"action": "approve", "poId": "PO-2025-456"}
    },
    {
      "type": "Action.Submit",
      "title": "Reject",
      "data": {"action": "reject", "poId": "PO-2025-456"}
    }
  ]
}
```

**Use Case**: Approval requests with approve/reject buttons
</example>

</action>

---

### Post Adaptive Card and Wait for a Response

<action id="action-003" category="create" complexity="high" throttle_impact="high">

<action_header>
**Operation Type**: Create (with wait)
**Complexity**: High
**Throttling Impact**: High
**Premium**: No
**Operation ID**: PostAdaptiveCardAndWaitForResponse
</action_header>

<description>
Posts adaptive card and pauses flow until ANY user responds. Returns user response data for processing. Commonly used for approvals, surveys, and interactive forms requiring immediate action.
</description>

<parameters>
#### Required Parameters

**Post as** (`string`)
- **Values**: "Flow bot", "User"

**Post in** (`string`)
- **Values**: "Channel", "Chat", "Group chat"

**Flow Continuation Subscription Request** (`dynamic`)
- **Description**: Dynamic configuration with adaptive card JSON
- **Key Fields**:
  - Destination identifiers
  - Adaptive card JSON with submit actions
  - Update message after response (optional)
</parameters>

<returns>
**Return Type**: Dynamic based on adaptive card action data

**Structure**: Returns data object from card submit action

**Example**:
```json
{
  "data": {
    "action": "approve",
    "comments": "Approved for $5,000",
    "submittedBy": "john@contoso.com"
  },
  "responder": {
    "displayName": "John Doe",
    "email": "john@contoso.com",
    "id": "user-guid"
  }
}
```

**Access**: Use `body('Post_adaptive_card')?['data']?['action']` to get response values
</returns>

<limitations>
<limitation id="lim-action-008" severity="critical">
**Workflows App Required**: Requires Workflows app
</limitation>

<limitation id="lim-action-009" severity="critical">
**Cannot Combine with Response Trigger**: Cannot use with "When someone responds to adaptive card" trigger in same flow
- Use one or the other, not both
- Recommendation: Use this action for simple wait scenarios
</limitation>

<limitation id="lim-action-010" severity="high">
**ANY User Can Respond**: First response received wins
- Cannot restrict to specific users in action itself
- Workaround: Add condition to check responder after response
</limitation>

<limitation id="lim-action-011" severity="high">
**Flow Waits**: Flow execution pauses until response received
- Blocking operation
- Timeout: Default flow timeout applies (30 days max)
</limitation>

<limitation id="lim-action-012" severity="medium">
**Single Response Only**: Only first response captured
- Subsequent responses ignored
- Workaround: Update card after response to indicate completion
</limitation>
</limitations>

<best_practices>
- **Response Validation**: Add conditions to validate responder identity/role
- **Timeout**: Set appropriate flow timeout for expected response time
- **Update Message**: Provide update message thanking responder
- **Multiple Approvers**: For multi-stage approval, use separate flows or trigger approach
- **Card Design**: Make submit actions clear and obvious
- **Data Structure**: Include all needed data in action.data object
</best_practices>

<example>
**Scenario**: Approval workflow with single approver

**Adaptive Card** (simplified):
```json
{
  "type": "AdaptiveCard",
  "version": "1.2",
  "body": [
    {
      "type": "TextBlock",
      "text": "Expense Approval Request",
      "weight": "bolder"
    },
    {
      "type": "Input.Text",
      "id": "comments",
      "placeholder": "Add comments"
    }
  ],
  "actions": [
    {
      "type": "Action.Submit",
      "title": "Approve",
      "data": {"action": "approve"}
    },
    {
      "type": "Action.Submit",
      "title": "Reject",
      "data": {"action": "reject"}
    }
  ]
}
```

**Flow Logic**:
1. Post adaptive card and wait for response
2. Flow pauses
3. User clicks Approve or Reject
4. Flow resumes with response data
5. Condition: If action = "approve" → Process approval
6. Else → Process rejection

**Use Case**: Single-stage approval workflows with immediate decision
</example>

</action>

---

### Reply with a Message in a Channel

<action id="action-004" category="create" complexity="medium" throttle_impact="medium">

<action_header>
**Operation Type**: Create
**Complexity**: Medium
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: ReplyWithMessageInChannel
</action_header>

<description>
Replies to an existing message in a channel, creating a threaded conversation. Maintains message context and thread organization. Use for responding to notifications, questions, or updates.
</description>

<parameters>
#### Required Parameters

**Post as** (`string`)
- **Values**: "Flow bot", "User"

**Post in** (`string`)
- **Values**: "Channel" (chats don't support threaded replies)

**Reply Message Request** (`dynamic`)
- **Key Fields**:
  - Team ID
  - Channel ID
  - Parent Message ID (message to reply to)
  - Reply content
</parameters>

<returns>
**Return Type**: ConversationResponse with reply message details
</returns>

<limitations>
<limitation id="lim-action-013" severity="high">
**Workflows App Required**: Same requirement
</limitation>

<limitation id="lim-action-014" severity="medium">
**Channel Only**: Only works for channel messages, not chats
- Chats don't support threaded replies in same way
- Recommendation: Use regular post message for chat responses
</limitation>

<limitation id="lim-action-015" severity="medium">
**Size Limit**: ~28 KB message size limit
</limitation>
</limitations>

<best_practices>
- **Thread Organization**: Use replies to keep related messages together
- **Context**: Reference parent message content in reply
- **Notification**: @mention original sender for notification
- **Timing**: Reply promptly for better user experience
</best_practices>

<example>
**Use Case**: Auto-replying to questions in support channel with relevant information
</example>

</action>

---

### Reply with an Adaptive Card in a Channel

<action id="action-005" category="create" complexity="medium" throttle_impact="medium">

<action_header>
**Operation Type**: Create
**Complexity**: Medium
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: ReplyWithAdaptiveCardInChannel
</action_header>

<description>
Replies to channel message with adaptive card instead of plain text. Enables rich, interactive threaded responses.
</description>

<parameters>
Same as reply with message, but includes adaptive card JSON instead of plain text
</parameters>

<best_practices>
- **Rich Responses**: Use for detailed, formatted responses
- **Interactive Replies**: Include buttons/actions in replies
- **Status Updates**: Reply with status cards to original requests
</best_practices>

</action>

---

## Team/Channel/Chat Management

### Create a Channel

<action id="action-011" category="create" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Create
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: CreateChannel
</action_header>

<description>
Creates a new channel within specified team. Enables dynamic channel creation for projects, topics, or organizational needs.
</description>

<parameters>
#### Required Parameters

**Team** (`string`)
- **Description**: Team to create channel in
- **Format**: Dynamic dropdown of available teams

**Name** (`string`)
- **Description**: Channel name as displayed in Teams
- **Example**: "Project Alpha", "Sales Q4"

#### Optional Parameters

**Description** (`string`)
- **Description**: Textual description of channel purpose
- **Example**: "Channel for Project Alpha planning and updates"
</parameters>

<returns>
**Return Type**: Channel object

**Structure**:
```json
{
  "id": "channel-guid",
  "displayName": "Project Alpha",
  "description": "Channel for Project Alpha planning"
}
```

**Key Fields**:
- **id**: Unique channel identifier for subsequent operations
- **displayName**: Channel name
- **description**: Channel description
</returns>

<best_practices>
- **Naming Convention**: Use consistent naming scheme
- **Descriptions**: Provide clear descriptions for discoverability
- **Permissions**: Set appropriate permissions after creation
- **Notification**: Notify team of new channel creation
- **Templates**: Use standard templates for common channel types
</best_practices>

<example>
**Use Case**: Automatically creating project channels when project created in project management system

```json
{
  "Team": "Engineering Team",
  "Name": "Project - Customer Portal v2",
  "Description": "Planning, development, and deployment of Customer Portal version 2.0"
}
```
</example>

</action>

---

### Create a Chat

<action id="action-012" category="create" complexity="medium" throttle_impact="medium">

<action_header>
**Operation Type**: Create
**Complexity**: Medium
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: CreateChat
</action_header>

<description>
Creates one-on-one or group chat with specified members. Enables programmatic chat creation for collaboration, notifications, or support scenarios.
</description>

<parameters>
#### Optional Parameters

**Title** (`string`)
- **Description**: Title for group chats
- **Note**: Only applicable for group chats (3+ members)
- **Example**: "Project Alpha Team Chat"

#### Required Parameters

**Members to Add** (`string`)
- **Description**: User IDs to include in chat
- **Format**: Semicolon-separated user IDs (GUIDs)
- **Example**: "guid1;guid2;guid3"
- **Minimum**: 2 members (including creator)
- **Maximum**: 20 members
</parameters>

<returns>
**Return Type**: Chat object with ID and details
</returns>

<limitations>
<limitation id="lim-action-016" severity="high">
**Maximum 20 Users**: Cannot create chats with more than 20 users
- For larger groups, use channels instead
</limitation>

<limitation id="lim-action-017" severity="high">
**No Guest Users**: Cannot add guest users to chats
- Internal organization users only
</limitation>

<limitation id="lim-action-018" severity="medium">
**User IDs Required**: Must use Microsoft Entra ID (Azure AD) user IDs (GUIDs)
- Cannot use email addresses
- Use Office 365 Users connector to get user IDs from emails
</limitation>
</limitations>

<best_practices>
- **User ID Lookup**: Use "Office 365 Users - Get user profile (V2)" to get user IDs from emails
- **Title for Groups**: Always provide title for group chats (3+ members)
- **Membership Validation**: Verify all users exist before creating chat
- **Error Handling**: Handle cases where users can't be added
</best_practices>

<example>
**Use Case**: Creating support chat when high-priority ticket created

**Flow**:
1. Trigger: When ticket created with priority = High
2. Get user profile for ticket submitter (get user ID)
3. Get user profile for assigned support agent (get user ID)
4. Create chat with both user IDs
5. Post message in chat with ticket details
</example>

</action>

---

### Get a Team

<action id="action-013" category="read" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Read
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: GetTeam
</action_header>

<description>
Gets details for a team including settings, description, and configuration. Retrieves team metadata for validation or display.
</description>

<parameters>
#### Required Parameters

**Team** (`string`)
- **Description**: Team to retrieve details for
</parameters>

<returns>
Complete team object with all settings and metadata
</returns>

</action>

---

### List All Channels / List Channels

<action id="action-014-015" category="read" complexity="low" throttle_impact="low">

**List All Channels**: Lists all channels in team including shared channels (hosted elsewhere)

**List Channels**: Lists channels owned by the team only

<parameters>
**Required**: Team
**Optional**: Filter Query, Order By (OData syntax)
</parameters>

<best_practices>
- **Dynamic Dropdowns**: Use to populate channel selection lists
- **Shared Channels**: Use "List All Channels" to include shared channels
- **Filtering**: Apply OData filters for specific channel types
</best_practices>

</action>

---

### List Chats

<action id="action-016" category="read" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Read
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: ListChats
</action_header>

<description>
Lists recent chats user is part of with filtering options.
</description>

<parameters>
#### Required Parameters

**Chat Types** (`string`)
- **Description**: Filter by chat type
- **Values**: Filter options for chat types

**Topic** (`string`)
- **Description**: Filter by topic name
</parameters>

<returns>
Array of chat objects with ID, topic, created date, last updated date
</returns>

<best_practices>
- **Recent Activity**: Sort by last updated for most recent chats
- **Type Filtering**: Filter by 1:1 vs group chats
- **Pagination**: Implement if many chats expected
</best_practices>

</action>

---

## Member Management

### Add a Member to a Team

<action id="action-021" category="create" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Create
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: AddMemberToTeam
</action_header>

<description>
Adds a member to a team with optional owner designation. Enables automated team membership management.
</description>

<parameters>
#### Required Parameters

**Team** (`string`)
- **Description**: Team to add member to

**User** (`string`)
- **Description**: User principal name or Microsoft Entra ID
- **Format**: email@domain.com or GUID
- **Example**: "john.doe@contoso.com"

**Set User as Team Owner** (`boolean`)
- **Description**: Whether to make user a team owner
- **Default**: false (member role)
- **Note**: Can set guest users as owners
</parameters>

<best_practices>
- **Bulk Operations**: Add delay between adds for bulk membership
- **Validation**: Verify user exists before adding
- **Owner Role**: Use carefully; owners have full team control
- **Notification**: Send welcome message after adding member
- **Guest Users**: Can add guest users and set as owners
</best_practices>

<example>
**Use Case**: Adding new employees to department teams during onboarding

**Flow**:
1. Trigger: When employee record created in HR system
2. Get employee email
3. Add member to appropriate department teams
4. Post welcome message in team general channel
</example>

</action>

---

### List Members

<action id="action-022" category="read" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Read
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: ListMembers
</action_header>

<description>
Lists direct members of group chat or channel. Returns member details including roles and visible history start date.
</description>

<parameters>
#### Required Parameters

**Thread Type** (`string`)
- **Description**: Type of thread to list members from
- **Values**: Channel, Chat, Group chat

**List Members Request** (`dynamic`)
- **Description**: Configuration for member listing
- **Format**: Team/Channel/Chat identifiers
</parameters>

<returns>
**Return Type**: Array of member objects

**Structure**:
```json
{
  "members": [
    {
      "displayName": "John Doe",
      "email": "john@contoso.com",
      "id": "member-id",
      "roles": ["owner"],
      "tenantId": "tenant-guid",
      "userId": "user-guid",
      "visibleHistoryStartDateTime": "2025-01-01T00:00:00Z"
    }
  ]
}
```

**Key Fields**:
- **displayName**: Member display name
- **email**: Member email address
- **roles**: Array of roles ("owner" or empty for member)
- **userId**: Microsoft Entra ID user identifier
</returns>

<best_practices>
- **Role Filtering**: Filter by roles array to find owners
- **Presence Check**: Check membership before operations
- **Audit**: Use for membership auditing and reporting
- **Bulk Operations**: Loop through members for bulk messaging/actions
</best_practices>

</action>

---

## Tags Management

### Create a Tag for a Team

<action id="action-031" category="create" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Create
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: CreateTeamTag
</action_header>

<description>
Creates a tag in a team for organizing and @mentioning groups of users. Tags enable efficient group communication without creating channels or chats.
</description>

<parameters>
#### Required Parameters

**Team** (`string`)
- **Description**: Team to create tag in

**Display Name** (`string`)
- **Description**: Tag name as displayed
- **Example**: "Project Leads", "Backend Developers"

**Members' IDs** (`string`)
- **Description**: User IDs to assign to tag
- **Format**: Semicolon-separated UUIDs
- **Example**: "guid1;guid2;guid3"
- **Note**: Must be UUID format
</parameters>

<returns>
Tag object with ID, team ID, display name, member count
</returns>

<best_practices>
- **Descriptive Names**: Use clear, descriptive tag names
- **Role-Based**: Create tags for functional roles or project teams
- **UUID Format**: Ensure user IDs are in UUID format
- **@Mention Usage**: Use "Get @mention token for tag" to mention tag in messages
</best_practices>

<example>
**Use Case**: Creating "On-Call" tag for rotation of on-call engineers

**Flow**:
1. Scheduled trigger (weekly)
2. Get current on-call engineers from rotation system
3. Delete old "On-Call" tag
4. Create new "On-Call" tag with current engineers
5. Post announcement in team channel with @mention of new tag
</example>

</action>

---

### List All Tags for a Team / Add/Delete Tag Members

Similar tag management actions:
- **List All Tags**: Retrieves all tags in team
- **Add Member to Tag**: Adds user to existing tag
- **Delete Member from Tag**: Removes user from tag
- **Delete Tag**: Removes tag from team

---

## Utility Operations

### Get an @Mention Token for a User

<action id="action-041" category="utility" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Utility
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: GetMentionTokenForUser
</action_header>

<description>
Creates an @mention token that can be inserted into messages or adaptive cards to @mention a user. Generates proper mention syntax for Teams messaging.
</description>

<parameters>
#### Required Parameters

**User** (`string`)
- **Description**: User principal name or user ID
- **Format**: email@domain.com or GUID
- **Example**: "john.doe@contoso.com"
</parameters>

<returns>
**Return Type**: String (mention token)

**Format**: `<at>John Doe</at>`

**Usage**: Insert token directly into message content
</returns>

<best_practices>
- **Notification**: Use for important notifications requiring user attention
- **Context**: Include context around @mention for clarity
- **Multiple Mentions**: Generate token for each user to mention
- **Limit**: Remember 20 user mentions per message limit
</best_practices>

<example>
```
Message:
"<p>New high-priority task assigned.</p>
<p>@[mention-token] - Please review task #12345.</p>"

Where [mention-token] is output from this action
```

**Use Case**: Assigning tasks with @mention notification
</example>

</action>

---

### Get an @Mention Token for a Team Tag

Similar to user mention but creates token for team tags. Use to @mention entire groups.

---

### Post a Feed Notification

<action id="action-043" category="utility" complexity="medium" throttle_impact="medium">

<action_header>
**Operation Type**: Utility
**Complexity**: Medium
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: PostFeedNotification
</action_header>

<description>
Posts notification to user's activity feed linking to chat or team. Creates feed item visible in Teams activity section.
</description>

<parameters>
#### Required Parameters

**Post as** (`string`)
- **Values**: "Flow bot", "User"

**Notification Type** (`string`)
- **Description**: Type of notification to create

**Post Feed Notification Request** (`dynamic`)
- **Description**: Configuration with recipient and content details
</parameters>

<best_practices>
- **Important Updates**: Use for high-priority notifications
- **Deep Linking**: Link notification to relevant chat/channel
- **Frequency**: Don't overuse; can become noise
- **Context**: Provide clear context in notification text
</best_practices>

</action>

---

### Send a Microsoft Graph HTTP Request

<action id="action-044" category="utility" complexity="high" throttle_impact="variable">

<action_header>
**Operation Type**: Utility
**Complexity**: High
**Throttling Impact**: Variable
**Premium**: No
**Operation ID**: SendGraphHTTPRequest
</action_header>

<description>
Constructs custom Microsoft Graph REST API request to Teams endpoints. Enables advanced operations not available through standard actions. Supported segments: /teams, /me, /users, channels, chats, installedApps, messages, pinnedMessages.
</description>

<parameters>
#### Required Parameters

**URI** (`string`)
- **Description**: Full or relative URI for Graph API
- **Format**: Relative (/teams/{id}) or full (https://graph.microsoft.com/v1.0/teams/{id})
- **Example**: "/teams/{team-id}/channels"

**Method** (`string`)
- **Description**: HTTP method
- **Values**: GET, POST, PUT, PATCH, DELETE
- **Default**: GET

#### Optional Parameters

**Body** (`string`)
- **Description**: Request body content
- **Format**: JSON string
- **Usage**: Required for POST, PUT, PATCH

**Content-Type** (`string`)
- **Description**: Content-type header
- **Default**: application/json

**CustomHeader1-5** (`string`)
- **Description**: Custom headers
- **Format**: "header-name: header-value"
- **Example**: "Prefer: return=representation"
</parameters>

<returns>
**Return Type**: Dynamic object based on API response
</returns>

<best_practices>
- **Documentation**: Reference Microsoft Graph API documentation
- **Testing**: Test API calls in Graph Explorer first
- **Error Handling**: Implement robust error handling
- **Permissions**: Ensure connection has required permissions
- **Rate Limits**: Monitor Graph API rate limits
</best_practices>

<example>
**Use Case**: Get detailed channel statistics not available through standard actions

```json
{
  "URI": "/teams/{team-id}/channels/{channel-id}/messages/delta",
  "Method": "GET"
}
```
</example>

</action>

---

## Deprecated Actions Summary

The following actions are deprecated and replaced by newer versions. Existing flows will continue to work but new flows should use current actions:

### Deprecated Messaging Actions
- Post a message (replaced by Post message in chat or channel)
- Post a message (V2) (replaced by V3 / current action)
- Post a message (V3) (replaced by current action)
- Post a reply to a message (replaced by Reply with message in channel)
- Post a reply to a message (V2)
- Post message as Flow bot to user (replaced by current action)
- Post message as Flow bot to channel (replaced by current action)
- Post adaptive card as Flow bot (replaced by Post card in chat or channel)
- Post adaptive card and wait (V1) (replaced by current action)
- Post choice of options as Flow bot (replaced by adaptive card approach)

### Deprecated Shifts Actions (14 actions)
All Shifts-related actions deprecated. Use Shifts connector instead:
- Approve/Decline Swap Shifts requests
- Approve/Decline Time Off requests
- Approve/Decline Offer/Open Shift requests
- Create/Delete/Update shifts and open shifts
- Get shift/schedule/scheduling group details
- List various shift-related items

**Recommendation**: Use dedicated Shifts connector for all shift management operations.

---

## Common Error Codes

<error id="err-403" http_code="403">
**Error**: 403 Forbidden
**Causes**:
- Insufficient permissions for operation
- Workflows app not installed
- Private channel access attempt
- Guest user limitations

**Solutions**:
- Verify user permissions
- Install Workflows app
- Use standard channels
- Check guest user constraints
</error>

<error id="err-404" http_code="404">
**Error**: 404 Not Found
**Causes**:
- Team/channel/chat doesn't exist
- Message ID invalid or deleted
- User removed from team

**Solutions**:
- Verify resource IDs are current
- Check user still has access
- Handle deletion scenarios
</error>

<error id="err-429" http_code="429">
**Error**: 429 Too Many Requests
**Causes**:
- Exceeded 100 API calls per 60 seconds
- Exceeded 25 non-GET calls per 300 seconds (specific operations)

**Solutions**:
- Add delays between operations (3+ seconds)
- Implement exponential backoff
- Reduce operation frequency
- Use multiple connections for high volume
</error>

---

## General Limitations

<limitation id="lim-general-001" severity="critical">
**API Rate Limits**:
- 100 calls per 60 seconds per connection (general)
- 25 non-GET calls per 300 seconds (List chats, Feed notifications)
- 300 non-GET calls per 300 seconds (other operations)

**Recommendation**: Add 3+ second delays; monitor usage
</limitation>

<limitation id="lim-general-002" severity="high">
**Message Size**: ~28 KB maximum per message/card
- Includes all formatting and content
- Recommendation: Keep messages concise
</limitation>

<limitation id="lim-general-003" severity="high">
**Workflows App Required**: Most messaging actions require Workflows app
- Usually auto-installed
- Manual installation if missing
</limitation>

<limitation id="lim-general-004" severity="high">
**Private Channels Not Supported**: Cannot post to private channels
- Standard and shared channels only
- No current workaround
</limitation>

<limitation id="lim-general-005" severity="medium">
**Polling Latency**: Trigger polling intervals 3-10 minutes
- Not real-time for polling triggers
- Use webhook triggers when available
</limitation>

<limitation id="lim-general-006" severity="medium">
**Subscription Required**: Microsoft 365 Teams subscription required
- All users need Teams license
</limitation>

---

## Performance Best Practices

### Messaging Optimization
1. **Size Management**: Keep messages under 20 KB
2. **Batching**: Avoid rapid-fire messages; add delays
3. **Formatting**: Use HTML formatting judiciously
4. **@Mentions**: Generate tokens efficiently; cache when possible

### API Management
1. **Rate Limiting**: Add 3+ second delays between operations
2. **Monitoring**: Track API usage patterns
3. **Concurrency**: Limit concurrent operations to 10-20
4. **Error Handling**: Implement retry logic with backoff

### Member Operations
1. **Bulk Adds**: Delay between member additions
2. **Caching**: Cache team/channel lists for reuse
3. **Validation**: Verify users exist before operations

---

**Last Updated**: 2025-10-31
**Documentation Version**: 1.0
**Connector Version**: Current (as of 2025-10-31)
**Official Reference**: https://learn.microsoft.com/en-us/connectors/teams/
