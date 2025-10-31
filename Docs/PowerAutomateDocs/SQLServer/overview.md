# SQL Server Connector Overview

---
type: connector-overview
connector_name: SQL Server
connector_type: standard
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [sql, database, query, stored procedure, table, row, azure sql, on-premises]
related_connectors: [Dataverse, Excel Online, SharePoint]
api_limits:
  native_calls_per_10s: 500
  crud_calls_per_10s: 100
  max_concurrent_native: 200
  max_concurrent_crud: 125
  execution_timeout_seconds: 110
official_docs_url: https://learn.microsoft.com/en-us/connectors/sql/
---

<official_docs>
https://learn.microsoft.com/en-us/connectors/sql/
</official_docs>

<description>
SQL Server connector provides comprehensive database operations for both Azure SQL and on-premises SQL Server instances, enabling native SQL query execution, CRUD operations on tables, stored procedure calls, and triggers for data changes. Supports multiple authentication methods including Microsoft Entra ID, SQL authentication, and Windows authentication.
</description>

<capabilities>
## Core Capabilities
- Native SQL query execution (SELECT, INSERT, UPDATE, DELETE, JOINs, etc.)
- CRUD operations on database tables
- Stored procedure execution with input parameters
- Triggers for INSERT and UPDATE operations (requires IDENTITY and ROWVERSION columns)
- Table and column metadata retrieval
- Support for Azure SQL and on-premises SQL Server (via gateway)

## Supported Operations
- **Query**: Execute SQL query (V2) - Native T-SQL
- **CRUD**: Insert row, Update row, Delete row, Get row, Get rows (V2)
- **Stored Procedures**: Execute stored procedure (V2)
- **Metadata**: Get tables (V2), Get columns
- **Triggers**: When item created (V2), When item modified (V2)

## Integration Features
- OData-style filtering and ordering for Get rows
- Pagination support with $skip and $top
- Multiple authentication methods (Entra ID, SQL, Windows, Service Principal, Certificate, Managed Identity)
- On-premises data gateway support
- Azure Logic Apps Managed Identity support
</capabilities>

<api_limits>
## Rate Limits

**Native SQL Operations** (Execute SQL query)
- **500 calls per 10 seconds** per connection
- **200 concurrent calls** maximum
- Throttling scope: per connection

**CRUD Operations** (Insert/Update/Delete/Get row)
- **100 calls per 10 seconds** per connection
- **125 concurrent calls** maximum
- Throttling scope: per connection

**Throttling Behavior**
- HTTP Status: 429 (Too Many Requests)
- Error message: "Rate limit exceeded"
- Automatic retry: yes

## Size Limits
- **Query Result**: No explicit documented limit (depends on timeout)
- **Row Size**: Depends on table schema and SQL Server limits
- **Concurrent Operations**: 200 (native) or 125 (CRUD)

## Timeout Limits
- **Execution Timeout**: 110 seconds maximum
- Long-running operations: Must complete within timeout or fail
</api_limits>

<critical_limitations>
## Data Operations

<limitation id="lim-001" severity="medium">
**String Trimming in Azure SQL**: String values trimmed when using Azure SQL instance

- **Impact**: Leading/trailing spaces removed from string values
- **Scope**: Azure SQL database operations
- **Workaround**: Trim strings in flow before comparison, or use CHAR/NCHAR instead of VARCHAR
- **Affected Operations**: All data operations with string columns
</limitation>

<limitation id="lim-002" severity="high">
**Primary Key Required for CRUD**: GetItem, UpdateItem, DeleteItem require primary key

- **Impact**: Cannot use CRUD operations on tables without primary key
- **Scope**: Get row, Update row, Delete row actions
- **Workaround**: Use Execute SQL query for tables without primary key, or add primary key to table
- **Affected Operations**: Get row, Update row, Delete row
</limitation>

## Triggers

<limitation id="lim-003" severity="critical">
**IDENTITY Column Required for Create Trigger**: "When item created" requires IDENTITY column

