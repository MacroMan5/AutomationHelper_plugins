---
type: node-overview
node_name: PostgreSQL
node_type: database
category: action
auth_required: true
version: 1.0
last_updated: 2025-10-31
keywords: [postgresql, database, sql, relational, query, insert, update, delete, table, schema, credentials]
related_nodes: [MySQL, MongoDB, SQLite, HTTP Request]
rate_limits:
  service_rate_limit: Depends on PostgreSQL server configuration (typically 100-1000 concurrent connections)
  n8n_limit: none (N8N doesn't impose limits, server-side limits apply)
official_docs_url: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.postgres/
---

<official_docs>
- **Node Documentation**: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.postgres/
- **Credentials Setup**: https://docs.n8n.io/integrations/builtin/credentials/postgres/
- **PostgreSQL Official**: https://www.postgresql.org/docs/
</official_docs>

<description>
The PostgreSQL node enables N8N workflows to connect directly to PostgreSQL databases for executing SQL queries, inserting, updating, and deleting data. It supports both standard SQL operations and complex queries with schema/table selection, making it essential for database-driven automation workflows. Perfect for syncing data between systems, automating data operations, and building data-driven decision logic.
</description>

<capabilities>
## Core Capabilities
- Execute arbitrary SQL queries against PostgreSQL databases
- Insert single and batch records into tables
- Update existing records with flexible WHERE conditions
- Delete records based on conditions
- Select and retrieve data with filtering, sorting, and pagination
- Execute stored procedures and functions
- Support for multiple schemas and complex table structures
- Transaction support for multi-step operations
- Connection pooling for optimal resource management

## Supported Operations
- **Execute Query**: Run custom SQL statements (SELECT, INSERT, UPDATE, DELETE, etc.)
- **Insert**: Add new rows to tables with auto/manual field mapping
- **Update**: Modify existing records with WHERE clause conditions
- **Delete**: Remove records matching specified criteria
- **Select**: Query data with filtering and pagination options
- **Insert or Update (Upsert)**: Atomic insert-or-update operations
- **Execute Stored Procedure**: Call database functions and procedures
- **Get Schema**: Retrieve table structure and metadata information

## Integration Features
- OAuth2 and standard credential authentication
- SSL/TLS encryption for secure connections
- SSH tunnel support for remote database access
- Connection timeout configuration (default 30s, customizable)
- Automatic connection pooling
- Support for both localhost and remote PostgreSQL instances
- Compatible with managed PostgreSQL services (AWS RDS, Google Cloud SQL, Azure Database)
- Transaction support for data consistency
- Batch operation support for bulk processing
</capabilities>

<rate_limits>
## Rate Limits

**Service-Level Throttling**
- **Connection limit**: Configurable at PostgreSQL server level (default 100 connections)
- **Query execution time**: No inherent limit, configured at server level
- **Concurrent connections**: Limited by PostgreSQL max_connections setting
- **Throttling scope**: Per PostgreSQL server
- **Retry-After header**: N/A (database-specific)
- **N8N built-in retry**: Yes (configurable exponential backoff)

**Operation-Specific Limits**
- **Insert operations**: Limited by available database connections
- **Bulk operations**: Recommended batch size 1000-5000 rows per operation
- **Large table scans**: May require pagination or WHERE conditions
- **Complex queries**: Execution time depends on query optimization and indexes

**N8N Platform Limits**
- No built-in rate limiting by N8N platform
- Self-hosted: Limited by server resources (CPU, memory, network)
- Cloud: Depends on N8N cloud plan and database server resources
- Memory per execution: 512MB-2GB (depends on result set size)

**Throttling Behavior**
- HTTP Status: 504 (gateway timeout) or database-specific error codes
- Error message: "Connection timeout", "Too many connections", "Query timeout"
- N8N automatic retry: Yes (configurable)
- Recommended retry strategy: Exponential backoff with 3-5 second delays

## Size Limits

**Data Operations**
- Max items per execution: **1000-5000** (configurable, depends on memory)
- Max result set size: Limited by available memory
- Max request payload: **50MB** (typical, depends on server config)
- Max connection timeout: **300 seconds** (configurable)

**Query Operations**
- Max query size: **10MB** (practical limit)
- Max result rows: Unlimited (limited by memory and pagination)
- Max INSERT values clause: **1000-5000 rows** per statement

## Timeout Limits
- Default timeout: **30 seconds** for connection establishment
- Query execution timeout: **300 seconds** (N8N default, configurable)
- Max configurable timeout: **3600 seconds** (1 hour)
- Long-running operations: Supported with proper timeout configuration
</rate_limits>

<critical_limitations>
## Critical Limitations & Workarounds

<limitation id="lim-001" severity="critical">
**Connection Pool Exhaustion**
- **Issue**: PostgreSQL connections are finite resources. High-volume workflows can exhaust the connection pool
- **Impact**: "Too many connections" errors, workflow failures, database service degradation
- **Cause**: Opening connections without proper cleanup or connection pooling
- **Workaround**:
  1. Configure connection pooling in N8N settings
  2. Limit concurrent workflow executions
  3. Reuse connections within single workflow when possible
  4. Implement batch operations instead of individual queries
  5. Monitor active connections: `SELECT count(*) FROM pg_stat_activity;`
- **N8N Handling**: N8N reuses database connections when possible; configure in node settings
</limitation>

<limitation id="lim-002" severity="critical">
**No Server-Side Pagination Support**
- **Issue**: Large result sets must be loaded entirely into memory
- **Impact**: Out-of-memory errors, slow workflow execution, potential crashes
- **Cause**: No built-in pagination in PostgreSQL node (unlike some cloud databases)
- **Workaround**:
  1. Use LIMIT and OFFSET in SELECT queries: `SELECT * FROM table LIMIT 1000 OFFSET 0`
  2. Implement client-side pagination in N8N workflow
  3. Split operations into multiple workflow executions
  4. Use WHERE conditions to filter data at source
  5. Archive old data to reduce table size
- **N8N Handling**: Implement pagination manually using LIMIT/OFFSET in SQL
</limitation>

<limitation id="lim-003" severity="critical">
**Manual Field Mapping Required**
- **Issue**: Auto field mapping fails when incoming data field names don't match table column names
- **Impact**: Data insertion failures, incorrect data mapping, workflow errors
- **Cause**: N8N cannot automatically infer PostgreSQL schema from arbitrary input
- **Workaround**:
  1. Ensure input field names match database column names exactly (case-sensitive)
  2. Use Set node (Edit Fields) to rename incoming fields before PostgreSQL operation
  3. Choose "Map Each Column Manually" option in node configuration
  4. Create views in database that match expected input structure
  5. Use transform queries to prepare data: `SELECT field AS "expectedName" FROM ...`
- **N8N Handling**: Choose mapping strategy in node UI; manual mapping is more reliable
</limitation>

<limitation id="lim-004" severity="high">
**Transaction Isolation Issues**
- **Issue**: No multi-statement transaction support in single node operation
- **Impact**: Data consistency problems, partial updates in failure scenarios
- **Cause**: Each node execution is isolated; multi-step transactions require BEGIN/COMMIT syntax
- **Workaround**:
  1. Include BEGIN/COMMIT/ROLLBACK in Execute Query operation
  2. Implement transaction logic in stored procedures
  3. Use ON CONFLICT clauses for upsert safety
  4. Enable autocommit mode and ensure idempotent operations
  5. Implement application-level retry logic
- **N8N Handling**: Use raw SQL with explicit transaction control
</limitation>

<limitation id="lim-005" severity="high">
**SSL Certificate Validation**
- **Issue**: SSL certificate issues can block connections to remote PostgreSQL instances
- **Impact**: Connection failures, security vulnerabilities if ignoring SSL
- **Cause**: Self-signed certificates, expired certificates, or certificate chain issues
- **Workaround**:
  1. Enable "Ignore SSL Issues" option only for trusted internal networks
  2. Install proper SSL certificates on PostgreSQL server
  3. Use SSH tunnel instead of direct SSL connection
  4. Configure trust store in N8N environment
  5. Use managed PostgreSQL services with valid SSL certificates
- **N8N Handling**: "Ignore SSL Issues" checkbox in credentials (use cautiously)
</limitation>

<limitation id="lim-006" severity="high">
**No Real-Time Change Detection**
- **Issue**: PostgreSQL node doesn't support LISTEN/NOTIFY triggers or subscriptions
- **Impact**: Requires polling for changes, increases latency and database load
- **Cause**: N8N triggers are action-based, not event-based subscriptions
- **Workaround**:
  1. Use Schedule Trigger node with regular polling queries
  2. Implement timestamp-based change detection (WHERE updated_at > last_sync)
  3. Use PostgreSQL LISTEN/NOTIFY with custom webhook listener
  4. Create materialized views with change tracking
  5. Implement application-level event queue
- **N8N Handling**: Combine Schedule Trigger with SELECT queries checking for updates
</limitation>

<limitation id="lim-007" severity="high">
**Character Encoding Issues**
- **Issue**: UTF-8 and special character handling inconsistencies
- **Impact**: Data corruption, mojibake characters, search failures
- **Cause**: Connection encoding mismatch or database encoding configuration
- **Workaround**:
  1. Ensure database created with UTF-8 encoding: `CREATE DATABASE db_name ENCODING 'UTF8';`
  2. Set connection encoding in credentials: `SET client_encoding TO 'UTF8';`
  3. Validate data in Set node before insertion
  4. Use PostgreSQL text encoding functions: `convert()`, `encode()`
  5. Test with special characters in staging environment first
- **N8N Handling**: Configure UTF-8 encoding in PostgreSQL server and N8N connection
</limitation>

<limitation id="lim-008" severity="medium">
**Large Object (BLOB) Handling Limitations**
- **Issue**: Binary Large Objects have limited support in N8N
- **Impact**: Cannot directly insert/retrieve files, base64 encoding overhead
- **Cause**: N8N workflow data serialization constraints
- **Workaround**:
  1. Store file references instead of binary data
  2. Convert binary to base64 for transport: `encode(data, 'base64')`
  3. Use separate file storage (S3, Google Drive) and store URLs
  4. Implement chunked upload for large files
  5. Use bytea type with base64 encoding/decoding
- **N8N Handling**: Use text columns with base64-encoded content or file references
</limitation>
</critical_limitations>

<authentication>
## Authentication Methods

### Standard Username/Password (Most Common)
**Requirements**:
- Host/IP address of PostgreSQL server
- Port number (default 5432)
- Database name
- Username with appropriate table permissions
- User password

**Configuration in N8N**:
1. Add PostgreSQL credential in N8N credentials panel
2. Enter connection details
3. Test connection before saving
4. Reference in PostgreSQL node

**Security Notes**:
- Never hardcode credentials; always use N8N credential system
- Use least-privilege user accounts (read-only for SELECT, insert-only for data load)
- Rotate passwords regularly
- Enable audit logging for sensitive operations

### SSH Tunnel Authentication (Remote/Secure)
**When to use**:
- Connecting to PostgreSQL over untrusted networks
- Private database not exposed to internet
- Corporate VPN/SSH bastion host requirements

**Requirements**:
- SSH host, port, username
- SSH private key or password
- PostgreSQL server reachable from SSH host
- Target PostgreSQL credentials

**Configuration**:
1. Enable "SSH Tunnel" in PostgreSQL credentials
2. Provide SSH connection details
3. Provide PostgreSQL details accessible from SSH host
4. Test end-to-end connection

### Environment-Based Configuration
**For self-hosted N8N**:
- Set `DB_POSTGRE_HOST`, `DB_POSTGRE_PORT`, `DB_POSTGRE_USER`, `DB_POSTGRE_PASSWORD` environment variables
- Reference via `{{ $env.DB_POSTGRE_HOST }}` in N8N expressions

**For managed services** (AWS RDS, Google Cloud SQL, Azure Database):
- Use service-provided connection strings
- Enable network access in service security groups/firewall rules
- Use IAM authentication where available instead of static credentials
</authentication>

<common_use_cases>
## Common Use Cases

### 1. Real-Time Data Synchronization
**Scenario**: Sync customer data from CRM to PostgreSQL database on schedule
- **Typical workflow**: Schedule Trigger → HTTP Request (fetch CRM data) → Set (map fields) → PostgreSQL Insert/Upsert → Email notification
- **Why this operation**: Keeps PostgreSQL database current with external source
- **Considerations**: Duplicate key handling, partial sync recovery, error notifications
- **N8N Pattern**: Use upsert operation with timestamp tracking

### 2. Automated Report Generation
**Scenario**: Generate daily reports by querying PostgreSQL, formatting results, and emailing
- **Typical workflow**: Schedule Trigger → PostgreSQL Select → Set (format data) → Gmail Send → Slack notification
- **Why this operation**: Automates manual reporting tasks, ensures consistency
- **Considerations**: Time zone handling, large result sets, attachment size limits
- **N8N Pattern**: Use LIMIT/OFFSET for pagination, JSON formatting for attachments

### 3. Data Cleanup and Archival
**Scenario**: Archive old records and delete completed tasks from PostgreSQL
- **Typical workflow**: Schedule Trigger → PostgreSQL Select (old records) → Google Drive Upload (archive) → PostgreSQL Delete → Logging
- **Why this operation**: Maintains database performance, compliance with retention policies
- **Considerations**: Transaction safety, backup before delete, verification queries
- **N8N Pattern**: Wrap in error handling, implement soft deletes with status field

### 4. Inventory Management Automation
**Scenario**: Update inventory in PostgreSQL when orders received via webhook
- **Typical workflow**: Webhook Trigger → PostgreSQL Select (current stock) → Math operations (calculate new stock) → PostgreSQL Update → IF (low stock) → Email alert
- **Why this operation**: Real-time inventory synchronization, prevents overselling
- **Considerations**: Concurrent order handling, transaction isolation, stock level thresholds
- **N8N Pattern**: Use SELECT FOR UPDATE for locking rows during update

### 5. Data Validation and Correction
**Scenario**: Identify and fix data quality issues in PostgreSQL records
- **Typical workflow**: Schedule Trigger → PostgreSQL Select (invalid records) → Code node (validation logic) → PostgreSQL Update (corrections) → Audit log
- **Why this operation**: Maintains data quality, identifies data entry errors
- **Considerations**: Validation rules, audit trail, safe update limits
- **N8N Pattern**: Use Code node for complex validation logic, limit updates to prevent accidents
</common_use_cases>

<best_practices>
## Best Practices

### Performance Optimization
1. **Use indexes effectively**: Ensure SELECT, WHERE, and JOIN columns have indexes
   - Check missing indexes: `SELECT * FROM pg_stat_user_tables WHERE seq_scan > idx_scan;`
   - Create strategically: `CREATE INDEX idx_user_email ON users(email);`

2. **Optimize queries**: Use EXPLAIN ANALYZE to identify slow queries
   - Bad: `SELECT * FROM large_table WHERE date > '2025-01-01'` (full table scan)
   - Good: `SELECT id, name FROM large_table WHERE date > '2025-01-01' LIMIT 1000` (indexed, limited)

3. **Batch operations**: Insert/update multiple rows in single operation vs. looping
   - Impact: 10x faster for bulk operations, reduces network overhead
   - N8N Implementation: Use array inputs with INSERT ... VALUES (...), (...), (...)

4. **Connection pooling**: Reuse connections, limit concurrent connections
   - Impact: Prevents "too many connections" errors
   - N8N Implementation: Configure connection pool size in PostgreSQL credentials

5. **Pagination for large results**: Always use LIMIT and OFFSET
   - Impact: Prevents out-of-memory errors, improves workflow reliability
   - N8N Implementation: Implement offset-based or cursor-based pagination

### Reliability
1. **Error Handling**: Wrap PostgreSQL operations in Try/Catch or IF nodes
   - Expected errors: Connection failures, constraint violations, timeout
   - N8N Feature: Use error workflow for retry logic

2. **Idempotent operations**: Design operations that can be safely retried
   - Use UPSERT (INSERT ... ON CONFLICT) for safe retries
   - Include unique constraints to prevent duplicate inserts

3. **Transactions**: Use explicit BEGIN/COMMIT for multi-step operations
   - Ensures all-or-nothing atomicity
   - Prevents partial updates on failure

4. **Audit trails**: Log all write operations (INSERT, UPDATE, DELETE)
   - Create audit tables: `CREATE TABLE audit_log (id, table_name, operation, old_data, new_data, timestamp)`
   - Use triggers or application logging

5. **Backup verification**: Test database backups regularly
   - Prevent data loss scenarios
   - N8N automation: Schedule backup verification workflows

### Security
1. **Use least-privilege accounts**: Create user roles with minimal permissions
   - Read-only: `GRANT SELECT ON schema.* TO readonly_user;`
   - Data load: `GRANT INSERT, UPDATE ON schema.* TO data_loader;`
   - Admin: Restrict to trusted machines only

2. **Encrypt sensitive data**: Use PostgreSQL pgcrypto extension for encryption
   - Encrypt at application level for additional security
   - Never store plain text passwords, API keys, PII

3. **Network security**: Use SSL/TLS and SSH tunnels for remote connections
   - Enforce SSL: `ssl = on` in postgresql.conf
   - Use SSH tunnels for untrusted networks

4. **SQL injection prevention**: Use parameterized queries
   - Always use placeholders in Execute Query
   - Never concatenate user input into SQL strings

5. **Access control**: Monitor and log all database access
   - Enable audit logging: `log_statement = 'all'`
   - Monitor failed connection attempts

### Data Handling
1. **Validate before insert**: Use Set node to validate field types and required fields
   - Prevents database constraint errors
   - Improves error message clarity

2. **Handle nulls properly**: Use PostgreSQL IS NULL / IS NOT NULL
   - Avoid NULL comparisons with =, use IS NULL instead
   - Consider DEFAULT values for optional columns

3. **Type conversions**: Be explicit about data types
   - PostgreSQL type casting: `CAST(field AS INTEGER)` or `field::INTEGER`
   - Validate numeric/date formats before storage

4. **Time zones**: Store all timestamps in UTC
   - Configure session: `SET timezone = 'UTC';`
   - Convert at application level for display

5. **Data archival**: Archive old data regularly to maintain performance
   - Keep active data in main tables
   - Archive pattern: Move to archive table on schedule
   - Prevents table bloat and improves query performance

### Debugging
1. **Connection testing**: Test connection before assuming data issues
   - Use "Test Connection" in N8N credentials panel
   - Verify firewall rules, SSL settings, credentials

2. **Query logging**: Enable and analyze slow queries
   - Enable slow query log: `log_min_duration_statement = 1000;` (log queries > 1s)
   - Use EXPLAIN ANALYZE for query optimization

3. **Row counting**: Verify operations affected expected number of rows
   - PostgreSQL UPDATE/DELETE returns row count
   - Check: `SELECT COUNT(*) FROM table WHERE condition;` after operations

4. **Transaction inspection**: Monitor active transactions
   - View transactions: `SELECT pid, usename, state FROM pg_stat_activity;`
   - Kill stuck transactions: `SELECT pg_terminate_backend(pid);`
</best_practices>

<common_errors>
## Common Errors & Troubleshooting

<error ref="err-001" http_code="08001">
**Error**: "could not connect to server: Connection refused" or "Connection timed out"
- **Cause**: PostgreSQL server is down, unreachable, or firewall blocking connection
- **N8N Context**: Occurs when testing credentials or executing queries
- **Fix**:
  1. Verify PostgreSQL server is running: `systemctl status postgresql` or `pg_isready -h host -p 5432`
  2. Check host and port: Use `telnet host port` to verify connectivity
  3. Check firewall rules: Ensure port 5432 (or custom port) is open
  4. Verify N8N can reach database: Check network routing from N8N to database server
  5. For cloud databases: Enable inbound traffic from N8N IP address
- **Prevention**: Monitor database uptime, test connections before workflows fail
</error>

<error ref="err-002" http_code="08006">
**Error**: "FATAL: too many connections" or "Connection pool exhausted"
- **Cause**: PostgreSQL max_connections limit reached
- **N8N Context**: Occurs under high workflow concurrency
- **Fix**:
  1. Check active connections: `SELECT COUNT(*) FROM pg_stat_activity;`
  2. Increase max_connections in postgresql.conf (requires restart)
  3. Enable connection pooling: Configure in N8N PostgreSQL credentials
  4. Close idle connections: `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle';`
  5. Reduce concurrent workflow executions temporarily
  6. Check for connection leaks in N8N workflows
- **Prevention**: Monitor active connections with alerts
</error>

<error ref="err-003" http_code="42P01">
**Error**: "relation \"table_name\" does not exist" or "table not found"
- **Cause**: Incorrect table name, wrong schema selected, or table doesn't exist
- **N8N Context**: Query execution fails immediately
- **Fix**:
  1. List available tables: `SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';`
  2. Verify schema name: `SELECT schema_name FROM information_schema.schemata;`
  3. Use fully qualified name: `schema_name.table_name` instead of just `table_name`
  4. Check case sensitivity: PostgreSQL is case-sensitive for unquoted identifiers
  5. Use double quotes for mixed case: `"TableName"` not `TableName`
- **Prevention**: Document exact table and schema names, test queries before deploying
</error>

<error ref="err-004" http_code="23505">
**Error**: "duplicate key value violates unique constraint" or "Unique constraint violation"
- **Cause**: Attempting to insert/update record with duplicate value in unique/primary key column
- **N8N Context**: INSERT or UPDATE operations fail
- **Fix**:
  1. Check constraint: `\d table_name` to view constraints
  2. Use UPSERT instead of INSERT: `INSERT ... ON CONFLICT (column) DO UPDATE SET ...`
  3. Pre-check for existence: SELECT before INSERT
  4. Use different unique value
  5. Temporarily disable constraint if needed (dangerous): `ALTER TABLE table_name DISABLE TRIGGER ALL;`
- **Prevention**: Use UPSERT operations, implement duplicate detection logic
</error>

<error ref="err-005" http_code="42883">
**Error**: "function does not exist" or "column does not exist"
- **Cause**: Typo in function/column name, wrong data type, or permission issue
- **N8N Context**: Query execution or function call fails
- **Fix**:
  1. Verify column names: `SELECT column_name FROM information_schema.columns WHERE table_name = 'table';`
  2. List available functions: `SELECT proname FROM pg_proc;` (for specific schema)
  3. Check function signature: `\df function_name` in psql
  4. Verify permissions: `GRANT EXECUTE ON FUNCTION func_name TO user;`
  5. Use correct data types: Function parameters must match exactly
- **Prevention**: Use schema inspection queries, enable IDE autocomplete features
</error>

<error ref="err-006" http_code="57P03">
**Error**: "cannot execute UPDATE/DELETE because concurrent execution" or "Serialization failure"
- **Cause**: Transaction isolation level conflict, concurrent modification
- **N8N Context**: Concurrent workflows modifying same records
- **Fix**:
  1. Check isolation level: `SHOW transaction_isolation;`
  2. Use SELECT FOR UPDATE to lock rows: `SELECT * FROM table WHERE id = ? FOR UPDATE;`
  3. Implement retry logic with exponential backoff
  4. Reduce concurrent workflow executions
  5. Use pessimistic locking (row-level locks) for critical operations
- **Prevention**: Design for concurrency, test under load, implement proper locking
</error>

<error ref="err-007" http_code="53300">
**Error**: "too much SQL recursion" or "stack depth exceeded"
- **Cause**: Recursive query or trigger with circular references
- **N8N Context**: SELECT operations with recursive CTEs (Common Table Expressions)
- **Fix**:
  1. Limit recursion depth: `WITH RECURSIVE cte AS (... UNION ALL ... LIMIT 1000)`
  2. Avoid circular triggers: Review trigger dependencies
  3. Simplify query logic: Break into multiple simple queries
  4. Increase stack_depth_limit (dangerous): `SET max_stack_depth = '4MB';`
- **Prevention**: Test complex recursive queries, monitor query execution time
</error>

<error ref="err-008" http_code="XX000">
**Error**: "Internal error" or unexpected PostgreSQL error
- **Cause**: Database corruption, bug, or resource exhaustion
- **N8N Context**: Intermittent failures, unpredictable errors
- **Fix**:
  1. Check database integrity: `REINDEX DATABASE dbname;`
  2. Monitor server resources: CPU, memory, disk space
  3. Check PostgreSQL logs: `/var/log/postgresql/`
  4. Rebuild corrupted indexes: `REINDEX TABLE table_name;`
  5. Contact PostgreSQL support if persistent
- **Prevention**: Regular maintenance, monitoring, backups
</error>

### SSL/Connection Errors
- **"SSL: CERTIFICATE_VERIFY_FAILED"**: Enable "Ignore SSL Issues" (for trusted networks only) or install valid SSL certificate
- **"No pg_hba.conf entry"**: PostgreSQL server rejecting connection type (TCP, SSL). Check pg_hba.conf configuration
- **"Authentication failed"**: Wrong credentials, user permissions, or authentication method mismatch

### Field Mapping Errors
- **"Column does not exist"**: Field name doesn't match table column (case-sensitive); use Set node to rename fields
- **"Value too long for type"**: Data exceeds column size limit; validate in Set node before insert
- **"Cannot insert NULL"**: Required column missing from insert operation; add missing field or check constraint

### Query Timeout Errors
- **"execution timeout"**: Query taking too long; add indexes, reduce result set with WHERE, use LIMIT
- **"connection timeout"**: Database unreachable or very slow; check network, server load
</common_errors>

<related_operations>
## Related Database Nodes

### Similar Database Nodes
- **MySQL**: Similar operations, different syntax, no UPSERT support
- **MongoDB**: NoSQL alternative, document-based, no transactions
- **SQLite**: Single-file database, no concurrent access, limited scalability
- **SQL Server**: Enterprise alternative, T-SQL dialect, similar operations

### Common Supporting Nodes
- **Set (Edit Fields)**: Transform data to match PostgreSQL schema before INSERT
- **IF**: Validate data or conditions before database operations
- **Code Node**: Complex data transformation, custom SQL generation
- **Loop Over Items**: Process multiple records with database operations
- **Error Trigger**: Handle database failures gracefully

### Workflow Patterns
1. **Data Sync Pattern**: HTTP Request → Set → PostgreSQL Insert/Update → Email Notification
2. **Report Generation**: Schedule → PostgreSQL Select → Set (format) → Email/Slack
3. **Data Validation**: Schedule → PostgreSQL Select → Code (validate) → PostgreSQL Update
4. **Audit Logging**: (Any operation) → PostgreSQL Insert (audit table)
5. **Batch Processing**: Schedule → PostgreSQL Select → Loop → Process → PostgreSQL Update

### See Also
- **Backup Strategy**: Use `pg_dump` for regular backups, store in cloud storage
- **Performance Tuning**: Review slow query log, add indexes, optimize queries
- **High Availability**: Configure replication, read replicas, failover
- **Compliance**: Implement audit logging, encryption, access controls
</related_operations>

<troubleshooting>
## Troubleshooting Guide

### Connection Issues

**Problem**: "Connection refused" errors
- **Check**: PostgreSQL server status, firewall rules, network connectivity
- **Solution**:
  1. Verify server: `sudo systemctl status postgresql` or cloud console
  2. Test connectivity: `telnet host port` or `nc -zv host port`
  3. Check firewall: Security groups (cloud) or `sudo iptables -L` (local)
  4. Verify credentials: Username, password, database name
  5. Check N8N server can reach database: Network routing, DNS resolution
- **N8N Tools**:
  - Use "Test Connection" in credentials panel
  - Check N8N execution logs for connection details
  - Verify N8N server has network access to database

**Problem**: Intermittent connection timeouts
- **Check**: Network latency, database server load, connection pool
- **Solution**:
  1. Increase connection timeout in credentials (up to 300s)
  2. Implement retry logic with exponential backoff
  3. Check database server metrics (CPU, memory, connections)
  4. Review slow queries and optimize
  5. Enable connection pooling
- **N8N Tools**:
  - Configure error workflow for automatic retries
  - Monitor N8N execution metrics
  - Check PostgreSQL system logs

### Query Execution Issues

**Problem**: Queries work in psql but fail in N8N
- **Check**: SQL syntax, parameter binding, transaction context
- **Solution**:
  1. Test exact query in psql: `psql -h host -U user -d database`
  2. Verify parameter values: Use Set node to log values before PostgreSQL
  3. Check transaction context: Avoid mixing autocommit and explicit transactions
  4. Verify escaping: Special characters in dynamic SQL
  5. Test with simpler query: Isolate problem to specific SQL feature
- **N8N Tools**:
  - Use Code node to debug SQL generation
  - Enable verbose logging in N8N
  - Execute Node to test with different data

**Problem**: Performance degradation over time
- **Check**: Query optimization, connection leaks, table bloat
- **Solution**:
  1. Analyze slow queries: `EXPLAIN ANALYZE SELECT ...`
  2. Create missing indexes: `CREATE INDEX idx_name ON table(column);`
  3. Vacuum database: `VACUUM ANALYZE;` (maintenance)
  4. Check table bloat: `SELECT * FROM pg_stat_user_tables;`
  5. Review connection count: Monitor for connection leaks
  6. Archive old data: Move inactive records to archive table
- **N8N Tools**:
  - Monitor execution time trends
  - Log query execution times
  - Schedule maintenance workflows

### Data Issues

**Problem**: Data inconsistency between systems
- **Check**: Sync frequency, error handling, partial updates
- **Solution**:
  1. Enable audit logging: Track all changes
  2. Implement checksums: Verify data integrity
  3. Use UPSERT: Ensure safe retries
  4. Verify timestamps: Sync based on last_modified
  5. Test error scenarios: Network failure during insert
- **N8N Tools**:
  - Add verification step after insert/update
  - Log mismatches to error table
  - Implement reconciliation workflow

**Problem**: NULL values causing issues
- **Check**: Column defaults, NULL handling, validation
- **Solution**:
  1. Define explicit defaults: `ALTER TABLE table ADD COLUMN col DEFAULT '';`
  2. Add NOT NULL constraints: Prevent NULL in critical columns
  3. Use COALESCE: Handle NULLs in queries
  4. Validate before insert: Set node validation
  5. Document NULL meaning: Empty, unknown, not applicable
- **N8N Tools**:
  - Use Set node to provide defaults
  - Add IF node for NULL validation
  - Test with NULL values in staging

### Concurrency Issues

**Problem**: "Duplicate key" errors under load
- **Check**: Insert logic, uniqueness constraints, concurrent executions
- **Solution**:
  1. Use UPSERT: Atomic insert-or-update
  2. Pre-check existence: SELECT before INSERT
  3. Add unique constraint: Prevent accidental duplicates
  4. Implement deduplication: Track processed IDs
  5. Throttle concurrent executions: Limit simultaneous workflows
- **N8N Tools**:
  - Use SELECT FOR UPDATE for row locking
  - Implement error handling for constraint violations
  - Add queue management for high-volume operations

**Problem**: Transaction rollback on concurrent modifications
- **Check**: Isolation level, row locking, concurrent workflows
- **Solution**:
  1. Increase isolation level: READ COMMITTED → SERIALIZABLE (if needed)
  2. Use SELECT FOR UPDATE: Lock rows during update
  3. Implement retry logic: Exponential backoff for serialization failures
  4. Reduce operation scope: Target specific rows, not entire table
  5. Use pessimistic locking: Lock before modification
- **N8N Tools**:
  - Monitor transaction conflicts in logs
  - Implement error workflow for retries
  - Test concurrency scenarios before deployment
</troubleshooting>

---

**Documentation Status**: ✅ **COMPLETE & PRODUCTION-READY**
**Last Updated**: 2025-10-31
**Next Steps**: See "See Also" section for related operations and patterns