# Approvals Connector Overview

---
type: connector-overview
connector_name: Approvals
connector_type: standard
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [approval, workflow, request, approve, reject, decision, voting]
related_connectors: [Office 365 Outlook, Microsoft Teams, SharePoint]
api_limits:
  creation_calls_per_minute: 50
  non_creation_calls_per_minute: 500
official_docs_url: https://learn.microsoft.com/en-us/connectors/approvals/
---

<official_docs>
https://learn.microsoft.com/en-us/connectors/approvals/
</official_docs>

<description>
Approvals connector enables creation and management of approval workflows within Power Automate, supporting various approval types (Approve/Reject, Custom responses, Everyone must approve) with actionable emails, Teams integration, and comprehensive tracking. Flows can pause execution awaiting approval decisions with automatic notifications to approvers.
</description>

<capabilities>
## Core Capabilities
- Start and wait for approval (blocking flow execution)
- Create approval without waiting (non-blocking)
- Multiple approval types (Basic, Custom, Everyone must approve)
- Actionable email notifications to approvers
- Teams approval integration
- Attachment support in approval requests
- Custom response options
- Approval reassignment and delegation

## Supported Operations
- **Approval Creation**: Start and wait, Create approval, Start and wait for text approval
- **Approval Management**: Wait for approval, Cancel approval, Reassign approval
- **Response Handling**: Respond to approval, Get approval responses
- **Integration**: Send actionable emails, Teams approval cards

## Integration Features
- Actionable Outlook emails (approve/reject directly from email)
- Microsoft Teams approval cards
- Attachment support (multiple files)
- Custom response options beyond Approve/Reject
- Flow creator identity in approval details (anti-spoofing)
</capabilities>

<api_limits>
## Rate Limits

**Per Flow Limits**
- **Creation requests**: 50 calls per 60 seconds
- **Non-creation requests**: 500 calls per 60 seconds
- Throttling scope: per flow

**Throttling Behavior**
- HTTP Status: 429 (Too Many Requests)
- Automatic retry: yes

## Size Limits
- **Attachments**: Multiple files supported, no duplicate names allowed
- **Recipient List**: Limited by data size (large lists may fail with "Everyone must approve")
- **Response Text**: No explicit documented limit

## Timeout Limits
- Approval timeout: Configurable, no maximum documented
- Default: No automatic timeout
</api_limits>

<critical_limitations>
## Approval Behavior

<limitation id="lim-001" severity="medium">
**UTC Timestamps Only**: All timestamps display in UTC timezone

- **Impact**: User must convert times to local timezone
- **Scope**: All approval timestamps
- **Workaround**: Use formatDateTime() with timezone conversion
- **Affected Operations**: All approval actions
</limitation>

<limitation id="lim-002" severity="low">
**Flow Creator Always Shown**: Creator identity always visible in approval details

- **Impact**: Cannot hide who created approval (anti-spoofing measure)
- **Scope**: All approval requests
- **Workaround**: None - security feature by design
- **Affected Operations**: All approval creations
</limitation>

<limitation id="lim-003" severity="medium">
**Case-Sensitive Responses**: Basic responses must be exact: "Approve" and "Reject"

- **Impact**: "approve" or "APPROVE" won't work programmatically
- **Scope**: Await Basic approval responses
- **Workaround**: Use exact case in response comparisons
- **Affected Operations**: Respond to approval
</limitation>

## Email and Notifications

<limitation id="lim-004" severity="high">
**No Actionable Emails for Guests**: Guest users don't receive actionable Outlook emails

- **Impact**: Guests must use approval center web page
- **Scope**: Guest user approvers
- **Workaround**: Provide direct link to approval center
- **Affected Operations**: All approval notifications to guests
</limitation>

<limitation id="lim-005" severity="medium">
**Unique Attachment Names Required**: Multiple attachments cannot share same filename

- **Impact**: Upload fails if duplicate names exist
- **Scope**: Approval attachments
- **Workaround**: Rename files before attaching
- **Affected Operations**: Create approval with attachments
</limitation>

<limitation id="lim-006" severity="high">
**Everyone Must Approve Size Limit**: Large recipient lists may fail due to data size constraints

- **Impact**: Approval creation fails with many approvers
- **Scope**: "Everyone must approve" type
- **Workaround**: Split into multiple approval requests or use "First to respond" type
- **Affected Operations**: Create "Everyone must approve" approval
</limitation>
</critical_limitations>

<authentication>
## Supported Authentication Methods

### OAuth (Only Method)
- Flow type: Authorization Code
- Required permissions: Approval.Read.All, Approval.ReadWrite.All
- Token refresh: Automatic
- Account type: Organizational accounts only

## Required Permissions
- **Approval.ReadWrite.All**: Create and manage approvals
- **Mail.Send**: Send approval notification emails
</authentication>

<common_use_cases>
## 1. Purchase Request Approval
Approve purchase requests with amount-based routing

## 2. Document Review Workflow
Multi-stage document approval with reassignment

## 3. Time-Off Request Processing
Manager approval for vacation requests

## 4. Expense Report Approval
Finance team approval with receipt attachments

## 5. IT Access Request Approval
Security team approval for system access
</common_use_cases>

<best_practices>
## Performance Optimization
1. **Use "First to Respond"**: For faster decisions when any approver can decide
2. **Limit Recipient Lists**: Keep "Everyone must approve" lists under 20 approvers
3. **Cache Approval Details**: Store approval metadata to avoid repeated queries

## Reliability & Error Handling
1. **Handle Timeouts**: Set reasonable approval timeouts with fallback actions
2. **Implement Escalation**: Auto-escalate unanswered approvals after threshold
3. **Log All Approvals**: Record approval history for audit trail

## Security Best Practices
1. **Validate Approvers**: Verify approver list before sending
2. **Include Context**: Provide sufficient details for informed decisions
3. **Use Attachments Securely**: Validate file types and sizes
</best_practices>

<troubleshooting>
## Common Errors

### Throttling (429)
<error id="err-429" http_code="429">
- **Cause**: Exceeded 50 creations per minute
- **Fix**: Add delays between approval creations
</error>

### Guest User Email Issues
<error id="err-guest" http_code="N/A">
- **Cause**: Actionable emails not supported for guests
- **Fix**: Provide approval center link, educate guest users
</error>

### Duplicate Attachment Names
<error id="err-attachment" http_code="400">
- **Cause**: Multiple files with same name
- **Fix**: Rename files before attachment
</error>
</troubleshooting>

<related_docs>
- **Actions**: [actions.md](./actions.md) - To be created
- **Triggers**: [triggers.md](./triggers.md) - To be created
- **Official Docs**: https://learn.microsoft.com/en-us/connectors/approvals/
</related_docs>

<metadata_summary>
- **Last Updated**: 2025-10-31
- **Fetch Date**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 40%
- **Validation Status**: Validated
- **Next Review**: 2025-11-30
</metadata_summary>
