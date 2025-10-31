# Power Apps Connector Overview

---
type: connector-overview
connector_name: Power Apps (for Makers)
connector_type: standard
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [powerapps, app, canvas app, maker, publish, permission, environment]
related_connectors: [Dataverse, SharePoint, Office 365 Users]
api_limits:
  calls_per_minute: 1.67
  calls_per_hour: 100
official_docs_url: https://learn.microsoft.com/en-us/connectors/powerappsforappmakers/
---

<official_docs>
https://learn.microsoft.com/en-us/connectors/powerappsforappmakers/
</official_docs>

<description>
Power Apps for Makers connector enables automation of Power Apps management tasks including app publishing, version control, permission management, and resource retrieval across environments. Supports 20+ operations for managing apps, connections, connectors, and role assignments programmatically.
</description>

<capabilities>
## Core Capabilities
- App version management (get, publish, remove, restore)
- Permission and role assignment management
- App display name configuration
- Connection and connector lifecycle management
- Environment metadata retrieval
- Pagination support for large result sets

## Supported Operations
- **App Management**: Get/Publish/Remove/Restore app versions, Set display name
- **Permissions**: Edit role assignments for apps/connections/connectors
- **Resource Retrieval**: Get apps, connections, connectors, environments
- **Access Control**: Retrieve and modify role assignments with user notifications

## Integration Features
- Version restore functionality
- Granular RBAC via role assignments
- Comprehensive environment metadata
- Paginated results for large datasets
</capabilities>

<api_limits>
## Rate Limits
- **100 API calls per 60 seconds** per connection
- Throttling scope: per connection
- Retry-After header: yes
</api_limits>

<critical_limitations>
<limitation id="lim-001" severity="low">
**No Explicit Documented Limitations**: Connector documentation doesn't list critical operational constraints beyond throttling

- **Impact**: Minimal - standard throttling applies
- **Scope**: All operations
- **Workaround**: N/A
</limitation>
</critical_limitations>

<authentication>
## Supported Authentication Methods
### OAuth (Only Method)
- Flow type: Authorization Code
- Required permissions: Environment admin or app owner permissions
- Token refresh: Automatic
</authentication>

<common_use_cases>
## 1. Automated App Publishing
Publish app versions after successful testing

## 2. Permission Management
Automatically assign app permissions based on SharePoint groups

## 3. App Version Backup
Archive app versions before major changes

## 4. Environment Inventory
Report on all apps across environments

## 5. Connection Lifecycle Management
Monitor and manage connection health
</common_use_cases>

<best_practices>
## Performance Optimization
1. **Paginate Large Results**: Use pagination for environment/app lists
2. **Cache Metadata**: Store frequently accessed app info

## Reliability
1. **Verify Versions Before Restore**: Always validate version before restoring
2. **Test in Dev First**: Test version operations in dev environment
</best_practices>

<troubleshooting>
### Throttling (429)
<error id="err-429" http_code="429">
- **Cause**: Exceeded 100 calls per 60 seconds
- **Fix**: Add delays between operations
</error>
</troubleshooting>

<related_docs>
- **Official Docs**: https://learn.microsoft.com/en-us/connectors/powerappsforappmakers/
</related_docs>

<metadata_summary>
- **Last Updated**: 2025-10-31
- **Fetch Date**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 40%
</metadata_summary>