- **Impact**: Trigger doesn't work without IDENTITY column
- **Scope**: When item created (V2) trigger
- **Workaround**: Add IDENTITY column to table (typically ID column with AUTO_INCREMENT)
- **Affected Operations**: When item created (V2)
</limitation>

<limitation id="lim-004" severity="critical">
**ROWVERSION Column Required for Update Trigger**: "When item modified" requires ROWVERSION column

- **Impact**: Trigger doesn't work without ROWVERSION column for change tracking
- **Scope**: When item modified (V2) trigger
- **Workaround**: Add ROWVERSION column to table (timestamp data type)
- **Affected Operations**: When item modified (V2)
</limitation>

## Authentication & Access

<limitation id="lim-005" severity="high">
**Guest Users Unsupported for Entra ID**: Microsoft Entra ID guest users cannot use Entra ID connections

- **Impact**: Cross-tenant scenarios fail with Entra ID auth
- **Scope**: Microsoft Entra ID authentication
- **Workaround**: Use SQL authentication or internal accounts
- **Affected Operations**: All operations with Entra ID guest user connections
</limitation>

<limitation id="lim-006" severity="medium">
**Limited VNET Support**: Virtual Network environments have limited action support

- **Impact**: Some actions unavailable in VNET-integrated environments
- **Scope**: Azure Logic Apps in VNETs
- **Workaround**: Use standard Logic Apps or check action availability
- **Affected Operations**: Various actions in VNET environments
</limitation>

<limitation id="lim-007" severity="low">
**Gateway Required for On-Premises**: On-premises SQL Server requires on-premises data gateway

- **Impact**: Cannot connect to on-premises SQL without gateway
- **Scope**: On-premises SQL Server instances
- **Workaround**: Install and configure on-premises data gateway
- **Affected Operations**: All operations on on-premises SQL
</limitation>
</critical_limitations>

<authentication>
## Supported Authentication Methods

### Microsoft Entra ID (Recommended)
- Flow type: OAuth with Azure AD
- Required permissions: Database user permissions
- Token refresh: Automatic
- Shareable: No
- Available: Standard and Azure Government variants

### SQL Server Authentication
- Flow type: Username/Password
- Required: SQL Server login credentials
- Shareable: No (credentials stored per connection)

### Windows Authentication
- Flow type: Domain credentials
- Required: Windows domain account
- Shareable: No
- Use case: On-premises SQL Server

### Service Principal (Shareable)
- Flow type: Client ID/Secret
- Required: Azure AD app registration
- Shareable: Yes
- Use case: Unattended automation

### Client Certificate Authentication
- Flow type: Certificate-based
- Required: PFX certificate
- Shareable: Yes

### Managed Identity (Logic Apps Only)
- Flow type: Azure Managed Identity
- Required: System or user-assigned identity
- Shareable: N/A
- Use case: Azure Logic Apps only

## Required Permissions

### Database Permissions
- **SELECT**: Read data (Get rows, Execute query)
- **INSERT**: Create rows (Insert row, Execute query with INSERT)
- **UPDATE**: Modify rows (Update row, Execute query with UPDATE)
- **DELETE**: Remove rows (Delete row, Execute query with DELETE)
- **EXECUTE**: Run stored procedures

### Azure Permissions (for Entra ID auth)
- Database user must exist in Azure SQL database
- User must be granted appropriate database role (db_datareader, db_datawriter, etc.)
</authentication>

<common_use_cases>
## 1. Database Integration
Sync data between SQL Server and SharePoint/Dataverse

## 2. Reporting and Analytics
Extract data from SQL for Power BI or Excel reports

## 3. Data Validation
Query reference data from SQL to validate form submissions

## 4. ETL Workflows
Extract, transform, and load data between SQL and other systems

## 5. Audit Logging
Log flow operations to SQL database for compliance
</common_use_cases>

<best_practices>
## Performance Optimization
1. **Use Parameterized Queries**: Prevent SQL injection and improve plan caching
2. **Select Specific Columns**: Avoid SELECT *, retrieve only needed columns
3. **Implement Pagination**: Use $skip and $top for large result sets
4. **Create Indexes**: Index columns used in WHERE and JOIN clauses
5. **Use Stored Procedures**: Pre-compiled for better performance

