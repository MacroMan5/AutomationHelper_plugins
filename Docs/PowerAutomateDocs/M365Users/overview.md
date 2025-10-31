# Office 365 Users Connector Overview

---
type: connector-overview
connector_name: Office 365 Users
connector_type: standard
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [users, profile, manager, directory, azure ad, entra id, lookup, search]
related_connectors: [Office 365 Outlook, Microsoft Teams, SharePoint]
api_limits:
  calls_per_minute: 16.67
  calls_per_hour: 1000
official_docs_url: https://learn.microsoft.com/en-us/connectors/office365users/
---

<official_docs>
https://learn.microsoft.com/en-us/connectors/office365users/
</official_docs>

<description>
Office 365 Users connector provides access to Microsoft Entra ID (formerly Azure AD) user profiles, enabling lookups of user information, manager relationships, direct reports, and profile photos. Essential for building user-centric workflows, org chart navigation, and dynamic permission assignment.
</description>

<capabilities>
## Core Capabilities
- User profile retrieval with customizable field selection
- Manager and direct report lookups
- User search across display names, emails, and UPNs
- Profile photo retrieval
- Current user profile access
- Profile updates for current user

## Supported Operations
- **Profile Access**: Get user profile (V2), Get my profile (V2), Update my profile
- **Org Structure**: Get manager (V2), Get direct reports (V2)
- **Search**: Search for users (V2)
- **Photos**: Get user photo (V2)

## Integration Features
- Customizable field selection to reduce data transfer
- Search across multiple user properties
- Support for manager hierarchy navigation
- Profile photo in multiple sizes
</capabilities>

<api_limits>
## Rate Limits
- **1,000 API calls per 60 seconds** per connection
- Throttling scope: per connection
- Retry-After header: yes

## Size Limits
- **Profile Photo**: Multiple sizes available (48x48, 64x64, 96x96, 120x120, 240x240, 360x360, 432x432, 504x504, 648x648)
</api_limits>

<critical_limitations>
## Access Requirements

<limitation id="lim-001" severity="high">
**REST API Required**: Connector requires Office 365 mailbox with REST API enabled

- **Impact**: Cannot use with mailboxes lacking REST API
- **Scope**: All operations
- **Workaround**: Enable REST API on mailbox or use different account
- **Affected Operations**: All actions
</limitation>

<limitation id="lim-002" severity="high">
**GCCH Unsupported in LogicApps**: Government Community Cloud High accounts not supported in LogicApps US Government Cloud

- **Impact**: Cannot use connector in LogicApps GCCH
- **Scope**: LogicApps in US Government Cloud
- **Workaround**: Use Power Automate or different cloud
- **Affected Operations**: All actions in LogicApps GCCH
</limitation>

## Data Retrieval

<limitation id="lim-003" severity="medium">
**Manager Returns Empty**: Get manager returns no data if user lacks configured manager in Entra ID

- **Impact**: Flow logic must handle empty/null manager scenarios
- **Scope**: Get manager (V2) action
- **Workaround**: Check if manager exists before using, handle null values
- **Affected Operations**: Get manager (V2)
</limitation>

<limitation id="lim-004" severity="medium">
**Guest User 401 Errors**: Guest users may encounter unauthorized errors with certain actions

- **Impact**: Cross-tenant scenarios may fail
- **Scope**: Guest user connections
- **Workaround**: Use internal accounts or configure B2B access properly
- **Affected Operations**: Various actions for guest users
</limitation>

<limitation id="lim-005" severity="medium">
**Field Selection Required**: Default field selection may trigger 403 errors

- **Impact**: Queries fail with default selections
- **Scope**: Profile retrieval actions
- **Workaround**: Explicitly specify required fields using $select parameter
- **Affected Operations**: Get user profile, Search for users
</limitation>

<limitation id="lim-006" severity="low">
**Conditional Access Blocks**: Conditional Access policies can block connector operations

- **Impact**: Operations fail if CA policy applies
- **Scope**: All operations when CA enabled
- **Workaround**: Configure CA exceptions for service accounts
- **Affected Operations**: All actions
</limitation>
</critical_limitations>

<authentication>
## Supported Authentication Methods
### OAuth (Only Method)
- Flow type: Authorization Code
- Required permissions: User.Read.All, User.ReadBasic.All
- Token refresh: Automatic
- Account type: Organizational accounts only

## Required Permissions
- **User.Read.All**: Read all user profiles
- **User.ReadBasic.All**: Read basic profiles of all users
- **User.ReadWrite**: Update current user's profile
</authentication>

<common_use_cases>
## 1. Manager Approval Routing
Get user's manager and send approval request

## 2. User Profile Enrichment
Retrieve user details for SharePoint item creation

## 3. Org Chart Navigation
Build org structure for reporting or visualization

## 4. Dynamic Permission Assignment
Assign permissions based on department or manager

## 5. User Search and Lookup
Find users by name or email for workflow assignment
</common_use_cases>

<best_practices>
## Performance Optimization
1. **Specify Fields**: Always use $select to retrieve only needed fields
2. **Cache User Data**: Store frequently accessed profiles in variables
3. **Batch User Lookups**: Retrieve multiple users in single operation when possible

## Reliability
1. **Handle Null Managers**: Always check if manager exists before using
2. **Validate User Exists**: Verify user profile returned before accessing properties
3. **Retry on 401/403**: Implement retry for transient permission errors

## Security
1. **Use Service Account**: Dedicated account for user lookups
2. **Limit Profile Access**: Only request necessary profile fields
3. **Handle Sensitive Data**: Treat user emails and names as PII
</best_practices>

<troubleshooting>
### Throttling (429)
<error id="err-429" http_code="429">
- **Cause**: Exceeded 1,000 calls per 60 seconds
- **Fix**: Add delays, cache user data, batch lookups
</error>

### Unauthorized (401)
<error id="err-401" http_code="401">
- **Cause**: Insufficient permissions or guest user issue
- **Fix**: Grant User.Read.All, verify account type
</error>

### Forbidden (403)
<error id="err-403" http_code="403">
- **Cause**: Default field selection or Conditional Access
- **Fix**: Explicitly specify fields with $select, configure CA exceptions
</error>

### User Not Found (404)
<error id="err-404" http_code="404">
- **Cause**: User doesn't exist or was deleted
- **Fix**: Validate user exists before lookup, handle 404 gracefully
</error>
</troubleshooting>

<related_docs>
- **Official Docs**: https://learn.microsoft.com/en-us/connectors/office365users/
</related_docs>

<metadata_summary>
- **Last Updated**: 2025-10-31
- **Fetch Date**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 40%
</metadata_summary>
