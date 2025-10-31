# Microsoft Planner Connector Overview

---
type: connector-overview
connector_name: Microsoft Planner
connector_type: standard
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [planner, tasks, project management, bucket, assignment, checklist, plan]
related_connectors: [Microsoft Teams, Office 365 Groups, Office 365 Outlook]
api_limits:
  calls_per_minute: 1.67
  calls_per_hour: 100
  trigger_poll_frequency_seconds: 60
official_docs_url: https://learn.microsoft.com/en-us/connectors/planner/
---

<official_docs>
https://learn.microsoft.com/en-us/connectors/planner/
</official_docs>

<description>
Microsoft Planner connector enables automation of task management workflows including task creation, updates, assignments, and organization via buckets. Supports 25 color categories, checklist management, and integration with Teams for collaborative task tracking within Microsoft 365 groups.
</description>

<capabilities>
## Core Capabilities
- Task CRUD operations (Create, Read, Update, Delete)
- Task assignments with user IDs or emails
- Bucket management for task organization
- 25 color category labels
- Checklist and reference link management
- Completion percentage tracking
- Date and priority management

## Supported Operations
- **Task Management**: Create task, Update task, Get task details, List tasks
- **Assignments**: Add/Remove assignees using user IDs or emails
- **Organization**: Create bucket, List buckets, Move tasks between buckets
- **Details**: Manage descriptions, checklists, and references

## Integration Features
- Triggers for new tasks and assignments
- Color categorization (25 categories)
- Bucket-based organization
- Checklist support for subtasks
- Reference links for related resources
- Progress tracking with completion percentage
</capabilities>

<api_limits>
## Rate Limits
- **100 API calls per 60 seconds** per connection
- **Trigger polling**: 1 poll per 60 seconds
- Throttling scope: per connection
- Retry-After header: yes

## Size Limits
- **Task Title**: No explicit documented limit
- **Description**: No explicit documented limit
- **Checklist Items**: No explicit documented limit
- **Assignees**: No explicit limit per task
</api_limits>

<critical_limitations>
## Plan Support

<limitation id="lim-001" severity="critical">
**Basic Plans Only**: Connector currently supports basic Planner plans only

- **Impact**: Advanced plan features unavailable
- **Scope**: All operations
- **Workaround**: None - use basic plans for automation
- **Affected Operations**: All actions and triggers
</limitation>

## UI Behavior

<limitation id="lim-002" severity="low">
**Group ID Dropdown Behavior**: Group ID parameter only populates dependent dropdowns

- **Impact**: Dropdown may show warnings but any valid value works after selection
- **Scope**: UI configuration in Power Automate designer
- **Workaround**: Ignore warnings if valid Group ID is used
- **Affected Operations**: All actions requiring Group ID
</limitation>

## Connection Sharing

<limitation id="lim-003" severity="medium">
**Non-Shareable Connections**: Connections cannot be shared between users

- **Impact**: Each user must create own connection when apps shared
- **Scope**: All connection types
- **Workaround**: Document connection setup for all users
- **Affected Operations**: All operations
</limitation>
</critical_limitations>

<authentication>
## Supported Authentication Methods
### OAuth (Only Method)
- Flow type: Authorization Code
- Required permissions: Group.ReadWrite.All, Tasks.ReadWrite
- Token refresh: Automatic
- Account type: Organizational accounts only

## Required Permissions
- **Group.ReadWrite.All**: Access to Microsoft 365 Groups and plans
- **Tasks.ReadWrite**: Create and manage Planner tasks
</authentication>

<common_use_cases>
## 1. Automated Task Creation from Forms
Create Planner tasks from form submissions

## 2. Project Setup Automation
Auto-create standard task set for new projects

## 3. Task Assignment Based on Rules
Assign tasks based on department, skills, or availability

## 4. Status Reporting
Generate task completion reports for project managers

## 5. Integration with Approvals
Create follow-up tasks based on approval decisions
</common_use_cases>

<best_practices>
## Performance Optimization
1. **Batch Task Creation**: Create multiple tasks with delays to avoid throttling
2. **Cache Plan/Bucket IDs**: Store IDs in variables to avoid repeated lookups
3. **Use Task References**: Link to external resources instead of duplicating data

## Reliability
1. **Handle Missing Plans**: Verify plan exists before task operations
2. **Validate Assignees**: Check user IDs/emails are valid before assigning
3. **Set Due Dates Carefully**: Validate date formats (ISO 8601)

## Security
1. **Control Task Visibility**: Planner tasks visible to all group members
2. **Sensitive Data**: Avoid including sensitive info in task titles/descriptions
3. **Assignment Notifications**: Be aware users receive notifications for assignments
</best_practices>

<troubleshooting>
### Throttling (429)
<error id="err-429" http_code="429">
- **Cause**: Exceeded 100 calls per 60 seconds
- **Fix**: Add delays between task operations, batch creates
</error>

### Plan Not Found (404)
<error id="err-404" http_code="404">
- **Cause**: Plan ID invalid or plan deleted
- **Fix**: Verify plan exists in Planner, check Group ID is correct
</error>

### Permission Denied (403)
<error id="err-403" http_code="403">
- **Cause**: User not member of group containing plan
- **Fix**: Add user to Microsoft 365 Group
</error>

### Invalid Assignee
<error id="err-assignee" http_code="400">
- **Cause**: User ID or email invalid or not in group
- **Fix**: Verify user exists and is group member
</error>
</troubleshooting>

<related_docs>
- **Official Docs**: https://learn.microsoft.com/en-us/connectors/planner/
- **Microsoft Teams**: [Link](../Teams/overview.md) - Teams integration
</related_docs>

<metadata_summary>
- **Last Updated**: 2025-10-31
- **Fetch Date**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 40%
</metadata_summary>
