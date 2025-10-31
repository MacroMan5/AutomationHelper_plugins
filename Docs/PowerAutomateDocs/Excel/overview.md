# Excel Online (Business) Connector Overview

---
type: connector-overview
connector_name: Excel Online (Business)
connector_type: standard
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [excel, spreadsheet, workbook, table, row, worksheet, cells, data, office scripts]
related_connectors: [SharePoint, OneDrive for Business, Office 365 Outlook]
api_limits:
  calls_per_minute: 1.67
  calls_per_hour: 100
  max_file_size_mb: 25
  max_row_retrieval: 256
  run_script_calls_per_day: 1600
official_docs_url: https://learn.microsoft.com/en-us/connectors/excelonlinebusiness/
---

<official_docs>
https://learn.microsoft.com/en-us/connectors/excelonlinebusiness/
https://learn.microsoft.com/en-us/office/dev/scripts/testing/platform-limits
</official_docs>

<description>
Excel Online (Business) connector enables automation of Excel workbook operations stored in OneDrive for Business, SharePoint document libraries, or Microsoft 365 Groups. Supports table operations (add, update, delete, list rows), worksheet management, and Office Scripts execution for complex data manipulation scenarios.
</description>

<capabilities>
## Core Capabilities
- CRUD operations on Excel table rows (Create, Read, Update, Delete)
- Table and worksheet management (create, list, query)
- Row filtering, sorting, and pagination
- Office Scripts execution for advanced automation
- Integration with OneDrive, SharePoint, and Teams file locations
- Support for .xlsx and .xlxb file formats

## Supported Operations
- **Row Operations**: Add, update, delete, get single row, list multiple rows with filters
- **Table Management**: Create tables, get table list, add key columns for row identification
- **Worksheet Management**: Create worksheets, list worksheets in workbook
- **Script Execution**: Run Office Scripts from default location or SharePoint libraries
- **Bulk Operations**: List rows with OData filtering and ordering

## Integration Features
- OneDrive for Business and SharePoint file access
- OData query support for filtering and sorting
- Key column-based row identification for updates/deletes
- Automatic pagination for large datasets (256 rows default)
- File locking to prevent concurrent modification conflicts
</capabilities>

<api_limits>
## Rate Limits

**Connection-Level Throttling**
- **100 API calls per 60 seconds** per connection
- Throttling scope: per connection
- Retry-After header: yes

**Action-Specific Limits**
- Run script: **3 calls per 10 seconds** and **1,600 calls per day per user** (resets at 12:00 AM UTC)
- List rows: Returns **256 rows by default** (use $skip, $top for pagination)

**Throttling Behavior**
- HTTP Status: 429 (Too Many Requests)
- Error message: "Too many requests" or "The request was throttled"
- Automatic retry: yes (with exponential backoff)

## Size Limits

**File Operations**
- Max file size: **25 MB**
- Max request payload: **5 MB**
- Max response size: **5 MB**
- Supported formats: .xlsx, .xlxb

**Data Operations**
- Max rows per table: **64,000 auto-generated ID rows**
- Max columns per request: **500 columns**
- Max range cells: **5,000,000 cells**
- Default rows retrieved: **256 rows** (configurable with $top, $skip)

**Script Operations**
- Max parameters size for Run script: **30 MB** (30,000,000 bytes)

## Timeout Limits
- Default timeout: **120 seconds** for synchronous operations
- Max timeout: **120 seconds**
- Long-running operations: Not supported (use Office Scripts for complex operations)
- File lock duration: **Up to 6 minutes** after use
</api_limits>

<critical_limitations>
## File Access & Permissions

<limitation id="lim-001" severity="critical">
**Write Access Required**: User must have write permissions to Excel file

- **Impact**: Read-only files return "502 BadGateway" error
- **Scope**: All actions (even read operations like List rows)
- **Workaround**: Grant write access to service account, or copy file to writable location
- **Affected Operations**: All actions

**Example Scenario**: Flow fails with 502 error when accessing shared read-only Excel file
</limitation>

<limitation id="lim-002" severity="high">
**Concurrent Modification Conflicts**: Multiple clients modifying same file causes merge conflicts

- **Impact**: Data corruption, duplicate entries, operation failures
- **Scope**: When Excel Desktop, Excel Web, Power Automate, or Power Apps access same file simultaneously
- **Workaround**: Use single automation client, implement file locking strategy, or use SharePoint list instead
- **Affected Operations**: All write operations