## Reliability & Error Handling
1. **Handle Timeouts**: Implement retry logic for 110-second timeout
2. **Validate Data Types**: Ensure data types match table schema
3. **Check Row Counts**: Verify operations affected expected number of rows
4. **Use Transactions**: Wrap related operations in SQL transactions

## Security Best Practices
1. **Use Entra ID Auth**: Prefer Entra ID over SQL authentication
2. **Parameterize Queries**: Never concatenate user input into SQL
3. **Apply Least Privilege**: Grant minimum necessary permissions
4. **Encrypt Connections**: Always use encrypted connections (Azure SQL enforces by default)
5. **Audit Access**: Enable SQL Server auditing for sensitive tables

## Flow Design
1. **Avoid Loops with Queries**: Use JOINs or batch operations instead of row-by-row processing
2. **Cache Reference Data**: Store lookups in variables to reduce queries
3. **Use CRUD Operations**: Prefer CRUD actions over raw SQL for simple operations (better error handling)
</best_practices>

<troubleshooting>
## Common Errors

### Throttling (429)
<error id="err-429" http_code="429">
- **Symptom**: "Rate limit exceeded"
- **Cause**: Exceeded 500 native or 100 CRUD calls per 10 seconds
- **Fix**: Add delays between operations, use batch operations, implement retry logic
- **Reference**: [API Limits](#api_limits)
</error>

### Timeout (504)
<error id="err-504" http_code="504">
- **Symptom**: "Gateway timeout" or "Operation timed out"
- **Cause**: Query exceeded 110-second timeout
- **Fix**: Optimize query (indexes, reduce result set), break into smaller operations
- **Reference**: [Timeout Limits](#api_limits)
</error>

### SQL Syntax Error
<error id="err-sql-syntax" http_code="400">
- **Symptom**: "Incorrect syntax near..." or SQL error message
- **Cause**: Invalid SQL syntax in Execute SQL query
- **Fix**: Validate SQL syntax, test query in SQL Server Management Studio
- **Prevention**: Use parameterized queries, test queries before deploying
</error>

### Permission Denied (403)
<error id="err-403" http_code="403">
- **Symptom**: "Permission denied" or "Cannot open database"
- **Cause**: Insufficient database permissions or user not granted access
- **Fix**: Grant required permissions (SELECT, INSERT, UPDATE, DELETE, EXECUTE)
- **Reference**: [Required Permissions](#authentication)
</error>

### Connection Timeout
<error id="err-connection" http_code="500">
- **Symptom**: "Cannot connect to database" or "Login failed"
- **Cause**: SQL Server unavailable, firewall blocking, incorrect credentials
- **Fix**: Verify SQL Server running, check firewall rules (Azure SQL: allow Azure services), validate credentials
</error>

### Primary Key Missing
<error id="err-pk" http_code="400">
- **Symptom**: "Primary key required" or "Cannot identify row"
- **Cause**: Using Get/Update/Delete row on table without primary key
- **Fix**: Add primary key to table or use Execute SQL query action
- **Reference**: [Limitation lim-002](#lim-002)
</error>

### Trigger Not Firing
<error id="err-trigger" http_code="N/A">
- **Symptom**: Trigger doesn't activate when rows created/modified
- **Cause**: Missing IDENTITY (create trigger) or ROWVERSION (update trigger) column
- **Fix**: Add required column to table schema
- **Reference**: [Limitations lim-003, lim-004](#lim-003)
</error>
</troubleshooting>

<related_docs>
- **Actions**: [actions.md](./actions.md) - To be created
- **Triggers**: [triggers.md](./triggers.md) - To be created
- **Official Docs**: https://learn.microsoft.com/en-us/connectors/sql/
- **Dataverse**: [Link](../Dataverse/overview.md) - Alternative data platform
</related_docs>

<metadata_summary>
- **Last Updated**: 2025-10-31
- **Fetch Date**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 40%
- **Validation Status**: Validated
- **Next Review**: 2025-11-30
</metadata_summary>
