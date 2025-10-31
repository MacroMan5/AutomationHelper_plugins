# SharePoint Online - Connector Overview

---
type: connector-overview
connector_name: SharePoint
connector_type: standard
publisher: Microsoft
category: Content and Files
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [sharepoint, document, list, library, collaboration, file, folder, approval, hub site, syntex]
capabilities: [document_management, list_operations, file_operations, approval_workflows, sharing, hub_governance, document_generation]
api_limits:
  calls_per_minute: 10
  calls_per_hour: 600
  bandwidth_mb_per_minute: 1000
availability:
  power_automate: true
  logic_apps: true
  power_apps: true
  copilot_studio: true
pricing_tier: standard
---

<official_docs>
https://learn.microsoft.com/en-us/connectors/sharepointonline/
</official_docs>

<description>
The SharePoint connector enables organizations to manage documents and collaborate with colleagues, partners, and customers. It provides comprehensive capabilities for document management, list operations, approval workflows, and content governance across SharePoint Online and on-premises SharePoint 2016/2019 deployments (via On-Premises Data Gateway).
</description>

---

## Capabilities Overview

<capabilities>
**Core Features**:
- **Document Management**: Create, read, update, delete files and folders
- **List Operations**: Manage list items with CRUD operations and change tracking
- **File Operations**: Upload, download, copy, move, check in/out, attachments (up to 90MB)
- **Folder Operations**: Create, copy, move, extract archives
- **Approval Workflows**: Content approval, approval requests, status management
- **Sharing & Permissions**: Create sharing links, grant access, manage permissions
- **Hub Site Governance**: Join requests, approval workflows, site association
- **Document Generation**: Microsoft Syntex template-based document creation
- **Attachment Management**: Add, retrieve, delete item attachments (max 90MB)

**Deployment Support**:
- SharePoint Online (native)
- On-premises SharePoint 2016/2019 (via On-Premises Data Gateway)
</capabilities>

---

## API Limits and Throttling

<api_limits>
| Limit Type | Value | Scope |
|------------|-------|-------|
| **API Calls** | 600 calls | Per 60 seconds per connection |
| **Bandwidth Transfer** | 1000 MB | Per 60 seconds per connection |
| **Attachment Size** | 90 MB | Maximum per file upload/attachment |
| **Image Upload** | 90 MB | Maximum via Power Apps |

**Throttling Behavior**:
- Exceeding 600 calls/60s triggers HTTP 429 (Too Many Requests)
- Bandwidth limit applies to cumulative upload/download operations
- Throttling is per-connection (multiple connections = independent limits)

**Throttle Management**:
- Add delays between API calls in loops (minimum 1-2 seconds)
- Use batch operations where possible
- Implement server-side filtering to reduce call volume
- Monitor flow execution frequency to avoid rate limit violations
</api_limits>

---

## Critical Limitations

<critical_limitations>

<limitation id="lim-sp-overview-001" severity="critical">
**List & Library Template Support**: Power Automate flows for lists are only supported in **generic lists and generic document libraries**. Custom list and library templates are currently NOT supported including:
- Announcements lists
- Contacts lists
- Events lists
- Tasks lists
- Custom library templates

**Impact**: Flows targeting these templates will fail or exhibit unexpected behavior.

**Workaround**: Migrate data to generic lists or use SharePoint HTTP connector for advanced scenarios.
</limitation>

<limitation id="lim-sp-overview-002" severity="high">
**Naming Restrictions - Periods in List Names**: Lists containing periods in names (e.g., "MySharePoint.List") cause errors when used as dynamic values in flow actions.

**Error Example**: Dynamic content resolution fails with "Property not found" errors.

**Workaround**:
1. Select list from dropdown menu (not dynamic value)
2. Use list GUID instead of display name
3. Reference via list ID property
</limitation>

<limitation id="lim-sp-overview-003" severity="high">
**Delegation Limits**: SharePoint lists with more than 5,000 items are subject to delegation limits:
- **Non-delegable fields**: ID (except `=` operation), Thumbnail, ModerationStatus, VersionNumber, ContentType
- **Non-delegable operators**: `NOT` operator not supported
- **Person field**: Only Email and DisplayName properties are delegable