**Example Scenario**: User edits Excel in browser while Power Automate flow writes rows, causing data loss
</limitation>

## Data Structure & Format

<limitation id="lim-003" severity="high">
**Table Required for Row Operations**: Actions require data formatted as Excel table, not range

- **Impact**: Cannot use actions on regular cell ranges
- **Scope**: All row operations (Add, Update, Delete, Get, List)
- **Workaround**: Convert range to table in Excel (Insert → Table)
- **Affected Operations**: Add row, Update row, Delete row, Get row, List rows

**Example Scenario**: Flow fails when trying to add row to Sheet1 without formatted table
</limitation>

<limitation id="lim-004" severity="medium">
**Key Column Required for Update/Delete**: Update and Delete actions require key column for row identification

- **Impact**: Cannot update/delete without unique identifier column
- **Scope**: Update row, Delete row actions
- **Workaround**: Use "Add a key column to a table" action to create identifier column
- **Affected Operations**: Update row, Delete row

**Example Scenario**: Cannot update row by employee name without key column containing unique IDs
</limitation>

<limitation id="lim-005" severity="medium">
**Single Filter Per Column**: Only one filter operation allowed per column

- **Impact**: Cannot combine AND/OR conditions on same column (e.g., "Status eq 'Active' or Status eq 'Pending'")
- **Scope**: List rows with OData $filter parameter
- **Workaround**: Retrieve all rows, filter in flow with Filter Array or Condition actions
- **Affected Operations**: List rows present in a table

**Example Scenario**: Cannot filter rows where "Amount > 100 AND Amount < 1000" in single query
</limitation>

<limitation id="lim-006" severity="medium">
**Single Sort Column**: Only one column can be sorted at a time

- **Impact**: Cannot sort by multiple columns (e.g., "sort by Department, then by Name")
- **Scope**: List rows with OData $orderby parameter
- **Workaround**: Sort additional columns in flow with Sort Array or Office Script
- **Affected Operations**: List rows present in a table
</limitation>

## Performance & Reliability

<limitation id="lim-007" severity="high">
**File Lock After Use**: Excel file locked for up to 6 minutes after operation

- **Impact**: Subsequent operations may fail with file busy error
- **Scope**: All file modifications
- **Workaround**: Add 1-2 minute delay between operations, implement retry logic
- **Affected Operations**: All write actions

**Example Scenario**: Second flow run fails because file still locked from previous run 3 minutes ago
</limitation>

<limitation id="lim-008" severity="high">
**Complex Formulas Cause Timeouts**: Heavy formulas with large row counts trigger 120-second timeout

- **Impact**: Duplicate row insertions, incomplete operations
- **Scope**: Tables with volatile formulas (NOW(), TODAY(), RAND(), etc.) or heavy calculations
- **Workaround**: Use empty worksheet for data insertion, move formula calculations elsewhere, or use Office Scripts
- **Affected Operations**: Add row, Update row (when formulas recalculate)

**Example Scenario**: Adding row to table with 10,000 rows and complex VLOOKUP formulas times out, creates duplicate
</limitation>

<limitation id="lim-009" severity="medium">
**256 Row Default Retrieval**: List rows returns only 256 rows by default

- **Impact**: Missing data if table has more than 256 rows
- **Scope**: List rows present in a table action
- **Workaround**: Use $top and $skip parameters for pagination, or retrieve in batches with Do Until loop
- **Affected Operations**: List rows present in a table

**Example Scenario**: Table has 1,000 rows, but flow only processes first 256 rows
</limitation>

<limitation id="lim-010" severity="low">
**30-Second Change Propagation**: Changes may take up to 30 seconds to be visible

- **Impact**: Subsequent reads may not reflect recent writes
- **Scope**: All operations when querying immediately after write
- **Workaround**: Add 30-second delay after write before reading, or retry with delay
- **Affected Operations**: All actions when chained closely

**Example Scenario**: Add row then immediately Get row returns 404 for new row
</limitation>

## Data Type & Column Constraints

<limitation id="lim-011" severity="medium">
**Numeric-Only Column Headers Unsupported**: Column names containing only numbers cause unexpected behavior

- **Impact**: Unable to reference columns, data mapping errors
- **Scope**: All row operations
- **Workaround**: Rename columns to include at least one letter (e.g., "Col1", "Year2024")
- **Affected Operations**: All row actions

**Example Scenario**: Table with columns "2024", "2025" fails to map correctly in flow
</limitation>

<limitation id="lim-012" severity="medium">
**Hidden Columns Incompatible with OData**: Hidden columns cannot be used in $filter or $orderby

