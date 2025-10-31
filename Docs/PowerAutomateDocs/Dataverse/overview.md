# Microsoft Dataverse Connector Overview

---
type: connector-overview
connector_name: Microsoft Dataverse
connector_type: standard
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [dataverse, cds, common data service, database, table, row, record, power platform]
related_connectors: [Power Apps, SharePoint, Office 365 Outlook]
api_limits:
  calls_per_minute: 20
  calls_per_5minutes: 6000
  max_batch_operations: 1000
official_docs_url: https://learn.microsoft.com/en-us/connectors/commondataserviceforapps/
---

<official_docs>
https://learn.microsoft.com/en-us/connectors/commondataserviceforapps/
</official_docs>

<description>
Microsoft Dataverse connector provides comprehensive database operations for Power Platform, enabling CRUD operations on tables, relationship management, file handling, and advanced querying with Relevance Search. Supports transactional batch operations, business process flows, and webhook-based triggers for real-time data change notifications.
</description>

<capabilities>
## Core Capabilities
- CRUD operations on Dataverse tables (Create, Read, Update, Delete, Upsert)
- Advanced querying with OData filtering and sorting
- Relationship management (relate/unrelate rows)
- File and image upload/download
- Batch operations with changeset support (transactional)
- Relevance Search integration
- Business Process Flow integration
- Custom and standard action execution

## Supported Operations
- **Data Management**: Add/Update/Delete/Get row, List rows, Upsert row
- **Relationships**: Relate rows, Unrelate rows
- **Files**: Upload file/image, Download file/image
- **Search**: Search rows (Relevance Search), List rows (OData query)
- **Advanced**: Perform bound/unbound actions, Execute changeset, Run business process flow steps

## Integration Features
- Webhook-based triggers for real-time data changes
- Scope and filtering options for triggers (organization, business unit, user)
- Service Principal and Certificate authentication for unattended automation
- Multi-environment support with "WithOrganization" action variants
- Transactional batch operations via changesets
</capabilities>

<api_limits>
## Rate Limits

**Connection-Level Throttling**
- **6,000 API calls per 300 seconds** (5 minutes) per connection
- **20 calls per minute** average
- Throttling scope: per connection
- Retry-After header: yes

**Throttling Behavior**
- HTTP Status: 429 (Too Many Requests)
- Error message: "Rate limit exceeded"
- Automatic retry: yes (with exponential backoff)

## Size Limits

**Data Operations**
- Max batch operations: **1,000 operations** per changeset
- Max file upload size: Varies by table configuration
- Max OData query complexity: No explicit documented limit

## Timeout Limits
- Default timeout: **120 seconds**
- Long-running operations: Supported via async patterns
</api_limits>

<critical_limitations>
## Authentication

<limitation id="lim-001" severity="high">
**Default Authentication Deprecated**: Legacy default connection type is deprecated

- **Impact**: Flows using default auth may break in future
- **Scope**: Default authentication connections
- **Workaround**: Migrate to OAuth, Service Principal, or Certificate authentication
- **Affected Operations**: All operations using default auth
</limitation>

<limitation id="lim-002" severity="medium">
**Non-Shareable User Connections**: OAuth connections cannot be shared between users

- **Impact**: Each user must create own connection when apps shared
- **Scope**: OAuth authentication only (Service Principal and Certificate are shareable)
- **Workaround**: Use Service Principal or Certificate auth for shared scenarios
- **Affected Operations**: All operations with user-based OAuth
</limitation>

## Data Operations

<limitation id="lim-003" severity="medium">
**NoSQL Tables Require Partition ID**: NoSQL (Elastic) tables need partition ID for operations

- **Impact**: Cannot perform operations without specifying partition
- **Scope**: NoSQL/Elastic table operations
- **Workaround**: Always specify partition ID for elastic tables
- **Affected Operations**: All row operations on NoSQL tables
</limitation>

<limitation id="lim-004" severity="low">
**Multi-Environment Actions**: Some actions limited to current environment

- **Impact**: Cannot access data across environments without "WithOrganization" variant
- **Scope**: Standard actions
- **Workaround**: Use "WithOrganization" action variants for cross-environment
- **Affected Operations**: Standard CRUD actions
</limitation>
</critical_limitations>

<authentication>
## Supported Authentication Methods

### OAuth (User Context)
- Flow type: Authorization Code
- Required permissions: Dataverse user permissions
- Token refresh: Automatic
- Shareable: No

### Service Principal (App Context)
- Setup: Azure AD app registration with Client ID/Secret
- Required permissions: Application user in Dataverse
- Token refresh: Automatic
- Shareable: Yes

### Client Certificate Authentication
- Setup: PFX certificate upload
- Required permissions: Application user with certificate
- Token refresh: Automatic
- Shareable: Yes

### Default [DEPRECATED]
- Status: Deprecated - migrate to other methods
- Migration path: Use OAuth, Service Principal, or Certificate auth

## Required Permissions

### User Permissions (OAuth)
- Table-level permissions based on security roles
- Organization/Business Unit/User scope based on access level
- Read/Write/Create/Delete permissions per table

### Application Permissions (Service Principal)
- Application user must be created in Dataverse
- Security roles assigned to application user
- Same permission structure as regular users
</authentication>

<common_use_cases>
## 1. Form Data Storage
Store Power Apps form submissions in Dataverse tables

## 2. Automated Data Sync
Sync data between Dataverse and external systems (SQL, SharePoint)

## 3. Business Process Automation
Trigger flows when Dataverse records change (approvals, notifications)

## 4. Data Validation and Enrichment
Validate incoming data, enrich with lookups, update related records

## 5. Reporting and Analytics
Extract Dataverse data for Power BI reports or Excel analysis
</common_use_cases>

<best_practices>
## Performance Optimization
1. **Use Batch Operations**: Combine multiple operations in changesets for better performance
2. **Filter at Source**: Use OData filters to reduce data transfer
3. **Select Specific Columns**: Only retrieve needed columns with $select

## Reliability & Error Handling
1. **Use Upsert**: Prefer Upsert over separate Get + Update/Create logic
2. **Implement Retry**: Configure retry for transient 429 errors
3. **Use Changesets**: Wrap related operations in transactions

## Security Best Practices
1. **Use Service Principal**: Prefer app authentication for production flows
2. **Apply Least Privilege**: Grant minimum necessary permissions
3. **Audit Data Access**: Enable Dataverse auditing for sensitive tables
</best_practices>

<troubleshooting>
## Common Errors

### Throttling (429)
<error id="err-429" http_code="429">
- **Cause**: Exceeded 6,000 calls per 5 minutes
- **Fix**: Add delays, reduce query frequency, use batch operations
</error>

### Permission Denied (403)
<error id="err-403" http_code="403">
- **Cause**: Insufficient table permissions or wrong scope
- **Fix**: Grant required permissions via security roles
</error>

### Record Not Found (404)
<error id="err-404" http_code="404">
- **Cause**: Record GUID invalid or record deleted
- **Fix**: Verify GUID, handle deletion scenarios
</error>
</troubleshooting>

<related_docs>
- **Actions**: [actions.md](./actions.md) - To be created
- **Triggers**: [triggers.md](./triggers.md) - To be created
- **Power Apps**: [Link](../PowerApps/overview.md) - App integration
- **Official Docs**: https://learn.microsoft.com/en-us/connectors/commondataserviceforapps/
</related_docs>

<metadata_summary>
- **Last Updated**: 2025-10-31
- **Fetch Date**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 40%
- **Validation Status**: Validated
- **Next Review**: 2025-11-30
</metadata_summary>