**Impact**: Queries may return incomplete results if delegation threshold exceeded.

**Best Practice**:
- Use indexed columns in filters
- Implement server-side ODATA filtering with Get Items action
- Apply "Limit Columns by View" parameter
</limitation>

<limitation id="lim-sp-overview-004" severity="high">
**Guest User Restrictions**: Guest user accounts cannot view or retrieve dropdown list information in Power Apps and flows.

**Workaround**: Grant direct SharePoint permissions to guest users or use service accounts.
</limitation>

<limitation id="lim-sp-overview-005" severity="medium">
**Sensitivity Labels**: Sensitivity labels cannot be set on files via the SharePoint connector.

**Workaround**: Apply labels manually or use Graph API via HTTP action.
</limitation>

<limitation id="lim-sp-overview-006" severity="high">
**Conditional Access Policies**: Microsoft Entra ID (Azure AD) Conditional Access policies may block connector access including:
- Multi-factor authentication (MFA) requirements
- Device compliance requirements
- Network location-based restrictions

**Troubleshooting**: Review Conditional Access configuration in Azure AD portal.
</limitation>

<limitation id="lim-sp-overview-007" severity="medium">
**Cross-Drive Operations**: Cross-drive functionality is not supported. Files must be managed within the same SharePoint site/drive.

**Impact**: Cannot directly copy/move files between different site collections without explicit parameters.
</limitation>

<limitation id="lim-sp-overview-008" severity="medium">
**Character Encoding in Archives**: Extract Folder V2 action may distort special characters during extraction when archives don't adhere to zip specification standards.

**Workaround**: Create archives using modern tools supporting UTF-8 encoding and language encoding headers.
</limitation>

<limitation id="lim-sp-overview-009" severity="medium">
**Term Set Label Updates**: Changes to term set labels are not automatically reflected in flows or apps.

**Workaround**: Directly edit affected list item from SharePoint to force refresh.
</limitation>

<limitation id="lim-sp-overview-010" severity="low">
**Image Column Caching**: Image column variants (Small, Medium, Large) are auto-generated and cached, requiring ~30 seconds to refresh after updates.

**Impact**: Flows may retrieve stale image variants immediately after update.
</limitation>

<limitation id="lim-sp-overview-011" severity="medium">
**Custom Forms Limitation**: Custom forms for document libraries only support editing custom metadata, not library-level settings.

**Note**: Custom forms cannot be transferred between environments; must be recreated.
</limitation>

<limitation id="lim-sp-overview-012" severity="low">
**Built-In Flows**: Built-in SharePoint flows (e.g., "Request sign-off") cannot be edited in Power Automate portal.

**Workaround**: Create custom flows from scratch for full editing capabilities.
</limitation>

<limitation id="lim-sp-overview-013" severity="critical">
**Deletion Triggers**: Only site collection administrators can use file/item deletion triggers.

**Impact**: Regular users cannot create flows with deletion triggers.
</limitation>

</critical_limitations>

---

## Authentication & Connection

<authentication>
**Default Authentication Method**:
- **Username** (securestring, required): User principal name or email
- **Password** (securestring, required): Account password
- **On-Premises Data Gateway** (optional): Required for SharePoint 2016/2019 on-premises

**Connection Model**: Non-shareable connections
- When sharing Power Apps, recipients must create their own explicit SharePoint connections
- Service principal authentication not supported (use OAuth)

**Required Permissions**:
- **Read operations**: Site visitor permissions minimum
- **Write operations**: Site member/contributor permissions
- **Deletion operations**: Site collection administrator role required
- **Approval workflows**: Appropriate approval permissions
</authentication>

---

## Common Use Cases

<common_use_cases>

**1. Document Approval Workflows**
```
Trigger: When file created (properties only)
→ Get file metadata
→ Create approval request
→ Condition: Approval response
  → Approved: Set content approval status = Approve
  → Rejected: Move file to "Rejected" folder, Send notification
```
**Benefits**: Automated content governance, audit trail

---

**2. List Item Synchronization**
```
Trigger: When item created or modified
→ Get item changes (detect modified fields)
→ Condition: Specific field changed
→ Update corresponding item in target list
→ Log synchronization to tracking list
```
**Benefits**: Multi-list consistency, change tracking