- **Impact**: Cannot filter/sort by hidden columns
- **Scope**: List rows with OData parameters
- **Workaround**: Unhide columns or use Office Script to filter
- **Affected Operations**: List rows with $filter or $orderby
</limitation>

<limitation id="lim-013" severity="low">
**Case-Sensitive Key Column Field Names**: Key column names are case-sensitive in queries

- **Impact**: Query fails if case doesn't match exactly
- **Scope**: Update row, Delete row, Get row actions
- **Workaround**: Ensure exact case match in key column references
- **Affected Operations**: Actions using key column identification
</limitation>

## File Picker & Location

<limitation id="lim-014" severity="low">
**200 Item File Picker Limit**: File picker displays maximum 200 items per folder

- **Impact**: Cannot select files beyond first 200 in folder via UI
- **Scope**: File selection in Power Automate designer
- **Workaround**: Enter file path manually, organize files in subfolders, or use dynamic file path
- **Affected Operations**: All actions during configuration
</limitation>

<limitation id="lim-015" severity="medium">
**Guest User Access Issues**: Guest users from different tenants receive HTTP 404 errors

- **Impact**: Cross-tenant scenarios fail
- **Scope**: Guest user connections
- **Workaround**: Use internal service account or grant B2B access properly
- **Affected Operations**: All actions for guest users
</limitation>

## Unsupported Features

<limitation id="lim-016" severity="medium">
**Pivot Tables Unsupported**: Connector cannot interact with pivot tables

- **Impact**: Cannot read or update pivot table data directly
- **Scope**: All actions on pivot tables
- **Workaround**: Use source data table instead, or manipulate via Office Scripts
- **Affected Operations**: All row operations on pivot tables
</limitation>

<limitation id="lim-017" severity="low">
**Run Script Unavailable in Sovereign Clouds**: Office Scripts not available in GCC, GCC High, DoD

- **Impact**: Advanced automation scenarios blocked in government clouds
- **Scope**: Run script actions only
- **Workaround**: Use standard actions or move workload to commercial cloud
- **Affected Operations**: Run script, Run script from SharePoint library
</limitation>
</critical_limitations>

<authentication>
## Supported Authentication Methods

### OAuth 2.0 (Only Method)
- Flow type: Authorization Code
- Required scopes: Files.ReadWrite.All (Graph API)
- Token refresh: Automatic
- Account type: Organizational accounts (Azure AD) and personal Microsoft accounts (OneDrive Personal)

### Service Principal
- Supported: Yes (via Azure AD app registration)
- Setup: Register app, grant Files.ReadWrite.All, use in Power Automate connection
- Limitations: Requires admin consent for organizational files

## Required Permissions

### Delegated Permissions (User Context)
- **Files.ReadWrite**: Read and write files user can access
- **Files.ReadWrite.All**: Read and write all files user can access
- **Sites.ReadWrite.All**: Read and write items in all site collections (for SharePoint files)

### Application Permissions (App-Only Context)
- **Files.ReadWrite.All**: Read and write files in all site collections
- Note: Requires admin consent

## Permission Troubleshooting
- Insufficient permissions error: Verify user has write access to file (read-only causes 502 error)
- Guest user 404 errors: Ensure proper cross-tenant B2B access configured
- Conditional Access: May block automation - configure CA policies for service accounts
</authentication>

<common_use_cases>
## 1. Data Collection and Aggregation

**Description**: Collect form responses or data from multiple sources into Excel for reporting

**Typical Flow**:
```
Trigger: When item created (SharePoint/Forms)
↓
Action 1: Get response details/item details
↓
Action 2: Add row into Excel table - Map fields to columns
↓
Result: Centralized data repository in Excel for Power BI or analysis
```

**Key Actions**: Add a row into a table, Get tables
**Best For**: Survey aggregation, order tracking, incident logging

---

## 2. Automated Report Generation

**Description**: Generate periodic reports by extracting Excel data and distributing via email

**Typical Flow**:
```
Trigger: Scheduled (daily/weekly)
↓
Action 1: List rows present in a table - Filter by date/status
↓
Action 2: Compose HTML table - Format data
↓
Action 3: Send email (Outlook) - Include report
↓
Result: Automated distribution of Excel data reports
```

**Key Actions**: List rows present in a table, Compose
**Best For**: Daily summaries, weekly metrics, status reports

---

## 3. Data Validation and Enrichment

**Description**: Validate incoming data against Excel reference tables and enrich records