---

**3. File Management Automation**
```
Trigger: When file created
→ Check filename pattern (validation)
→ Extract metadata from filename
→ Update file properties with metadata
→ Move to organized folder structure
→ Send notification to stakeholders
```
**Benefits**: Automated file organization, metadata enrichment

---

**4. Content Publishing Workflows**
```
Schedule: Daily at 8 AM
→ Get items (filter: PublishDate = Today AND Status = Ready)
→ Apply to each item:
  → Generate document using Syntex
  → Upload to public library
  → Update item status = Published
  → Create sharing link
  → Send email with link
```
**Benefits**: Scheduled content publication, consistent delivery

---

**5. Hub Site Governance**
```
Trigger: When site requests hub join
→ Create approval request
→ Condition: Approval response
  → Approved:
    → Approve hub site join request
    → Notify requestor with approval token
    → Join hub site with token
  → Rejected:
    → Cancel hub site join request
    → Send rejection notification
```
**Benefits**: Controlled hub site expansion, governance compliance

---

**6. Syntex Document Generation**
```
Trigger: When item created in "Document Requests" list
→ Get item properties (customer name, contract date, amount)
→ Generate document using Syntex template
→ Upload to "Contracts" library
→ Update request item with document link
→ Send email to requester
```
**Benefits**: Automated document creation from templates, consistency

---

**7. Attachment Management**
```
Trigger: When item created or modified
→ Get attachments
→ Apply to each attachment:
  → Get attachment content
  → Upload to document library (organized storage)
  → Delete attachment from item (cleanup)
  → Update item with library link
```
**Benefits**: Centralized file storage, attachment size optimization

</common_use_cases>

---

## Best Practices

<best_practices>

### Performance Optimization

1. **Use "Limit Columns by View" Parameter**
   - Reduces payload size for lists with many columns
   - Avoids delegation threshold issues
   - Improves flow execution speed
   ```
   Get Items action: Select view with only required columns
   ```

2. **Server-Side Filtering with ODATA**
   - Apply filters in "Filter Query" parameter (delegable)
   - Use indexed columns in filter expressions
   - Example: `Status eq 'Active' AND Priority lt 3`

3. **Batch Operations**
   - Group multiple items in single Get Items call instead of multiple Get Item calls
   - Use "Top Count" to limit results appropriately

4. **Folder-Scoped Triggers**
   - Limit triggers to specific folders using "Limit Entries to Folder"
   - Reduces trigger execution frequency

### Reliability Patterns

1. **Error Handling with Scopes**
   ```
   Scope: Main Operations
   → Actions inside scope

   Scope: Error Handling (Configure run after: has failed)
   → Log error to tracking list
   → Send admin notification
   → Implement retry logic
   ```

2. **ETag Management**
   - Get file metadata before approval status changes to obtain ETag
   - Prevents concurrency conflicts
   ```
   Get file metadata → Capture ETag → Set approval status (use ETag)
   ```

3. **Idempotency**
   - Implement duplicate detection (track processed item IDs)
   - Use unique identifiers to prevent double-processing

4. **Versioning Requirement**
   - Enable list versioning for "Get Item Changes" operation effectiveness
   - Version history provides change tracking capability

### Security & Governance

1. **Least Privilege Access**
   - Grant minimum required permissions to service accounts
   - Use separate connections for read vs write operations

2. **Sharing Link Scope**
   - Use "Organization" scope for internal sharing (not "Anyone")
   - Set expiration dates on anonymous links
   - Example: `Link Scope: Organization, Expiration: 2025-12-31`

3. **Approval Checkpoints**
   - Implement approval workflows for critical operations (deletions, moves)
   - Log approval decisions for audit trail

4. **Conditional Access Compliance**
   - Test flows with Conditional Access policies applied
   - Document policy requirements for flow execution

### Data Management

1. **Indexed Columns**
   - Create column indexes for frequently filtered fields
   - Improves query performance on large lists (>5000 items)

2. **Archival Strategy**
   - Move old items to archive lists instead of deletion
   - Implement retention policies for compliance

3. **Attachment Size Monitoring**
   - Validate attachment size < 90MB before upload
   - Implement file size checks in flows