**Typical Flow**:
```
Trigger: When item created (SharePoint)
↓
Action 1: Get a row - Lookup reference data in Excel
↓
Action 2: Condition - Validate against criteria
↓
Action 3: Update SharePoint item - Add enriched data
↓
Result: Data validation and enrichment pipeline
```

**Key Actions**: Get a row, List rows present in a table (with filter)
**Best For**: Product catalog lookups, pricing validation, customer data enrichment

---

## 4. Inventory and Stock Management

**Description**: Track inventory levels and trigger alerts when stock low

**Typical Flow**:
```
Trigger: When item sold (SharePoint/SQL/API)
↓
Action 1: Get a row - Retrieve current stock level
↓
Action 2: Update a row - Decrement stock quantity
↓
Action 3: Condition - Check if below threshold
↓
Action 4: Send notification if low stock
↓
Result: Real-time inventory tracking with automated alerts
```

**Key Actions**: Get a row, Update a row
**Best For**: Product inventory, asset tracking, supply chain management

---

## 5. Approval Workflows with Excel Tracking

**Description**: Initiate approvals and track status in Excel for reporting

**Typical Flow**:
```
Trigger: When item created (Forms/SharePoint)
↓
Action 1: Add row into table - Log request
↓
Action 2: Start approval - Send to manager
↓
Action 3: Update a row - Record decision
↓
Action 4: Send notification - Inform requester
↓
Result: Approval process with Excel-based audit trail
```

**Key Actions**: Add a row into a table, Update a row
**Best For**: Purchase requests, time-off approvals, expense reports
</common_use_cases>

<best_practices>
## Performance Optimization

### API Call Efficiency
1. **Use Batch Operations**: Minimize calls by retrieving/updating multiple rows efficiently
2. **Implement Pagination**: Use $top and $skip for large datasets instead of retrieving all rows
3. **Cache Reference Data**: Store frequently accessed lookup data in variables to avoid repeated queries

### Throttling Management
1. **Add Delays Between Calls**: Insert 1-2 second delays when processing multiple rows
2. **Enable Concurrency Control**: Limit concurrent runs to 5-10 to prevent throttling
3. **Implement Retry Logic**: Use Scope with Configure run after for 429 errors

### File Lock Mitigation
1. **Serialize Operations**: Avoid concurrent access to same file from multiple flows
2. **Add Delay After Write**: Wait 30-60 seconds after write before reading again
3. **Use Separate Files**: Split data across multiple files if possible

## Reliability & Error Handling

### Retry Logic
1. **Retry on Transient Failures**: Configure retry for 429, 502, 504 errors
2. **Exponential Backoff**: Increase delay between retries (1s, 2s, 4s, 8s)

### Idempotency
1. **Use Key Columns**: Always use key column for updates to ensure idempotent operations
2. **Check Before Insert**: Verify row doesn't exist before adding

### Error Recovery
1. **Wrap in Scope**: Use Scope action with error handling for file operations
2. **Log Failures**: Record failed operations for manual review

## Security Best Practices

### Authentication
1. **Use Service Accounts**: Avoid personal accounts for production flows
2. **Grant Minimum Permissions**: Use Files.ReadWrite instead of Files.ReadWrite.All when possible

### Data Protection
1. **Validate Input**: Sanitize data before writing to Excel
2. **Implement Access Controls**: Use SharePoint permissions to control file access

## Flow Design

### Data Structure
1. **Use Tables**: Always format data as Excel table, not range
2. **Add Key Columns**: Create unique identifier columns for update/delete operations
3. **Avoid Complex Formulas**: Minimize volatile and heavy formulas in tables used by automation

### Action Ordering
1. **Create Table First**: Ensure table exists before row operations
2. **Add Key Column Early**: Add key column immediately after creating table
3. **Validate Before Update**: Check row exists before attempting update

### Variable Management
1. **Store File Path**: Store file location in variable for reusability
2. **Cache Table Names**: Store table and worksheet names for consistency
</best_practices>

<troubleshooting>
## Common Errors

### File Access Errors (502 BadGateway)

<error id="err-502" http_code="502">
- **Symptom**: "502 Bad Gateway" or "File is read-only"
- **Cause**: User lacks write permissions to file
- **Immediate Fix**:
  1. Grant write access to user/service account
  2. Check file is not checked out in SharePoint
  3. Verify file is not in read-only folder