4. **Change Tracking**
   - Use "Get Item Changes" for efficient delta queries
   - Specify time window with "Since" parameter (version label or ISO 8601 date)

</best_practices>

---

## Troubleshooting Guide

<troubleshooting>

<error id="err-sp-overview-001" severity="high">
**Error**: "CannotDisableTriggerConcurrency"

**Cause**: Concurrency control cannot be disabled after being enabled on trigger.

**Solution**:
1. Export flow as JSON
2. Edit JSON to remove 'concurrency control' section from trigger configuration
3. Delete original flow
4. Import edited JSON as new flow
</error>

<error id="err-sp-overview-002" severity="high">
**Error**: Incomplete dataset returned from Get Items action

**Cause**: Delegation limit exceeded (list >5000 items with non-delegable filter).

**Solutions**:
1. Use indexed columns in filter expressions
2. Apply "Limit Columns by View" parameter
3. Implement client-side filtering for non-delegable conditions
4. Use SQL Server functions for complex queries
</error>

<error id="err-sp-overview-003" severity="medium">
**Error**: "For a selected item" trigger not visible in SharePoint

**Cause**: Flow not in default Power Automate environment.

**Solution**:
1. Create flow in default environment
2. Export and import to default environment if needed
3. Verify flow is published and enabled
4. Refresh SharePoint page after flow creation
</error>

<error id="err-sp-overview-004" severity="medium">
**Error**: Guest users cannot see dropdown list data

**Cause**: Guest accounts lack permission to retrieve SharePoint metadata via connector.

**Solutions**:
1. Grant direct SharePoint site permissions to guest users
2. Use service account with full permissions
3. Avoid dynamic dropdowns for guest user scenarios
</error>

<error id="err-sp-overview-005" severity="high">
**Error**: Dynamic value errors with list names containing periods

**Example**: "MySharePoint.List" fails in dynamic content

**Solutions**:
1. Select list from dropdown (not dynamic value)
2. Use list GUID: `lists/` + GUID
3. Reference via `ID` property instead of display name
</error>

<error id="err-sp-overview-006" severity="high">
**Error**: Conditional Access blocking flow execution

**Symptoms**: 403 Forbidden or authentication failures

**Solutions**:
1. Review Conditional Access policies in Azure AD
2. Verify MFA requirements are met
3. Check device compliance status
4. Whitelist Power Automate service IPs if network-restricted
5. Contact IT admin for policy exceptions
</error>

<error id="err-sp-overview-007" severity="medium">
**Error**: Special characters distorted in extracted zip files

**Cause**: Archive not using UTF-8 encoding or standard zip specification.

**Solutions**:
1. Re-create archive using modern zip tool (.NET Zip Archive SDK)
2. Ensure UTF-8 encoding enabled
3. Include language encoding headers in archive
4. Test with ASCII-only filenames if possible
</error>

<error id="err-sp-overview-008" severity="medium">
**Error**: Term set labels not updating in flow/app

**Cause**: Label changes cached and not auto-refreshed.

**Solutions**:
1. Manually edit affected list item from SharePoint UI to force refresh
2. Re-save flow after term set updates
3. Clear browser cache and reload
</error>

<error id="err-sp-overview-009" http_code="429" severity="critical">
**Error**: Too Many Requests - Throttling

**Cause**: Exceeded 600 API calls per 60 seconds per connection.

**Solutions**:
1. Add Delay actions in loops (minimum 1-2 seconds)
2. Reduce trigger polling frequency
3. Use batch operations (Get Items instead of multiple Get Item)
4. Distribute load across multiple connections
5. Implement retry logic with exponential backoff

**Throttle Formula**:
```
Max concurrent flows = 600 / (calls per flow * flows per minute)
Example: Flow with 5 calls = 600 / (5 * 10) = 12 concurrent flows max
```
</error>

</troubleshooting>

---

## Connector Metadata