- **Prevention**: Use service account with consistent write permissions
- **Reference**: [Limitation lim-001](#lim-001)
</error>

### Throttling Errors (429)

<error id="err-429" http_code="429">
- **Symptom**: "Too Many Requests" or "The request was throttled"
- **Cause**: Exceeded 100 calls per 60 seconds limit
- **Immediate Fix**:
  1. Add 1-2 second delay between Excel operations
  2. Enable concurrency control (limit to 10 runs)
  3. Implement exponential backoff retry
- **Prevention**: Monitor API call frequency, batch operations when possible
- **Reference**: [API Limits](#api_limits)
</error>

### Permission Errors (403)

<error id="err-403" http_code="403">
- **Symptom**: "Forbidden" or "Access denied"
- **Cause**: Insufficient permissions or file locked
- **Immediate Fix**:
  1. Verify user has access to file in OneDrive/SharePoint
  2. Check file sharing settings
  3. Wait 5 minutes if file recently accessed
- **Prevention**: Use consistent service account, implement file locking strategy
</error>

### Timeout Errors (504)

<error id="err-504" http_code="504">
- **Symptom**: "Gateway Timeout" or operation takes longer than 120 seconds
- **Cause**: Complex formulas, large row counts, or slow recalculation
- **Immediate Fix**:
  1. Simplify or remove formulas in table
  2. Use empty worksheet for data insertion
  3. Break operation into smaller batches
- **Prevention**: Minimize formulas in automation tables, use Office Scripts for complex operations
- **Reference**: [Limitation lim-008](#lim-008)
</error>

### Table Not Found Errors (404)

<error id="err-404" http_code="404">
- **Symptom**: "Table not found" or "The resource could not be found"
- **Cause**: Table name incorrect, table deleted, or file path wrong
- **Immediate Fix**:
  1. Verify table name in Excel (case-sensitive)
  2. Check file path is correct
  3. Confirm table still exists
- **Prevention**: Store table names in variables, validate table existence before operations
</error>

### Row Not Found Errors

<error id="err-row-404" http_code="404">
- **Symptom**: "Row not found" for Get/Update/Delete operations
- **Cause**: Key column value doesn't match any row, or row deleted
- **Immediate Fix**:
  1. Verify key column value is correct
  2. Check row still exists in Excel
  3. Ensure key column name matches exactly (case-sensitive)
- **Prevention**: Validate key values before operations, implement error handling
</error>

### Duplicate Row Insertions

<error id="err-duplicate" http_code="N/A">
- **Symptom**: Same row inserted multiple times
- **Cause**: Timeout during Add row operation causes retry, complex formulas slow down operation
- **Immediate Fix**:
  1. Check for duplicate rows in Excel
  2. Manually delete duplicates
  3. Simplify formulas in table
- **Prevention**: Use empty worksheet for insertions, add unique constraints, implement deduplication logic
- **Reference**: [Limitation lim-008](#lim-008)
</error>

## Diagnostic Steps

1. **Check Error Details**
   - HTTP status code
   - Error message text
   - Action that failed
   - File path and table name

2. **Verify Configuration**
   - Connection valid (re-authenticate if needed)
   - File path correct
   - Table exists in workbook
   - User has write permissions

3. **Review File State**
   - File not checked out
   - No concurrent edits happening
   - File size under 25MB
   - File not locked from recent operation

4. **Test Incrementally**
   - Test with simple table (no formulas)
   - Try with single row operation
   - Verify table structure matches expectations
   - Check file picker can access file

5. **Check Service Health**
   - OneDrive/SharePoint service status
   - Power Automate service health
   - Graph API availability
</troubleshooting>

<related_docs>
## Documentation Structure

- **Actions**: [actions.md](./actions.md) - All available actions (to be created)
- **Triggers**: [triggers.md](./triggers.md) - Available triggers (to be created)

## Related Connectors

- **SharePoint**: [Link](../SharePoint/overview.md) - Store Excel files in SharePoint libraries
- **OneDrive for Business**: [Link](../OneDrive/overview.md) - Store Excel files in OneDrive
- **Office 365 Outlook**: [Link](../Outlook/overview.md) - Send Excel reports via email
- **Microsoft Teams**: [Link](../Teams/overview.md) - Share Excel files in Teams channels

## External Resources

- **Official Documentation**: https://learn.microsoft.com/en-us/connectors/excelonlinebusiness/
- **Office Scripts Limits**: https://learn.microsoft.com/en-us/office/dev/scripts/testing/platform-limits
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
- **Source**: Microsoft Learn official documentation + Power Platform community
</metadata_summary>