<connector_metadata>
| Property | Value |
|----------|-------|
| **Publisher** | Microsoft |
| **Service Class** | Standard |
| **Category** | Content and Files |
| **Pricing Tier** | Standard (included in Microsoft 365) |
| **Website** | products.office.com/sharepoint/collaboration |
| **Privacy Policy** | privacy.microsoft.com |
| **Contact Email** | idcknowledgeeco@microsoft.com |
| **Available In** | Power Automate, Logic Apps, Power Apps, Copilot Studio |
| **Regions** | All Power Automate, Logic Apps, Power Apps regions |
| **On-Premises Support** | Yes (via On-Premises Data Gateway for SharePoint 2016/2019) |
</connector_metadata>

---

## Related Connectors

<related_connectors>
- **SharePoint HTTP**: Advanced REST API operations not covered by standard connector
- **OneDrive for Business**: Personal file storage (SharePoint-backed)
- **Microsoft 365 Users**: User profile lookups for People fields
- **Approvals**: Enhanced approval workflows
- **Microsoft Syntex**: Document generation and classification
- **Microsoft Forms**: Form responses integrated with SharePoint lists
- **Excel Online (Business)**: Excel files stored in SharePoint libraries
- **Microsoft Teams**: SharePoint as backing store for Teams files
</related_connectors>

---

## Integration Patterns

<integration_patterns>

**Pattern 1: Multi-Site File Sync**
```
Trigger: File created in Site A
→ Get file content
→ Create file in Site B (with conflict resolution)
→ Update metadata in both locations
→ Log sync operation
```

**Pattern 2: Approval with Versioning**
```
Trigger: File modified
→ Get file metadata (capture ETag)
→ Create approval request
→ Condition: Approval outcome
  → Approved: Set content approval status (use ETag)
  → Rejected: Discard changes, restore previous version
```

**Pattern 3: Hub Governance Workflow**
```
Trigger: Site requests hub join
→ Set hub join status to pending
→ Create approval request (send to hub admin)
→ Condition: Approval response
  → Approved:
    → Approve hub join
    → Provide approval token
    → Join hub site with correlation ID
  → Rejected:
    → Cancel hub join request
    → Notify requester
```

**Pattern 4: Syntex + SharePoint Integration**
```
Trigger: Item created in request list
→ Get item properties
→ Generate document using Syntex
→ Upload to library
→ Update item with document link
→ Create sharing link
→ Send notification email
```

**Pattern 5: Change Tracking & Audit**
```
Trigger: Item or file modified
→ Get item changes (since last check)
→ Parse changed fields
→ Log changes to audit list
→ Condition: Critical field changed
  → Send alert to stakeholders
```

</integration_patterns>

---

## Known Issues & Workarounds

<known_issues>

| Issue | Impact | Workaround |
|-------|--------|------------|
| **Concurrency control disabled permanently** | Cannot re-enable once disabled | Export/edit JSON, remove concurrency section, re-import |
| **Special characters in zip extraction** | Character distortion | Use UTF-8 encoded archives with .NET Zip Archive SDK |
| **Term set labels stale** | Outdated labels in flows/apps | Manually edit list item to force refresh |
| **Custom forms not transferable** | Cannot move between environments | Recreate or create in target environment initially |
| **Incomplete delegation results** | Missing items beyond threshold | Use indexed columns, client-side filtering, or SQL Server |
| **Guest user dropdown issues** | Cannot see list data | Grant direct permissions or use service account |
| **Period in list names** | Dynamic value errors | Use dropdown selection or list GUID |
| **Cross-drive limitations** | Cannot move between sites easily | Use explicit source/destination parameters |
| **Image variant caching** | ~30s delay for refreshed images | Account for delay or use direct library links |

</known_issues>

---

## Data Type Mappings & Delegation

For comprehensive data type mappings and delegable function tables, refer to:
- **Power Apps SharePoint Documentation**: Detailed delegation support matrix
- **SharePoint REST API Reference**: Field type specifications
- **ODATA Query Reference**: Supported operators and functions

---

## Version History

**Version 1.0** (2025-10-31):
- Initial comprehensive overview documentation
- Format v2 with YAML frontmatter and XML tags
- 13 critical limitations documented
- 51 actions and 13 triggers covered
- Troubleshooting guide with 9 common errors
- 7 workflow patterns and integration examples

---

**Last Updated**: 2025-10-31
**Fetch Date**: 2025-10-31
**Documentation Format**: Agent-Optimized v2
